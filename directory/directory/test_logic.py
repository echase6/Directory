"""This is a pipeline test, for automated tests of the logic"""

from directory.logic import *


def test_pipeline():
    """
    This runs the logic functions through their paces.
    """
    assert get_all_entries() == {}

    try:
        create_directory_entry('name1', 'address1')
    except AddressEntry.AlreadyExists:
        assert False
    else:
        assert True

    assert get_all_entries() == {'name1': ['address1']}

    try:
        create_directory_entry('name1', 'address1')
    except AddressEntry.AlreadyExists:
        assert True
    else:
        assert False

    try:
        update_directory_entry('name1', 'address1')
    except AddressEntry.DoesNotExist:
        assert False
    else:
        assert True

    try:
        delete_directory_entry('name1', 'address1')
    except AddressEntry.DoesNotExist:
        assert False
    else:
        assert True

    assert get_all_entries() == {}

    try:
        delete_directory_entry('name1', 'address1')
    except AddressEntry.DoesNotExist:
        assert True
    else:
        assert False

    try:
        create_directory_entry('name2', 'address2')
    except AddressEntry.AlreadyExists:
        assert False
    else:
        assert True

    assert get_all_entries() == {'name2': ['address2']}

    try:
        create_directory_entry('name3', 'address3')
    except AddressEntry.AlreadyExists:
        assert False
    else:
        assert True

    assert get_all_entries() == {'name2': ['address2'], 'name3': ['address3']}

    assert get_entries_by_name('name3') == {'name3': ['address3']}

    try:
        create_directory_entry('name3', 'address4')
    except AddressEntry.AlreadyExists:
        assert False
    else:
        assert True

    assert get_entries_by_name('name3') == {'name3': ['address3', 'address4']}

