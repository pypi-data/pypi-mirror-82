# -----------------------------------------------------------------------------
# Description:    General utilities.
# Repository:     https://gitlab.com/quantify-os/quantify-core
# Copyright (C) Qblox BV & Orange Quantum Systems Holding BV (2020)
# -----------------------------------------------------------------------------
import importlib
import copy
import xxhash
import numpy as np
import json
import pathlib
from collections.abc import MutableMapping


def delete_keys_from_dict(dictionary: dict, keys: set):
    """
    Delete keys from dictionary recursively.

    Parameters
    ----------
    dictionary : dict
        to be mutated
    keys : set
        a set of keys to strip from the dictionary
    Returns
    -------
    dict
        a new dictionary that does not included the blacklisted keys
    """
    keys_set = set(keys)  # optimization for the "if key in keys" lookup.

    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = delete_keys_from_dict(value, keys_set)
            else:
                modified_dict[key] = value
    return modified_dict


def make_hash(o):
    """
    Makes a hash from a dictionary, list, tuple or set to any level, that contains
    only other hashable types (including any lists, tuples, sets, and
    dictionaries).

    from: https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    """

    h = xxhash.xxh64()
    if isinstance(o, (set, tuple, list)):

        return tuple([make_hash(e) for e in o])

    elif isinstance(o, np.ndarray):
        # numpy arrays behave funny for hashing
        h.update(o)
        val = h.intdigest()
        h.reset()
        return val

    elif not isinstance(o, dict):
        return hash(o)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))


def import_func_from_string(function_string):
    """
    Based on https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
    """
    mod_name, func_name = function_string.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    return func


def load_json_schema(relative_to, filename):
    """
    Load a JSON schema from file. Expects a 'schemas' directory in the same directory as `relative_to`.

    .. tip:: Typical usage of the form `schema = load_json_schema(__file__, 'definition.json')`

    Parameters
    ----------
    relative_to : str
        the file to begin searching from
    filename : str
        the JSON file to load
    Returns
    -------
    dict
        the schema
    """
    path = pathlib.Path(relative_to).resolve().parent.joinpath('schemas', filename)
    with path.open(mode='r') as f:
        return json.load(f)


def without(d, keys):
    """
    Utility that copies a dictionary exluding a specific list of keys.
    """
    if not isinstance(keys, list):
        keys = [keys]
    new_d = d.copy()
    for key in keys:
        new_d.pop(key)
    return new_d


class KeyboardFinish(KeyboardInterrupt):
    """
    Indicates the user has signalled to safely abort/finish the experiment.
    """
    pass
