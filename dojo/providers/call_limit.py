"""One persistent probe attempt; consumed before dispatch and never refunded."""

import os
from pathlib import Path


class CallLimitError(RuntimeError):
    """Missing, consumed or uncertain call permission; no retry is allowed."""


def consume_one_call(marker: Path) -> None:
    """Exclusive creation is the admission decision, including across processes.

    The caller supplies one fixed project marker, never a new path per request.
    Existing/partial files refuse permission. This caps attempts, not billing.
    """
    marker = Path(marker)
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        with marker.open("xb") as stream:
            stream.write(b"dojo-one-call-consumed-v1\n")
            stream.flush()
            os.fsync(stream.fileno())
    except OSError:
        raise CallLimitError("Probe permit unavailable or already consumed; no request allowed") from None
