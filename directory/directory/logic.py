"""directory Logic."""

from datetime import datetime

from directory.models import AddressEntry
from directory.settings import DATABASE


def create_directory_entry(name, address):
    """
    Create and save an entry, after checking if one already exists.
    Raise an exception if one is found
    :param name:
    :param address:
    :return:
    """
    entries = AddressEntry.objects.using(DATABASE).filter(name=name,
                                                          address=address)
    if len(entries) == 0:
        new_item = AddressEntry(name=name, address=address,
                                date_created=datetime.now(), version=1)
        new_item.save(using=DATABASE)
        return
    raise AddressEntry.AlreadyExists


def update_directory_entry(name, address):
    """
    Update an entry, after checking if one already exists.  This should
        change the date_updated and version fields.
    Raise an exception if one is not found
    :param name:
    :param address:
    :return:
    """
    entries = AddressEntry.objects.using(DATABASE).filter(name=name,
                                                          address=address)
    if len(entries) > 0:
        entries[0].version += 1
        entries[0].date_updated = datetime.now()
        entries[0].save(using=DATABASE)
    else:
        raise AddressEntry.DoesNotExist


def delete_directory_entry(name, address):
    """
    Delete an entry, after checking if one already exists.
    Raise an exception if one is not found
    :param name:
    :param address:
    :return:
    """

    entries = AddressEntry.objects.using(DATABASE).filter(name=name,
                                                          address=address)
    if len(entries) > 0:
        entries.delete()
    else:
        raise AddressEntry.DoesNotExist


def get_all_entries():
    """
    Get all entries, returned as a dictionary
    """
    entries = AddressEntry.objects.all()
    return entries_to_dict(entries)


def get_entries_by_name(name):
    """
    Get all entries that match the name, returned as a dictionary

    :param name: the key
    :return: Needs to be a dict
    """
    entries = AddressEntry.objects.using(DATABASE).filter(name=name)
    return entries_to_dict(entries)


def get_entries_by_name_address(name, address):
    """
    Get all entries that match the name and address, returned as a dictionary
    This should only be one.
    (This function does not have a use but may in the future)
    :param name: the key
    :param address: the key
    :return: Needs to be a dict
    """
    entries = AddressEntry.objects.using(DATABASE).filter(name=name,
                                                          address=address)
    return entries_to_dict(entries)


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
