"""Freeze the accepted Part 1 interfaces for the Part 2 web-agent assignment."""

import hashlib
import json
import sys
from pathlib import Path

from prepare_fasttrack_handoffs import packet

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/reviews/argon'
FILES = (
    'dojo/providers/__init__.py', 'dojo/providers/nebius_codec.py',
    'dojo/providers/fake_session.py', 'tests/test_nebius_codec.py',
    'tests/test_provider_fake_session.py', 'tests/test_provider_boundaries.py',
    'docs/provider-core-adapters.md', 'dojo/store/credits.py',
    'dojo/store/records.py',
)


def main():
    sources = [(name, (ROOT / name).read_bytes()) for name in FILES]
    prompt = '''# Accepted Part 1 supplement for provider restart Part 2

Read with provider-restart-part2-packet-v1.md. This supplement supplies accepted
Part 1, superseding historical proposals or stale copies of these exact paths.
Implement ONLY the eight Part 2 files. Do not replace or rewrite Part 1.
Primary executed 251 offline tests including five independent boundary cases
and existing accounting/controller compatibility cases. This is bounded test
evidence, not provider API verification. No live transport exists or is enabled.
Codec accepts exact ModelRequest; fake session accepts exact ScriptedWireTransport.
PricingSnapshot uses integer nano-USD per million tokens. Unknown usage remains
unknown and stops execution. Fake provider-shaped observations never certify
real provider provenance. Preserve disabled default tracing and untrusted search.
The tests' historical UNEXECUTED headers describe the original web delivery;
primary execution results are recorded separately in the assessment.
'''
    data = packet(prompt, sources, 'END OF ACCEPTED PROVIDER PART 1 SUPPLEMENT')
    name = 'provider-restart-part2-accepted-supplement-v1.md'
    manifest = {'packet': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                'sources': [{'path': n, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
                            for n, b in sources]}
    outputs = {name: data, 'provider-restart-part2-accepted-manifest-v1.json':
               (json.dumps(manifest, indent=2) + '\n').encode()}
    if sys.argv[1:] == ['--check']:
        for n, b in outputs.items():
            if (DEST / n).read_bytes() != b:
                raise ValueError(f'Source/supplement drift: {n}')
    elif not sys.argv[1:]:
        if any((DEST / n).exists() for n in outputs):
            raise FileExistsError('Preserve previous supplement')
        for n, b in outputs.items():
            (DEST / n).write_bytes(b)
    else:
        raise SystemExit('Use no arguments to create or --check to verify')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
