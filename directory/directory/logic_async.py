"""directory Logic.

These are the getters, which make asynchronous calls to the two databases
"""

import asyncio

from directory.models import AddressEntry
from directory.settings import DATABASE, DATABASE_WRITABLE


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
    entries, _ = loop.run_until_complete(asyncio.wait(queries_async))
    return entries_to_dict(entries)


async def get_entries_async(database):
    """
    An asynchronous reader from the database
    :param database:
    :return:
    """
    entries = AddressEntry.objects.using(database).all()
    return entries


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
    entries, _ = loop.run_until_complete(asyncio.wait(queries_async))
    return entries_to_dict(entries)


async def get_entries_async_by_name(database, name):
    """
    An asynchronous reader from the database
    :param database:
    :param name:
    :return:
    """
    entries = AddressEntry.objects.using(database).filter(name=name)
    return entries


def entries_to_dict(entries):
    """
    Convert entries to a dictionary, for serialiazation later
    """
    entry_dict = {}
    for entry in entries:
        for entry_result in entry.result():
            name = entry_result.name
            address = entry_result.address
            if name not in entry_dict:
                entry_dict[name] = [address]
            else:
                if address not in entry_dict[name]:
                    entry_dict[name].append(address)
    return entry_dict
