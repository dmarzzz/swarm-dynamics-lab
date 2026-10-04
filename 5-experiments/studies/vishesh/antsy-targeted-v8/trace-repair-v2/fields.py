"""Development candidate: explicit quantity annotation, never infer corrupted digits."""
import copy
import importlib.util
from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / 'src/fields.py'
spec = importlib.util.spec_from_file_location('frozen_fields', path)
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
# Permit an unclosed parenthesis only when the entire OCR word is the label.
# No hyphen-as-equals repair, arbitrary gap, confidence filter or largest-number rule.
LABEL = re.compile(r'^\s*total\s*\(\s*(?:qty|quantity)\s*=\s*\d+\s*\)?\s*$', re.I)


def extract(words):
    revised = copy.deepcopy(words)
    changes = []
    for index, word in enumerate(revised):
        if LABEL.fullmatch(word['text']):
            changes.append(index)
            word['text'] = 'Total'
    result = base.extract(revised)
    result['contract'] = 'quantity-label-development-v1'
    # The baseline evidence hashes describe normalized observations. Both original
    # and normalized input bindings are retained explicitly; no native evidence edited.
    result['normalization'] = {'original_sha256': base.digest(words),
                               'normalized_sha256': base.digest(revised),
                               'quantity_labels_removed': len(changes)}
    return result
