from logging import exception

from attr import has
from hashtable import HashTable
import pytest
from pytest_unordered import unordered

@pytest.fixture
def hash_table():
    sample_data =  HashTable(capacity=100)
    sample_data["holla"] = "hello"
    sample_data[98.6] = 37
    sample_data[False] = True
    return sample_data

def test_should_create_hashtable():
    assert HashTable(capacity=100) is not None

def test_should_report_length_of_empty_hash_table():
    assert len(HashTable(capacity=100)) == 0

def test_should_create_empty_value_slots():
    # Given
    expected_values = [None, None, None]
    hash_table = HashTable(capacity=3)

    # When
    actual_values = hash_table._pairs

    # Then
    assert actual_values == expected_values

def test_should_insert_key_value_pairs():
    hash_table = HashTable(capacity=100)

    hash_table["holla"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    assert ("holla","hello") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (False, True) in hash_table.pairs

    assert len(hash_table) == 3

@pytest.mark.skip
def test_should_not_shrink_when_removing_elements():
    pass

def test_should_not_contain_none_value_when_created():
    # hash_table = HashTable(capacity=100)
    # values = [pair.value for pair in hash_table.pairs if pair]
    assert None not in HashTable(capacity=100).values

def test_should_insert_none_value():
    hash_table = HashTable(capacity=100)
    hash_table['key'] = None
    assert ('key', None) in hash_table.pairs

def test_should_retrieve_value_by_key(hash_table):
    assert hash_table["holla"] == "hello"
    assert hash_table[98.6] == 37
    assert hash_table[False] == True

def test_should_raise_error_on_missing_key():
    hash_table = HashTable(capacity=100)
    with pytest.raises(KeyError) as exception_info:
        hash_table['missing_key']
    assert exception_info.type is KeyError
    assert exception_info.value.args[0] == 'missing_key'

def test_should_find_key(hash_table):
    assert "holla" in hash_table
    

def test_should_not_find_key(hash_table):
    assert "key_not_found" not in hash_table

def test_should_get_value(hash_table):
    assert hash_table.get("holla") == "hello"

def test_should_return_default_value_when_missing_key(hash_table):
    assert hash_table.get('missing_key', "default_value") == "default_value"

def test_should_return_none_when_missing_key(hash_table):
    assert hash_table.get('missing_key') is None

def test_should_get_value_with_default(hash_table):
    assert hash_table.get("holla", "default") == "hello"

def test_should_delete_key_value_pair(hash_table):
    assert "holla" in hash_table
    assert ("holla","hello") in hash_table.pairs
    assert len(hash_table) == 3

    del hash_table["holla"]

    assert "holla" not in hash_table
    assert ("holla", "hello") not in hash_table.pairs
    assert len(hash_table) == 2

def test_should_raise_key_error_when_delete_missing_key(hash_table):
    with pytest.raises(KeyError) as exception_info:
        del hash_table['missing_key']
    assert exception_info.type is KeyError
    assert exception_info.value.args[0] == 'missing_key'

def test_should_update_existing_key_value_pair(hash_table):
    assert hash_table['holla'] == 'hello'
    hash_table['holla'] = 'phedra'

    assert hash_table['holla'] == 'phedra'
    assert hash_table[98.6]  == 37
    assert hash_table[False] is True
    assert len(hash_table) == 3

def test_should_return_key_value_pairs(hash_table):
    assert ("holla", "hello") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (False, True) in hash_table.pairs

def test_should_return_copy_of_pairs(hash_table):
    assert hash_table.pairs is not hash_table.pairs

def test_should_not_include_blank_pairs(hash_table):
    assert None not in hash_table.pairs

def test_should_return_duplicate_values():
    hash_table = HashTable(capacity=100)
    hash_table['Alice'] = 24
    hash_table['Bob'] = 40
    hash_table['Joe'] = 40
    assert [24, 40, 40] == sorted(hash_table.values)

def test_should_get_values(hash_table):
    assert unordered(hash_table.values) == ['hello', 37, True]

def test_should_get_values_of_empty_hash_table():
    assert HashTable(capacity=100).values == []

def test_should_return_copy_of_values(hash_table):
    assert hash_table.values is not hash_table.values

def test_should_get_keys(hash_table):
    assert hash_table.keys == {'holla', 98.6, False}

def test_should_get_keys_of_empty_hash_table():
    assert HashTable(capacity=100).keys == set()

def should_return_copy_of_keys(hash_table):
    assert hash_table.keys is not hash_table.keys

def test_should_return_pairs(hash_table):
    assert hash_table.pairs == {
        ('holla', 'hello'),
        (98.6, 37),
        (False, True)
    }

def test_should_get_pairs_of_empty_hash_table():
    assert HashTable(capacity=100).pairs == set()

def test_should_convert_to_dict(hash_table):
    dictionary = dict(hash_table.pairs)
    assert set(dictionary.keys()) == hash_table.keys
    assert set(dictionary.items()) == hash_table.pairs
    assert list(dictionary.values()) == unordered(hash_table.values)

def test_should_not_create_hash_table_with_zero_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)

def test_should_not_create_hash_table_with_negative_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=-3)