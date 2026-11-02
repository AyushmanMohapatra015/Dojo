# Security and reporting

Do not post credentials, raw private evidence, account IDs or payment details in
issues or pull requests. Contact the repository owner privately for sensitive
findings. If no private reporting channel is available, open an issue requesting
one without disclosing exploit details or secrets.

## Verified checkpoint, 2026-11-02

- Private repository retained; no collaborator, visibility or token-scope changes.
- Dependabot vulnerability alerts and automatic security fixes enabled.
- Weekly npm and uv dependency update proposals configured. These create reviewable
  pull requests; they do not authorize automatic merging or paid execution.
- Vitest upgraded to 5.0.5; npm audit reports zero known vulnerabilities in the
  current lockfile. All 43 data tests, 51 UI tests and production build pass.
- Local Node 24.12.0 meets the updated toolchain requirement. See package engines.

## Unresolved platform limits and review scope

GitHub rejected secret-scanning enablement as unavailable for this repository.
Push protection could not be enabled through that request. Branch protection is
unavailable on the current private-repository plan. Keep the repository private;
any plan upgrade is an owner decision. No expanded authentication scope was requested.
Do not interpret these unavailable protections as active. Dependabot first-run
results and resulting PRs still need review after the configuration is pushed.

A prior known-pattern scan of 1,111 reachable Git file versions found only
credential-shaped rejection-test fixtures. This does not constitute complete
secret clearance. npm audit is a known-advisory query, not proof of security.
Python dependencies, Docker images, OS packages and the complete application
have not received a comprehensive vulnerability audit in this checkpoint.
No promise that all vulnerabilities or billing risks are eliminated is made.
