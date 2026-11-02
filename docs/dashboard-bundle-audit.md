# Static dashboard bundle audit (8g1)

Run `npm.cmd --prefix .\dashboard run build`, then
`.venv\Scripts\python.exe -m scripts.audit_dashboard_bundle` from the project
root before sharing the generated dashboard. The audit reads only
`dashboard/dist`. It permits an HTML entrypoint and bounded Vite JS/CSS assets,
rejects additional files and source maps, checks the production offline CSP and
synthetic disclosure, and refuses a small list of known private markers.

The current existing build passed with two assets. Five focused fixture tests
passed, covering private text, source-map references, extra files and missing
CSP. No website was deployed. The audit does not prove absence of every secret
or approve publication; review the source and final bundle before release.

The development server intentionally uses Vite hot reload and does not have the
production `connect-src 'none'` policy. A local development preview is therefore
not equivalent to the audited production build.
