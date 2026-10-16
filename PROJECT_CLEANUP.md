# Project completion checkpoint — tools and account access

Status: PENDING. Review this checkpoint when DOJO is finished, before declaring
project handoff complete. This is a persistent checklist, not a scheduled reminder.
No cleanup has been performed by creating this file.

Latest owner direction: continue development using carefully monitored promo
credits after spending safeguards are ready, then request Token Factory card
removal at project completion. Earlier immediate-closure discussions were
superseded. No card removal, account closure or promo redemption is confirmed.

## Token Factory support procedure — reported 2026-10-16

Support's reply supplied by the owner confirms payment-method inactivation is
handled by Customer Support, after account suspension and settlement of any
outstanding amounts. Ownership verification requires User ID and Org ID; share
these only in the verified support channel, not in the project repository.
The account may remain suspended without a payment method and be reactivated
later by adding one. Normal processing is 1–2 days, with confirmation by reply;
this is an estimate, not evidence that the request is already complete.

At project completion:

- [ ] Stop all project workloads and revoke all Token Factory API keys.
- [ ] Check balance/invoices and ask support to confirm no pending/unbilled
  usage remains; resolve any actual amount owed before inactivation.
- [ ] Request account suspension and saved-payment-method inactivation in the
  existing verified support thread; supply User ID and Org ID there if asked.
- [ ] Obtain written confirmation of suspension and payment-method inactivation.
  Keep the account suspended if retaining it; full account deletion is optional.
- [ ] If payment-token erasure is required, ask separately what is deactivated,
  what remains with the processor, and which retention obligations apply.

Support referred the token-deletion question to https://docs.nebius.com/legal/privacy
rather than explicitly confirming processor-token erasure. Inactivation and
deletion are different. None of this introduces a hard spending cap during use.

The owner wants project-added command-line tools removed after completion.
No software setup or cleanup can guarantee absolute safety. Uninstalling a
program and revoking its account access are separate actions; complete both.

## Inventory (update whenever a tool or integration is added)

| Tool / change | Before this project? | End-of-project action |
| --- | --- | --- |
| GitHub CLI 2.102.0 | Installed for this project | Sign out, revoke unused GitHub CLI access, then uninstall. |
| uv 0.13.0 | Added to the existing project .venv | Remove the project-local installation/environment after preserving reproducible setup and checking it is no longer needed. |
| Docker Desktop / CLI | Already installed; started for local validation | Preserve the shared installation. At completion review project images and any uniquely named dojo-validation containers only. |
| Docker validation images | Downloaded python:3.12-slim and built dojo-validation-demo:local | Review/remove these project images if no longer needed; do not prune unrelated images, volumes or containers. Temporary test containers are removed after each run. |
| more-itertools source clone | Downloaded under ignored data/repos/more-itertools | Optional project cache; preserve the upstream revision/provenance and validated record before removing this exact clone. No host dependency installation was performed. |
| Click and attrs source clones | Downloaded under ignored data/repos/click and data/repos/attrs | Optional project caches; preserve audit provenance and records first. Remove only the reviewed clone paths if no longer needed. No host dependency installation was performed. |
| Python .venv | Already existed; project dependencies were added | Review and remove only this disposable environment if no longer needed. Preserve pyproject.toml and uv.lock. |
| Git, Git Credential Manager, Python/Anaconda, winget | Already present | Do not automatically uninstall shared tools. Review with the owner if they want these removed too. |
| Git safe.directory entry | Added for D:/NVIDIA X NEBIUS | Remove this exact entry if it is no longer needed; never clear unrelated entries. |
| Nebius / Tavily / other CLIs | Not installed by this work | Add to inventory if installed later; do not claim they were removed. |

## Checklist — perform at project completion

- [ ] Save intended final code, results and documentation. The owner authorizes
  reviewed checkpoint pushes; verify the GitHub backup before removing any
  project environment.
- [ ] Review the inventory and identify every CLI/integration added during this
  project, including anything added after this checkpoint was written.
- [ ] Sign out of the project GitHub CLI account before uninstalling it:

  ```powershell
  & "C:\Program Files\GitHub CLI\gh.exe" auth logout --hostname github.com --user AyushmanMohapatra015
  ```

  Logout clears the local CLI account. It does not replace server-side revocation.
- [ ] In [GitHub Settings → Applications → Authorized OAuth Apps](https://github.com/settings/applications),
  review GitHub CLI and revoke its authorization if no longer needed. This may
  affect other GitHub CLI sessions using that authorization; review those first.
  Do not revoke unrelated applications.
- [ ] Review Windows Credential Manager and remove project-created credentials
  that are no longer needed. Git Credential Manager credentials may be shared
  with other repositories; do not indiscriminately erase GitHub credentials.
- [ ] Revoke project-only API keys in the relevant provider consoles if created
  later, and clear their environment variables from shells/user settings where
  they were configured. Never print, commit or paste the values.
- [ ] Stop/delete any billable project resources if created later. None were
  provisioned during this GitHub setup.
- [ ] Review the provider's final balance, invoices and saved payment method if
  card onboarding was completed. Current Token Factory docs allow automatic
  charges for usage debt; uninstalling a CLI or revoking a key does not settle
  invoices. Ask provider support about payment-method/account closure if needed.
- [ ] Uninstall GitHub CLI through Windows Installed apps or:

  ```powershell
  winget uninstall --id GitHub.cli --exact
  ```

  Use the registered Windows uninstaller if winget has a problem. Do not manually
  delete Program Files as a substitute for uninstalling.
- [ ] Remove project-only uv/dependency environments and temporary installers/logs
  after verifying the exact paths. Do not delete the project source or .git.
- [ ] After verifying the final backup/push and confirming recovery is unnecessary,
  remove the local email-repair bundle .git/dojo-before-email-fix.bundle. It holds
  the original commits with personal email metadata. Remove only that file;
  preserve .git. Old objects can also remain in local reflogs; do not claim this
  step securely erases all previous metadata from disk.
- [ ] Review the exact project safe.directory entry. If no longer needed, remove
  only this entry:

  ```powershell
  git config --global --fixed-value --unset-all safe.directory "D:/NVIDIA X NEBIUS"
  ```

- [ ] Open a fresh terminal and verify removed executables are no longer found.
  Verify revoked access in the provider account settings as well.
- [ ] Record what was removed, what remains intentionally, and the verification
  date in PROGRESS.md. Close this checklist only after checking actual results.

References: [GitHub CLI logout manual](https://cli.github.com/manual/gh_auth_logout)
and [GitHub OAuth authorization review](https://docs.github.com/en/apps/oauth-apps/using-oauth-apps/reviewing-your-authorized-oauth-apps).
