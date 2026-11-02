"""Preserve the existing packet; prepend only audited integration corrections."""

import json
import sys
from pathlib import Path

from audit_argon_provider_packet import audit
from prepare_fasttrack_handoffs import excerpt, fenced, sha

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / 'docs/reviews/argon/provider-partners-packet-v1.md'
ADDENDUM = ROOT / 'docs/reviews/argon/provider-partners-integration-addendum-v1.md'
TARGET = ROOT / 'docs/reviews/argon/provider-partners-packet-v2.md'


def build():
    report = audit()
    fixture = excerpt('tests/test_cache_identity.py', first=21, last=54)
    original = ORIGINAL.read_bytes()
    content = ('# Argon provider/partner packet v2: targeted integration review\n\n'
               'Read through END OF ARGON PROVIDER PARTNERS PACKET V2.\n'
               'The addendum below has precedence; the original 21-reference\n'
               'assignment remains byte-preserved as the final reference section.\n'
               'Nothing here enables services, keys, billing or registered runs.\n\n'
               + ADDENDUM.read_text(encoding='utf-8')
               + '\n## Additional fixture context\n\n' + fixture
               + '\n## Preserved original packet\n\n'
               + f'Original bytes: {len(original)}; SHA-256: {sha(original)}.\n\n')
    # Wrap the preserved original in a longer fence so its headings and earlier
    # end marker are clearly a reference, not a competing master instruction.
    content += fenced(original.decode('utf-8'), 'markdown')
    content += '\nEND OF ARGON PROVIDER PARTNERS PACKET V2\n'
    data = content.encode('utf-8')
    if len(data) > 200_000:
        raise ValueError('Targeted revision exceeded its context budget')
    report.update({'current_packet': TARGET.relative_to(ROOT).as_posix(),
                   'current_packet_bytes': len(data), 'current_packet_sha256': sha(data),
                   'additional_fixture_source': 'tests/test_cache_identity.py:21-54',
                   'new_implementation_work_packages': 0, 'total_existing_work_packages': 5})
    return data, report


def main():
    data, report = build()
    if sys.argv[1:] == ['--check']:
        if TARGET.read_bytes() != data:
            raise ValueError('Refined packet differs from verified original plus addendum')
    elif not sys.argv[1:]:
        with TARGET.open('xb') as output:
            output.write(data)
    else:
        raise SystemExit('Use no arguments to create or --check to verify')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
