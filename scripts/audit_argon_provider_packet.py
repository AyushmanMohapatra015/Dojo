"""Audit preserved packet bytes and report current-source drift/precision status."""

import hashlib
import json
import re
from decimal import Context, localcontext
from pathlib import Path

from dojo.store.credits import units

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'docs/reviews/argon/provider-partners-packet-v1.md'


def audit():
    text = PACKET.read_bytes().decode('utf-8')
    rows = re.findall(r'^\| ([^|]+) \| (\d+) \| ([0-9a-f]{64}) \|$', text, re.MULTILINE)
    blocks = {}
    lines = text.splitlines(keepends=True)
    index = 0
    while index < len(lines):
        line = lines[index].rstrip('\r\n')
        if not line.startswith('## FILE: '):
            index += 1
            continue
        name = line.removeprefix('## FILE: ')
        index += 1
        while index < len(lines) and not lines[index].strip():
            index += 1
        opening = re.fullmatch(r'(`{4,})[a-z]+\r?\n', lines[index])
        if opening is None or name in blocks:
            raise ValueError('Invalid or duplicate source block')
        fence = opening[1]
        index += 1
        content = []
        while index < len(lines) and lines[index].rstrip('\r\n') != fence:
            content.append(lines[index])
            index += 1
        if index == len(lines):
            raise ValueError('Unclosed outer fence')
        # packet() inserts exactly one additional newline before the outer close.
        blocks[name] = ''.join(content).removesuffix('\n').encode('utf-8')
        index += 1
    if len(rows) != 21 or set(blocks) != {name for name, _, _ in rows}:
        raise ValueError('Reference inventory differs')
    drift = []
    for name, count, digest in rows:
        data = blocks[name]
        if len(data) != int(count) or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError('Embedded reference bytes/hash mismatch')
        current = (ROOT / name).read_bytes()
        if current != data:
            drift.append(name)
    if not text.endswith('END OF ARGON PROVIDER PARTNERS PACKET\n'):
        raise ValueError('End marker missing')
    with localcontext() as context:
        context.prec = 2
        observed = units('0.00012288')
        with localcontext(Context(prec=80)):
            guarded = units('0.00012288')
            assert units('0.0000000001') == 1
            assert units('0.0000000011') == 2
        assert context.prec == 2
    assert guarded == 122880
    def price(prompt, completion):
        return (prompt * 60_000_000 + completion * 240_000_000 + 999_999) // 1_000_000
    assert price(1024, 256) == 122880 and price(400, 50) == 36000
    assert 3 * price(1024, 256) == 368640
    return {'verified_original_references': len(rows), 'complete_source_fences': len(blocks),
            'original_packet_sha256': hashlib.sha256(PACKET.read_bytes()).hexdigest(),
            'current_source_drift': drift,
            'current_sources_match_snapshot': not drift,
            'ledger_precision_probe': {'ambient_precision': 2, 'expected_nano_usd': 122880,
                                       'observed_nano_usd': observed,
                                       'under_reservation_reproduced': observed < 122880,
                                       'guarded_call_nano_usd': guarded,
                                       'caller_precision_restored': True},
            'independent_cost_oracles_verified': True,
            'ledger_created': False, 'provider_calls': 0}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
