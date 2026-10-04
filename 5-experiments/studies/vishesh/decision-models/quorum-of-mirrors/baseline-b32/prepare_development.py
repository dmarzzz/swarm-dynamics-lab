"""Rebuild actor-only development packets from locally retained, hash-bound HTML.
No network, model, credential, or dispatch operation. Full source text stays local.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html


def normalized(node):
    node = copy.deepcopy(node)
    for child in node.xpath('.//script|.//style|.//noscript'):
        child.drop_tree()
    return ' '.join(node.text_content().split())


def source_host(url):
    # Archive is a retrieval service, not the publisher or an independent source.
    if urlsplit(url).hostname == 'web.archive.org':
        for scheme in ('https://', 'http://'):
            position = url.find(scheme, len('https://'))
            if position >= 0:
                return urlsplit(url[position:]).hostname
    return urlsplit(url).hostname


def prepare(manifest, captures):
    actors, evaluators = [], []
    for case in manifest['cases']:
        evidence = []
        for entry in case['evidence']:
            raw = (Path(captures) / entry['document_id'] / 'raw.html').read_bytes()
            if hashlib.sha256(raw).hexdigest() != entry['raw_sha256']:
                raise ValueError('source_hash')
            nodes = html.fromstring(raw).xpath(entry['xpath'])
            if len(nodes) != 1:
                raise ValueError('source_xpath')
            text = normalized(nodes[0])
            start, end = entry['start'], entry['end']
            if not 0 <= start < end <= len(text):
                raise ValueError('source_offsets')
            text = text[start:end]
            if hashlib.sha256(text.encode()).hexdigest() != entry['text_sha256']:
                raise ValueError('passage_hash')
            evidence.append({
                'evidence_id': entry['evidence_id'],
                'document_id': entry['document_id'],
                'source_host': source_host(entry['source_url']),
                'text': text,
            })
        actors.append({key: case[key] for key in ('case_id', 'claim', 'claim_date')} | {'evidence': evidence})
        evaluators.append({key: case[key] for key in ('case_id', 'source_key', 'published_label', 'event_key', 'support_map', 'limitations')})
    return actors, evaluators


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--captures', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    actors, evaluators = prepare(json.loads(args.manifest.read_text()), args.captures)
    args.output.mkdir(parents=True, exist_ok=False)
    for name, content in [('actors.json', actors), ('evaluators.json', evaluators)]:
        (args.output / name).write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'development_packets': len(actors), 'source_bound_passages': sum(len(a['evidence']) for a in actors), 'native_qualified': False}))


if __name__ == '__main__':
    main()
