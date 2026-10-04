#!/usr/bin/env python3
"""Optional Chromium integration check. Requires playwright and installed Chromium.
Set PLAYWRIGHT_BROWSERS_PATH for a non-default browser installation.
"""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


def check():
    checks, errors = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for width, height in [(1440, 1000), (390, 844)]:
            page = browser.new_page(viewport={'width': width, 'height': height}, reduced_motion='reduce')
            page.on('pageerror', lambda e: errors.append(str(e)))
            requests = []
            page.on('request', lambda req: requests.append(req.url))
            page.goto((HERE / 'r1-results/replay.html').as_uri())
            assert '566' in page.locator('#panel').inner_text()
            for i in range(4):
                page.locator(f'[data-step="{i}"]').click()
                assert page.locator('[aria-current="step"]').count() == 1
                assert page.locator('#counter').inner_text() == f'0{i+1} / 04'
                assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
            assert '1,000' in page.locator('#panel').inner_text()
            assert page.locator('#next').is_disabled()
            page.locator('[data-step="2"]').click()
            assert '195/195' in page.locator('#panel').inner_text()
            page.locator('[data-step="0"]').click()
            page.locator('#play').click()
            assert page.locator('#play').inner_text() == 'Pause replay'
            page.locator('#play').click()
            assert page.locator('#play').inner_text() == 'Play replay'
            page.locator('#next').click()
            assert page.locator('#counter').inner_text() == '02 / 04'
            assert not any(url.startswith(('http://', 'https://')) for url in requests)
            checks.append({'viewport': [width, height], 'four_stages': True, 'no_horizontal_overflow': True,
                           'no_network': True, 'metrics_match': True, 'play_pause_and_next': True})
            page.close()
        browser.close()
    assert not errors, errors
    return {'browser': 'chromium', 'checks': checks, 'javascript_errors': errors}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--record', action='store_true')
    args = ap.parse_args()
    result = check()
    text = json.dumps(result, indent=2) + '\n'
    if args.record:
        with (HERE / 'r1-results/browser-check.json').open('x') as f:
            f.write(text)
    print(text, end='')
