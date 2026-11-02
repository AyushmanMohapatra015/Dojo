"""Build/check the replacement two-part offline provider handoff; preserve v1/v2."""

import hashlib
import json
import sys
from pathlib import Path

from prepare_fasttrack_handoffs import ARGON_FILES, packet

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/reviews/argon'
PREFIX = 'provider-restart'
FILES = tuple(dict.fromkeys((*ARGON_FILES,
    'tests/test_credit_precision.py',
    'docs/reviews/argon/provider-integration-intake-notes-v1.md')))


def build():
    sources = [(name, (ROOT / name).read_bytes()) for name in FILES]
    assignment = (DEST / 'provider-partners-assignment-v1.md').read_text(encoding='utf-8')
    addendum = (DEST / 'provider-partners-integration-addendum-v1.md').read_text(encoding='utf-8')
    common = '''This is a fresh replacement assignment, not recovery of a missing response.
You are a web agent without repository access. Use only the supplied exact sources.
Primary has no accepted dojo/providers package. Existing controller accepts exact
ScriptedTransport and synthetic ModelReply only; do not loosen that boundary.
All historical platform prices/model IDs/features below are configuration or
research context, NOT freshly verified current facts. Do not enable live calls.
The current credits.py and precision tests override old arithmetic assumptions.
No API keys, HTTP/SDK/socket clients, environment reads, dependencies, account
changes, live switch, data/spend.sqlite3 access or hosted tracing. Stdlib and
supplied existing project types only. Temporary ledgers and fictional responses.
Return complete files, one fenced block per path, manifest, API map, acceptance
coverage, primary test commands and honest UNEXECUTED labels. No invented test
results, no truncated bodies, no ellipses. If interrupted stop after a complete
file and list remaining paths. Existing sources are read-only references.

Instruction precedence: this replacement scope > exact API addendum > historical
five-WP assignment. Its instruction to complete all five WPs is superseded.
Historical notes referring to a missing response are superseded: do not request it.
Never treat a successful fake session as NVIDIA/Nebius execution evidence.
'''
    scopes = {
        1: '''PART 1 ONLY: complete WP1 and WP2 (8h1/8h2).
Return exactly dojo/providers/__init__.py, dojo/providers/nebius_codec.py,
dojo/providers/fake_session.py, tests/test_nebius_codec.py,
tests/test_provider_fake_session.py and docs/provider-core-adapters.md.
Implement SDK/wire payload separation, bounded duplicate-safe decoding, visible
content vs reasoning, usage accounting despite content failure, and durable
whole-session/per-request reservation checks with restart/uncertainty semantics.
Tests must exercise actual temporary SQL persistence, no-dispatch refusal,
known-usage stops, ambiguous responses, per-request overruns, malformed input,
failure finalization and reopening with a pending reservation. Do not implement
Part 2 or actual network transport. Freeze exported interfaces to the addendum.
''',
        2: '''PART 2 ONLY: complete WP3/WP4/WP5 (11b1/12i2/8h3).
WAIT: primary must first review Part 1 and provide its accepted source supplement
with hashes. If absent, return BLOCKED: accepted Part 1 supplement required.
Do not guess Part 1 implementations, recreate them or import a proposed version.
Return exactly dojo/providers/tavily_codec.py, dojo/providers/trace_events.py,
scripts/partner_adapters_demo.py, tests/test_tavily_codec.py,
tests/test_trace_events.py, tests/test_partner_demo.py and
docs/provider-partner-adapters.md. Reuse accepted Part 1 interfaces unchanged.
Build bounded search decoding/scripted fake search, aggregate-only disabled local
traces and temporary offline composition. Demonstrate no raw content in events,
no emissions when disabled and known/unknown accounting without live services.
No hosted LangSmith/Tavily clients, billing setup or provider runtime wiring.
''',
    }
    outputs = {}
    for part, scope in scopes.items():
        heading = f'# Argon provider replacement: Part {part}\n\n'
        prompt = (heading + common + '\n' + scope + '\n## Authoritative API addendum\n\n'
                  + addendum + '\n## Historical acceptance specification (scope above wins)\n\n'
                  + assignment)
        outputs[f'{PREFIX}-part{part}-packet-v1.md'] = packet(
            prompt, sources, f'END OF PROVIDER RESTART PART {part}')
    manifest = {'task': '8h6', 'live_calls': 0,
                'part2_requires_reviewed_part1_supplement': True,
                'sources': [{'path': n, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
                            for n, b in sources],
                'packets': {n: {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
                            for n, b in outputs.items()}}
    for content in outputs.values():
        if len(content) > 250_000:
            raise ValueError('Packet exceeds 250,000 byte budget')
    outputs[f'{PREFIX}-manifest-v1.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    return outputs


def main():
    if sys.argv[1:] not in ([], ['--check']):
        raise SystemExit('Use no arguments to create or --check to verify')
    outputs = build()
    if not sys.argv[1:]:
        if any((DEST / name).exists() for name in outputs):
            raise FileExistsError('Refusing to overwrite a historical packet')
        for name, data in outputs.items():
            (DEST / name).write_bytes(data)
    else:
        for name, data in outputs.items():
            if (DEST / name).read_bytes() != data:
                raise ValueError(f'Packet/source drift: {name}')
    print(json.dumps({name: len(data) for name, data in outputs.items()}, indent=2))


if __name__ == '__main__':
    main()
