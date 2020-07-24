import xml.etree.ElementTree as et
from collections import defaultdict
import pandas as pd


def flatten_xml(node, key_prefix=()):
    """
    Walk an XML node, generating tuples of key parts and values.
    """

    # Copy tag content if any
    text = (node.text or '').strip()
    if text:
        yield key_prefix, text

    # Copy attributes
    for attr, value in node.items():
        yield key_prefix + (attr,), value

    # Recurse into children
    for child in node:
        yield from flatten_xml(child, key_prefix + (child.tag,))


def dictify_key_pairs(pairs, key_sep='-'):
    """
    Dictify key pairs from flatten_xml, taking care of duplicate keys.
    """
    out = {}

    # Group by candidate key.
    key_map = defaultdict(list)
    for key_parts, value in pairs:
        key_map[key_sep.join(key_parts)].append(value)

    # Figure out the final dict with suffixes if required.
    for key, values in key_map.items():
        if len(values) == 1:  # No need to suffix keys.
            out[key] = values[0]
        else:  # More than one value for this key.
            for suffix, value in enumerate(values, 1):
                out[f'{key}{key_sep}{suffix}'] = value

    return out

	
rows = [dictify_key_pairs(flatten_xml(row)) for row in tree]
df = pd.DataFrame(rows)
