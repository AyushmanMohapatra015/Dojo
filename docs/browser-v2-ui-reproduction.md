# Browser explorer v2 local reproduction (10j3/10j4)

The dashboard loads a bundled **synthetic, UNVERIFIED** explorer view and paired
family diagnostic. It makes zero provider requests. Local file uploads are
validated in the browser against the accepted v2 data contracts. The source
ViewV2 is retained for bootstrap intervals; `deriveExplorerV2` supplies the
read model for charts, tables, run details, and family diagnostics.

From the repository root, with Node 20.19 or newer:

```powershell
cd dashboard
npm ci --ignore-scripts --no-audit --no-fund
npm test
npm run build
npm run preview
```

The preview binds to `127.0.0.1:4173`; open that URL locally. The two bundled
files are exact copies of the accepted `unequal-seeds` pair in
`docs/reviews/argon/browser-v2-context-v1/fixtures/`. To inspect other states,
upload another `.explorer.json` from that fixture directory, then its matching
`.family-diagnostic.json`. Uploading a new view clears the previous diagnostic.
Files larger than 2 MiB are refused before reading.

The production HTML sets `connect-src 'none'` and loads local built JS/CSS.
Development mode uses Vite and has different browser behavior. Static preview
does not prove cross-browser layout, keyboard behavior, screen-reader output,
or deployment suitability; those remain review items under 10j4/10g. The
current v2 schema accepts only synthetic, unverified results, so no real
benchmark claim is shown by this interface.
