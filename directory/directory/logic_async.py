"""directory Logic.

These are the getters, which make asynchronous calls to the two databases
"""

import asyncio
from datetime import datetime

from directory.models import AddressEntry
from directory.settings import DATABASE, DATABASE_WRITABLE


async def get_entries_async(database):
    """
    An asynchronous reader from the database
    :param database:
    :return:
    """
    entries = AddressEntry.objects.using(database).all()
    return entries


async def get_entries_async_by_name(database, name):
    """
    An asynchronous reader from the database
    :param database:
    :param name:
    :return:
    """
    entries = AddressEntry.objects.using(database).filter(name=name)
    return entries


def get_all_entries():
    """
    Get all entries, returned as a dictionary
    This makes two asynchronous calls to read from the two databases,
      and collects the results into one object
    """
    databases = [DATABASE_WRITABLE, DATABASE]
    queries_async = tuple(get_entries_async(database) for database in databases)

    event_loop = asyncio.ProactorEventLoop()  # This may be specific to Windows
    asyncio.set_event_loop(event_loop)
    loop = asyncio.get_event_loop()
    entities, _ = loop.run_until_complete(asyncio.wait(queries_async))

    entity_list = []
    for entity in entities:
        entity_list += entity.result()
    return entries_to_dict(entity_list)


def get_entries_by_name(name):
    """
    Get all entries by name, returned as a dictionary
    This makes two asynchronous calls to read from the two databases,
      and collects the results into one object
    """
    databases = [DATABASE_WRITABLE, DATABASE]
    queries_async = tuple(
        get_entries_async_by_name(database, name) for database in databases)

    event_loop = asyncio.ProactorEventLoop()  # This may be specific to Windows
    asyncio.set_event_loop(event_loop)
    loop = asyncio.get_event_loop()
    entities, _ = loop.run_until_complete(asyncio.wait(queries_async))

    entity_list = []
    for entity in entities:
        entity_list += entity.result()
    return entries_to_dict(entity_list)


def entries_to_dict(entries):
    r"""Convert entries to a dictionary, for serialiazation later

    >>> entry1 = AddressEntry(name='Eric', address='gmail',
    ... date_created=datetime.now(),
    ... date_updated=datetime.now(), version=2)
    >>> entries_to_dict([entry1])
    {'Eric': ['gmail']}
    >>> entry2 = AddressEntry(name='Eric', address='hotmail',
    ... date_created=datetime.now(),
    ... date_updated=datetime.now(), version=5)
    >>> entries_to_dict([entry1, entry2])
    {'Eric': ['gmail', 'hotmail']}
    >>> entry3 = AddressEntry(name='Bob', address='yahoo',
    ... date_created=datetime.now(),
    ... date_updated=datetime.now(), version=2)
    >>> sorted(entries_to_dict([entry1, entry2, entry3]).items())
    [('Bob', ['yahoo']), ('Eric', ['gmail', 'hotmail'])]
    """
    entry_dict = {}
    for entry in entries:
        if entry.name not in entry_dict:
            entry_dict[entry.name] = [entry.address]
        else:
            entry_dict[entry.name].append(entry.address)
    return entry_dict
