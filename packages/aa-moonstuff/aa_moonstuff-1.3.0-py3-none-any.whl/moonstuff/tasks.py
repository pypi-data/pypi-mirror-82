from .models import *
from celery import shared_task
import logging
from esi.models import Token
from esi.clients import esi_client_factory
from django.db import utils
import yaml, requests, bz2

logger = logging.getLogger(__name__)

"""
Swagger Operations:
get_characters_character_id
get_characters_character_id_notifications
get_universe_structures_structure_id
get_universe_moons_moon_id
get_corporation_corporation_id
get_corporation_corporation_id_mining_extractions
post_universe_names
"""


def _get_tokens(scopes):
    try:
        tokens = []
        characters = MoonDataCharacter.objects.all()
        for character in characters:
            tokens.append(Token.objects.filter(character_id=character.character.character_id).require_scopes(scopes)[0])
        return tokens
    except Exception as e:
        print(e)
        return False


@shared_task
def process_resources(scan):
    """
    This function processes a moonscan and saves the resources.

    Example Scan:
                  [
                    ['Moon Name', '', '', '', '', '', ''],
                    ['','Resource Name','Decimal Percentage','Resource Type ID','Solar System ID','Planet ID','Moon ID'],
                    ['...'],
                  ]
    :param scan: list
    :return: None
    """
    try:
        moon_name = scan[0][0]
        system_id = scan[1][4]
        moon_id = scan[1][6]
        moon, _ = Moon.objects.get_or_create(name=moon_name, system_id=system_id, moon_id=moon_id)
        moon.resources.clear()
        scan = scan[1:]
        for res in scan:
            # Trim off the empty index at the front
            res = res[1:]

            # While extremely unlikely, it is possible that 2 moons might have the same percentage
            # of an ore in them, so we will account for this.
            resource, _ = Resource.objects.get_or_create(ore=res[0], amount=res[1], ore_id_id=res[2])
            moon.resources.add(resource.pk)
    except Exception as e:
        logger.error("An Error occurred while processing the following moon scan. {}".format(scan))
        logger.error(e)
    return


@shared_task
def check_notifications(token):
    c = token.get_esi_client()

    # Get notifications
    notifications = c.Character.get_characters_character_id_notifications(character_id=token.character_id).result()
    char = MoonDataCharacter.objects.get(character__character_id=token.character_id)
    moon_pops = []

    moon_ids = Moon.objects.all().values_list('moon_id', flat=True)
    print(moon_ids)

    for noti in notifications:
        if ("MoonminingExtraction" in noti['type']) and ("Cancelled" not in noti['type']):
            # Parse the notification
            text = noti['text']
            parsed_text = yaml.load(text)

            total_ore = 0
            # Get total volume, so we can calculate percentages
            for k, v in parsed_text['oreVolumeByType'].items():
                total_ore += int(v)
            # Replace volume with percent in oreVolumeByType
            for k, v in parsed_text['oreVolumeByType'].items():
                percentage = int(v) / total_ore
                parsed_text['oreVolumeByType'][k] = percentage

            moon_pops.append(parsed_text)

    # Process notifications
    for pop in moon_pops:
        if pop['moonID'] in moon_ids:
            moon = Moon.objects.get(moon_id=pop['moonID'])
            moon.resources.clear()
            # Get ore names
            types = []
            for k in pop['oreVolumeByType']:
                types.append(int(k))
            names = c.Universe.post_universe_names(ids=types).result()
            types = {}
            for name in names:
                types[name['id']] = name['name']
            # Create the resources.
            for k, v in pop['oreVolumeByType'].items():
                # Truncate amount to ensure duplicates are caught correctly
                v = float('%.10f' % v)
                resource, _ = Resource.objects.get_or_create(ore=types[k], amount=v, ore_id_id=k)
                moon.resources.add(resource.pk)
                

@shared_task
def import_data():
    # Get tokens
    req_scopes = [
        'esi-industry.read_corporation_mining.v1',
        'esi-universe.read_structures.v1',
        'esi-characters.read_notifications.v1'
    ]

    tokens = _get_tokens(req_scopes)
    print(tokens)

    for token in tokens:
        c = token.get_esi_client()
        try:
            char = c.Character.get_characters_character_id(character_id=token.character_id).result()
            corp_id = char['corporation_id']
            try:
                corp = EveCorporationInfo.objects.get(corporation_id=corp_id)
            except:
                corp = EveCorporationInfo.objects.create_corporation(corp_id=corp_id)
            e = c.Industry.get_corporation_corporation_id_mining_extractions(corporation_id=corp_id).result()
            for event in e:
                # Gather structure information.
                try:
                    moon = Moon.objects.get(moon_id=event['moon_id'])
                except models.ObjectDoesNotExist:
                    # Moon Info
                    m = c.Universe.get_universe_moons_moon_id(moon_id=event['moon_id']).result()
                    moon, created = Moon.objects.get_or_create(moon_id=event['moon_id'], system_id=m['system_id'],
                                                               name=m['name'])

                try:
                    ref = Refinery.objects.get(structure_id=event['structure_id'])
                except models.ObjectDoesNotExist:
                    r = c.Universe.get_universe_structures_structure_id(structure_id=event['structure_id']).result()
                    refName = r['name']
                    owner = r['owner_id']
                    # TypeIDs: Athanor - 35835 | Tatara - 35836
                    size = True if r['type_id'] == "35836" else False
                    location = event['moon_id']

                    # Save info.
                    ref = Refinery(location=moon, name=refName, structure_id=event['structure_id'],
                                   owner=EveCorporationInfo.objects.get(corporation_id=owner), size=size).save()
                    ref = Refinery.objects.get(structure_id=event['structure_id'])

                # Times
                # Format: 2018-11-01T00:00:59Z
                arrival_time = event['chunk_arrival_time']
                start_time = event['extraction_start_time']
                decay_time = event['natural_decay_time']
                try:
                    extract = ExtractEvent.objects.get_or_create(start_time=start_time, decay_time=decay_time,
                                                                 arrival_time=arrival_time, structure=ref, moon=moon,
                                                                 corp=ref.owner)
                except utils.IntegrityError:
                    continue
            logger.info("Imported extraction data from %s" % token.character_id)
        except Exception as e:
            logger.error("Error importing data extraction data from %s" % token.character_id)
            logger.error(e)

        check_notifications(token)


@shared_task
def pull_ore_types():
    # Get Groups in Asteroid Category (25)
    c = esi_client_factory(version='latest')
    groups = c.Universe.get_universe_categories_category_id(category_id=25).result()
    groups = groups['groups']

    ore_ids = Ore.objects.all().values_list('ore_id', flat=True)

    new_ores = []
    updates = []
    # Get types in group
    for group in groups:
        group = c.Universe.get_universe_groups_group_id(group_id=group).result()
        types = group['types']
        group_id = group['group_id']
        group_name = group['name']
        # Get type info
        for t in types:
            t = c.Universe.get_universe_types_type_id(type_id=t).result()
            if t['type_id'] in ore_ids:
                updates.append(Ore(group_name=group_name,
                                group_id=group_id,
                                ore_name=t['name'],
                                ore_id=t['type_id'],
                                unit_value=None,
                                volume=t.get('volume', None)))
            else:
                new_ores.append(Ore(group_name=group_name,
                               group_id=group_id,
                               ore_name=t['name'],
                               ore_id=t['type_id'],
                               unit_value=None,
                               volume=t.get('volume', None)))
    if len(new_ores) > 0:
        Ore.objects.bulk_create(new_ores, batch_size=500)
    if len(updates) > 0:
        Ore.objects.bulk_update(updates, ['group_name', 'group_id', 'ore_name', 'volume'])
    calc_ore_values.delay()


@shared_task
def calc_ore_values():
    # Get Ore Type IDs
    ore_ids = Ore.objects.all().values_list('ore_id', flat=True).exclude(ore_name__contains="Compressed")

    invTypeMaterials_url = 'https://www.fuzzwork.co.uk/dump/latest/invTypeMaterials.csv.bz2'
    invTypeMaterials_req = requests.get(invTypeMaterials_url)
    with open('invTypeMaterials.csv.bz2', 'wb') as iN:
        iN.write(invTypeMaterials_req.content)
    open('invTypeMaterials.csv', 'wb').write(bz2.open('invTypeMaterials.csv.bz2', 'rb').read())

    mat_types = set()
    mats = {}
    with open("invTypeMaterials.csv", 'r', encoding='UTF-8') as iN:
        text = iN.read()

        rows = text.split('\n')
        for row in rows[1:-1]:
            data = row.split(',')
            # Skip this row if the ID is not an ore
            if int(data[0]) not in ore_ids:
                continue

            if int(data[0]) not in mats:
                mats[int(data[0])] = {data[1]: (int(data[2])*0.876)/100}
            else:
                mats[int(data[0])][data[1]] = (int(data[2])*0.876)/100
            mat_types.add(data[1])

    price_url = 'https://market.fuzzwork.co.uk/aggregates/?station=60003760&types={}'.format(','.join(mat_types))
    price_req = requests.get(price_url)
    price_data = price_req.json()
    values = []
    for ore, mats in mats.items():
        unit_value = 0
        for mat, quant in mats.items():
            unit_value += float(price_data.get(mat).get('buy').get('weightedAverage')) * quant
        values.append((ore, unit_value))

    for ore in values:
        Ore.objects.filter(pk=ore[0]).update(unit_value=ore[1])
