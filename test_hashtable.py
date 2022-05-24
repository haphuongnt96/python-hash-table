from logging import exception

from attr import has
from hashtable import HashTable
import pytest
from pytest_unordered import unordered
from unittest.mock import patch

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

def test_should_report_length(hash_table):
    assert len(hash_table) == 3

def test_should_create_empty_value_slots():
    # Given
    expected_values = [None, None, None]
    hash_table = HashTable(capacity=3)

    # When
    actual_values = hash_table._slots

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

def test_should_report_capacity_of_empty_hash_table():
    assert HashTable(capacity=100).capacity == 100

def test_should_report_capacity(hash_table):
    assert hash_table.capacity == 100

def test_should_iterate_over_keys(hash_table):
    for key in hash_table.keys:
        assert key in ('holla', 98.6, False)

def test_should_iterate_over_values(hash_table):
    for value in hash_table.values:
        assert value in ('hello', 37, True)

def test_should_iterate_over_pairs(hash_table):
    for key, value in hash_table.pairs:
        assert key in hash_table.keys
        assert value in hash_table.values

def test_should_iterate_over_instance(hash_table):
    for key in hash_table:
        assert key in ('holla', 98.6, False)

def test_should_use_dict_literal_for_str(hash_table):
    assert str(hash_table) in {        
        "{'holla': 'hello', 98.6: 37, False: True}",
        "{'holla': 'hello', False: True, 98.6: 37}",
        "{98.6: 37, 'holla': 'hello', False: True}",
        "{98.6: 37, False: True, 'holla': 'hello'}",
        "{False: True, 'holla': 'hello', 98.6: 37}",
        "{False: True, 98.6: 37, 'holla': 'hello'}",
    }

def test_should_create_hashtable_from_dict():
    dictionary = {"holla": "hello", 98.6: 37, False: True}
    hash_table = HashTable.from_dict(dictionary)

    assert hash_table.capacity == len(dictionary) * 10
    assert hash_table.keys == set(dictionary.keys())
    assert hash_table.pairs == set(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())

def test_should_create_hashtable_from_dict_with_custom_capacity():
    dictionary = {"holla": "hello", 98.6: 37, False: True}

    hash_table = HashTable.from_dict(dictionary, capacity=100)

    assert hash_table.capacity == 100
    assert hash_table.keys == set(dictionary.keys())
    assert hash_table.pairs == set(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())

def test_should_have_canonical_string_representation(hash_table):
    assert repr(hash_table) in {
        "HashTable.from_dict({'holla': 'hello', 98.6: 37, False: True})",
        "HashTable.from_dict({'holla': 'hello', False: True, 98.6: 37})",
        "HashTable.from_dict({98.6: 37, 'holla': 'hello', False: True})",
        "HashTable.from_dict({98.6: 37, False: True, 'holla': 'hello'})",
        "HashTable.from_dict({False: True, 'holla': 'hello', 98.6: 37})",
        "HashTable.from_dict({False: True, 98.6: 37, 'holla': 'hello'})",
    }

def test_should_compare_equal_to_itself(hash_table):
    assert hash_table == hash_table

def test_should_compare_equal_to_copy(hash_table):
    assert hash_table is not hash_table.copy()
    assert hash_table == hash_table.copy()

def test_should_compare_equal_with_different_pairs_order():
    h1 = HashTable.from_dict({"a": 1, "b": 2, "c": 3})
    h2 = HashTable.from_dict({"b": 2, "a": 1, "c": 3})
    assert h1 == h2

def test_should_compare_not_equal_with_different_key_value_sets(hash_table):
    other = HashTable.from_dict({"holla": "hello", 98.6: 37, False: "different value"})
    assert hash_table != other

def test_should_compare_not_equal_to_other_datatypes(hash_table):
    assert hash_table != 113

def test_should_copy_keys_values_pairs_capacity(hash_table):
    copy = hash_table.copy()
    assert copy is not hash_table
    assert set(hash_table.keys) == set(copy.keys)
    assert set(hash_table.pairs) == set(copy.pairs)
    assert unordered(hash_table.values) == copy.values
    assert hash_table.capacity == copy.capacity

def test_should_compare_equal_with_different_capacity():
    dictionary = {"a": 1, "b": 2, "c": 3}
    h1 = HashTable.from_dict(dictionary, capacity=50)
    h2 = HashTable.from_dict(dictionary, capacity=100)
    assert h1 == h2

def test_should_create_new_key_value_pairs_update_method(hash_table):
    hash_table.update({"a": 1, "b": 2})
    assert set(hash_table.pairs) == {('holla', 'hello'), (98.6, 37), (False, True), ("a", 1), ("b", 2)}
    hash_table.update(c=3, d=4)
    assert set(hash_table.pairs) == {('holla', 'hello'), (98.6, 37), (False, True), ("a", 1), ("b", 2), ("c", 3), ("d", 4)}

def test_should_update_existing_key_value_pair_update_method(hash_table):
    hash_table.update({"holla": "nana", False: False})
    assert set(hash_table.pairs) == {('holla', 'nana'), (98.6, 37), (False, False)}
    hash_table.update({98.6: 100}, holla=5)
    assert set(hash_table.pairs) == {('holla', 5), (98.6, 100), (False, False)}

@patch("builtins.hash", return_value=42)
def test_should_detect_hash_collision(hash_mock):
    assert hash("foobar") == 42