# Offline probe readiness (6e6)

Run from the project root:

```powershell
.\.venv\Scripts\python.exe -m dojo.probe_readiness
```

This makes no network calls, never creates a ledger or consumes/resets the
one-call permit, and prints only allowlisted statuses. The key may be loaded
into this short-lived host process but its value is never printed. A configured
key has not been authenticated. Existing ledger status checks use a short
SQLite transaction and can report unavailable while another process holds it.
The command deliberately never authorizes live execution.

Actual inspection: key configured, permit not consumed, ledger unavailable,
live policy false, input bound unverified. No inference requests were sent.
31 focused offline tests passed in 1.53 seconds and scoped Ruff passed.

## Tokenizer investigation

NVIDIA publishes the BF16 model repository at:
https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16

Pinned revision: bf77c3174f68ad409e1c2aa60daeb46e32d1c606.
Hashes/byte lengths of tokenizer configuration and chat template were recorded
in probe-tokenizer-source-v1.json using bounded public downloads. No model
weights were downloaded, template executed, or packages installed. The local
environment has neither tokenizers nor jinja2. A local tokenizer count was not
computed; provider tokenizer/template agreement is not verified. This research
does not turn the estimated input allowance into a proven provider bound.

For support, an optional question the owner can send with the credit-expiry
question is: Which tokenizer revision and chat template serve Nano, and do
max_tokens/max_completion_tokens=64 cap all generated/billed reasoning tokens?
Can input tokens for our fixed short arithmetic prompt be counted before an
inference request? No message has been sent by this workspace.
