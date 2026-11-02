# Open the local website

After Python and website dependency setup, run this from the project root:

```powershell
.\start-dashboard.cmd
```

Open `http://127.0.0.1:5173/` on the same PC. The launcher first checks whether
Dojo already responds on that address. Otherwise it starts the installed Vite
server, bound only to loopback. Keep the launching terminal open and press
Ctrl+C to stop a server started there. It does not install dependencies,
modify account settings, expose the site publicly or initiate inference.

You can also launch directly from the project root:

```powershell
npm.cmd --prefix .\dashboard run dev
```

If npm reports a missing `D:\NVIDIA X NEBIUS\package.json`, it was run in the
project root without the dashboard prefix. If the browser cannot connect,
the local server may have stopped; run the launcher again. A port-in-use
failure may mean another process owns port 5173; do not kill it without
checking what it is. The launcher does not stop or replace existing processes.

The 2026-11-02 unreachable-page incident had no listener on ports 5173/4173.
Starting the local Vite process restored the Dojo page with HTTP 200. The
launcher then recognized and reused that server. The site is still a local
synthetic example; this check is not public hosting or model execution.
