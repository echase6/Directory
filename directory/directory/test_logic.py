"""This is a pipeline test, for automated tests of the logic"""

from directory.logic import *
from directory.logic_async import *


def test_pipeline():
    """
    This runs the logic functions through their paces.
    """
    assert get_all_entries() == {}

    success = create_directory_entry('name1', 'address1')
    if success:
        assert True
    else:
        assert False

    assert get_all_entries() == {'name1': ['address1']}

    success = create_directory_entry('name1', 'address1')
    if success:
        assert False
    else:
        assert True

    success = update_directory_entry('name1', 'address1')
    if success:
        assert True
    else:
        assert False

    success = delete_directory_entry('name1', 'address1')
    if success:
        assert True
    else:
        assert False

    assert get_all_entries() == {}

    success = delete_directory_entry('name1', 'address1')
    if success:
        assert False
    else:
        assert True

    success = create_directory_entry('name2', 'address2')
    if success:
        assert True
    else:
        assert False

    assert get_all_entries() == {'name2': ['address2']}

    success = create_directory_entry('name3', 'address3')
    if success:
        assert True
    else:
        assert False

    assert get_all_entries() == {'name2': ['address2'], 'name3': ['address3']}

    assert get_entries_by_name('name3') == {'name3': ['address3']}

    success = create_directory_entry('name3', 'address4')
    if success:
        assert True
    else:
        assert False

    assert get_entries_by_name('name3') == {'name3': ['address3', 'address4']}

