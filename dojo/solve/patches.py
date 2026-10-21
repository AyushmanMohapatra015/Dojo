"""Git-compatible UTF-8 patch export, including empty-file creation and deletion."""

import difflib
import hashlib
from pathlib import PurePosixPath

from dojo.mine.real_task import safe_path

PATCH_BYTES = 1024 * 1024
PATCH_PROTOCOL = 'git-text-empty-v1'
EMPTY_BLOB = hashlib.sha1(b'blob 0\0').hexdigest()


def _lines(data):
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError('Non-UTF-8 text patch export is unsupported') from exc
    # Git hunks count LF-separated lines; Python splitlines also splits vertical
    # tabs and other Unicode separators and can silently change those bytes.
    pieces = text.split('\n')
    return [line + '\n' for line in pieces[:-1]] + ([pieces[-1]] if pieces[-1] else [])


def make_patch(base, current):
    """Never execute a patch here; callers retain and validate the file snapshots."""
    result, size = [], 0

    def emit(line):
        nonlocal size
        size += len(line.encode('utf-8'))
        if size > PATCH_BYTES:
            raise ValueError('Patch export exceeds adapter limits')
        result.append(line)

    for name in sorted(base.keys() | current.keys()):
        in_base, in_current = name in base, name in current
        old, new = base.get(name, b''), current.get(name, b'')
        if old == new and in_base == in_current:
            continue
        if (not safe_path(name) or str(PurePosixPath(name)) != name
                or any(ord(char) < 32 for char in name)):
            raise ValueError('Unsafe patch path')
        if any(char.isspace() or char == '"' for char in name):
            raise ValueError('Quoted patch paths need a later patch exporter')
        if b'\0' in old or b'\0' in new:
            raise ValueError('Binary patch export is unsupported')
        before, after = _lines(old), _lines(new)
        emit(f'diff --git a/{name} b/{name}\n')
        if not in_base:
            emit('new file mode 100644\n')
        elif not in_current:
            emit('deleted file mode 100644\n')
        if not old and not new:
            # Header-only unified diffs do not describe an empty file operation.
            # Git's mode and empty-blob metadata carry the existence transition.
            old_oid, new_oid = (EMPTY_BLOB, '0' * 40) if in_base else ('0' * 40, EMPTY_BLOB)
            emit(f'index {old_oid}..{new_oid}\n')
            continue
        for line in difflib.unified_diff(before, after,
                                         fromfile='a/' + name if in_base else '/dev/null',
                                         tofile='b/' + name if in_current else '/dev/null'):
            if not line.endswith('\n'):
                line += '\n\\ No newline at end of file\n'
            emit(line)
    return ''.join(result)
