# Local Nebius key setup (6e3)

The verifier explicitly reads only NEBIUS_API_KEY from the project-root .env
when live mode is requested. Existing nonempty process environment wins.
Dry runs do not load the file. No shell execution, variable expansion or other
.env variables are supported. UTF-8 (including BOM), comments and matching outer
quotes are accepted; duplicate, empty, whitespace-containing, malformed quoted
or oversized entries fail with a fixed error. Limit: 16 KiB.

The key is copied into the host process environment; candidate containers must
continue to exclude credentials. Never copy this file into a deployment,
review packet or Git commit. Loading is not API authentication verification.
No network request is made by the loader. The existing live switch and durable
accounting / one-attempt guard remain independent requirements.

Evidence: 47 offline tests passed; scoped Ruff clean; local boolean-only load
succeeded. No provider calls. See supervised-probe-next-steps.md for remaining
balance/expiry/exclusive-use and maximum allowance prerequisites.
