# Utilities for working with data structures
# % imports
import re


def dict_key_list_assign(dictionary, keys, value):
    """
    Assigns [value] as a nested index of the [dictionary] of the given list of [keys].
    """
    assert keys
    assert isinstance(
        dictionary, dict), f"Expected dictionary but got {type(dictionary)}"

    sub_dictionary = dictionary

    for key in keys[:-1]:
        if key not in sub_dictionary or not isinstance(sub_dictionary[key], dict):
            sub_dictionary[key] = {}

        sub_dictionary = sub_dictionary[key]

    sub_dictionary[keys[-1]] = value
    return dictionary


def list_pop_adjacent_same_values(lizt):
    """
    Removes values from a list if they are adjacent to items of the same value.
    """
    assert isinstance(lizt, list), f"Expected dictionary but got {type(lizt)}"

    i = 0

    while i < len(lizt)-1:
        if lizt[i] == lizt[i+1]:
            lizt.pop(i)
        else:
            i += 1

    return lizt


def replace_dict_keys_recursive(dictionary, key_mapping, exhaustive=True):
    """
    Changes the names of keys in a nested dictionary, using a key name mapping
    """
    assert isinstance(
        dictionary, dict), f"Expected dictionary but got {type(dictionary)}"
    output_dictionary = {}

    for k_raw in dictionary:
        k = k_raw.strip()
        if k in key_mapping:
            output_dictionary[key_mapping[k]] = dictionary[k]

            if isinstance(output_dictionary[key_mapping[k]], dict):
                output_dictionary[key_mapping[k]] = replace_dict_keys_recursive(
                    output_dictionary[key_mapping[k]], key_mapping, exhaustive)

        elif k.upper() in key_mapping.values():
            output_dictionary[k.upper()] = dictionary[k]

        elif exhaustive:
            raise ValueError(f"Could not find key in key mapping: {k}")

    return output_dictionary


def flatten_dict_keys(dictionary, flatten=lambda x: list(map(lambda y: y.strip(), re.split(',| and ', x)))):
    """
    Flatten the keys of a [dictionary] if [fun] turns the keys into multiple keys.
    """
    assert isinstance(
        dictionary, dict), f"Expected dictionary but got {type(dictionary)}"
    keys = list(dictionary.keys())

    for k in keys:
        v = dictionary[k]

        # recursively call function on values that are dictionaries
        if isinstance(v, dict):
            flatten_dict_keys(v, flatten)

        # if the key could be split, split it, reassign the keys to the value, and recurse
        split = flatten(k)

        if len(split) > 1:
            for s in split:
                dictionary[s] = dictionary[k]

            del dictionary[k]

    return dictionary


def split_dict_vals(dictionary, split=lambda x: list(map(lambda y: y.strip(), re.split(',|/', x)))):
    """
    Flatten the keys of a [dictionary] if [fun] turns the keys into multiple keys.
    """
    assert isinstance(
        dictionary, dict), f"Expected dictionary but got {type(dictionary)}"

    for k, v in dictionary.items():
        # if the value is a string, flatten it
        if isinstance(v, str):
            v = dictionary[k]
            lst = split(v)

            if len(lst) > 1:
                dictionary[k] = lst

        # if the value is a dictionary, recurse
        elif isinstance(v, dict):
            split_dict_vals(v, split)

    return dictionary


def json_preprocess(tree):
    """
    Preprocess [tuple]/[dict]/[list] items for JSON serialization
    """
    if isinstance(tree, dict):
        return {k: json_preprocess(v) for k, v in tree.items()}
    if isinstance(tree, tuple) and hasattr(tree, '_asdict'):
        return json_preprocess(tree._asdict())
    if isinstance(tree, (list, tuple)):
        return list(map(json_preprocess, tree))
    return tree


def get_nested_iterable_values(iterable):
    if isinstance(iterable, dict):
        for v in iterable.values():
            if isinstance(v, dict) or isinstance(v, list) or isinstance(v, tuple):
                yield from get_nested_iterable_values(v)
            else:
                yield v
    elif isinstance(iterable, list) or isinstance(iterable, tuple):
        for v in iterable:
            if isinstance(v, dict) or isinstance(v, list) or isinstance(v, tuple):
                yield from get_nested_iterable_values(v)
            else:
                yield v


# % main
if __name__ == "__main__":
    a = {4: 1, 6: 2, 7: {8: [3, 9, [10, 11]],
                         9: 4, 5: {10: 5}, 2: 6, 6: {2: 7, 1: 8}}}
    print(sorted(list(get_nested_iterable_values(a))))
