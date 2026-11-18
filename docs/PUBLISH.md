# Publishing the SmartyPOS MCP server to catalogs

Prerequisites (done): server live at https://mcp.smartypos.us/mcp; `server.json`, `smithery.yaml`, `glama.json`, `Dockerfile` in repo root; `mcp-publisher` v1.8.9 in `~/bin`; Ed25519 key in `/home/openclaw/.secrets/mcp-registry/` (private, mode 600, never in git).

## 1. Official MCP Registry (registry.modelcontextprotocol.io)

Name `us.smartypos/syrve-pos` is verified by HTTP domain auth for `smartypos.us`.

1. After the website deploy, confirm the proof file is served (200, no redirect, plain text):
   ```bash
   curl -sS -o - -w '\n%{http_code}\n' -H 'Accept: text/plain' -A 'mcp-registry/1.0' https://smartypos.us/.well-known/mcp-registry-auth
   # expected body: v=MCPv1; k=ed25519; p=HbP7EyJxOOcmzjIpNgr2dUSQRi/x2ppz8tqVusD+pp4=
   ```
   (source file: `site-smartypos/webroot/.well-known/mcp-registry-auth`; make sure WAF/redirects do not interfere.)
2. Login and publish:
   ```bash
   export PATH=$HOME/bin:$PATH
   mcp-publisher login http --domain smartypos.us --private-key-file /home/openclaw/.secrets/mcp-registry/private-key.hex
   cd /home/openclaw/work/smartypos-mcp
   mcp-publisher validate
   mcp-publisher publish
   ```
3. Verify: `curl "https://registry.modelcontextprotocol.io/v0/servers?search=smartypos"`.
4. New version: bump `version` in `server.json`, publish again.

If login fails with 401, the registry could not fetch the proof file (check step 1).
Regenerate the key if needed (see `docs`): `openssl genpkey -algorithm Ed25519 -out key.pem`; record = `v=MCPv1; k=ed25519; p=$(openssl pkey -in key.pem -pubout -outform DER | tail -c 32 | base64)`.

## 2. Glama (glama.ai)

1. Repo contains `glama.json` (maintainer maximemmmm) and a `Dockerfile`.
2. Open https://glama.ai/mcp/servers , click "Add Server", paste `https://github.com/maximemmmm/smartypos-mcp` (or it is picked up automatically from the official registry/GitHub within days).
3. On the server page, "Claim ownership" via GitHub (needs `glama.json`), then check the build/inspection passes (tools listed).

## 3. mcp.so

1. Go to https://mcp.so and click "Submit" (top bar), or open an issue/form at https://mcp.so/submit.
2. Type: Server. Name: `SmartyPOS - Syrve (iiko USA) restaurant POS`. URL: `https://github.com/maximemmmm/smartypos-mcp`. Server URL (remote): `https://mcp.smartypos.us/mcp`. Description and tags: syrve, iiko, restaurant-pos, toast-alternative, open-api, mcp, ai.

## 4. Smithery (smithery.ai)

1. Sign in at https://smithery.ai with GitHub (maximemmmm).
2. "New" > "Server" > either connect the GitHub repo `maximemmmm/smartypos-mcp` (uses `smithery.yaml` + `Dockerfile`, container runtime, HTTP on `$PORT` at `/mcp`) or choose "Connect an external URL" and enter `https://mcp.smartypos.us/mcp` (no auth needed).
3. Deploy / publish; Smithery scans the tools (9 tools, read-only).
4. CLI alternative: `npx @smithery/cli@latest mcp publish https://github.com/maximemmmm/smartypos-mcp -n maximemmmm/smartypos` (verify flags with `--help`; the web flow is the reliable path).

## After publishing
- Add the registry link to https://smartypos.us/features/ai-mcp/ and the README.
- Record in status log: `~/biz/.setup/status-sync/status-log smartypos-mcp "Published to <catalog>"`.
