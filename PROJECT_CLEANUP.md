# Project completion checkpoint — tools and account access

Status: PENDING. Review this checkpoint when DOJO is finished, before declaring
project handoff complete. This is a persistent checklist, not a scheduled reminder.
No cleanup has been performed by creating this file.

The owner wants project-added command-line tools removed after completion.
No software setup or cleanup can guarantee absolute safety. Uninstalling a
program and revoking its account access are separate actions; complete both.

## Inventory (update whenever a tool or integration is added)

| Tool / change | Before this project? | End-of-project action |
| --- | --- | --- |
| GitHub CLI 2.102.0 | Installed for this project | Sign out, revoke unused GitHub CLI access, then uninstall. |
| uv 0.13.0 | Added to the existing project .venv | Remove the project-local installation/environment after preserving reproducible setup and checking it is no longer needed. |
| Python .venv | Already existed; project dependencies were added | Review and remove only this disposable environment if no longer needed. Preserve pyproject.toml and uv.lock. |
| Git, Git Credential Manager, Python/Anaconda, winget | Already present | Do not automatically uninstall shared tools. Review with the owner if they want these removed too. |
| Git safe.directory entry | Added for D:/NVIDIA X NEBIUS | Remove this exact entry if it is no longer needed; never clear unrelated entries. |
| Nebius / Tavily / other CLIs | Not installed by this work | Add to inventory if installed later; do not claim they were removed. |

## Checklist — perform at project completion

- [ ] Save intended final code, results and documentation. The owner handles
  GitHub pushes; verify the backup before removing any project environment.
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
