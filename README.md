# SmartyPOS public MCP server - Syrve (iiko USA) restaurant POS

Public, read-only, no-auth [MCP](https://modelcontextprotocol.io) server that lets AI agents discover information about **Syrve** (the international/US edition of the **iiko** restaurant platform) and **SmartyPOS**, its US implementation and support partner (Sheno Inc., Sarasota FL).

- Endpoint: **https://mcp.smartypos.us/mcp** (streamable HTTP, stateless, no authentication)
- Site: https://smartypos.us/ - llms.txt: https://smartypos.us/llms.txt
- iiko in the USA = Syrve. iikoFront / iikoOffice / iikoCloud API = Syrve POS / Syrve Office / Syrve Cloud API.

## Tools (all read-only)

| Tool | What it returns |
|---|---|
| `about_smartypos` | Who SmartyPOS is, what Syrve is, partner listing |
| `syrve_features(category?)` | Features with live / pilot / coming_soon status |
| `ai_capabilities` | Open API (read+write), private MCP, AI ordering site, AI call review |
| `compare_pos(competitor)` | toast, clover, square, spoton, lightspeed, touchbistro, skytab - sourced, dated 2026-11 |
| `pricing` | Counter $59 / Service $99 / Group $129 per month; no processor lock-in |
| `integrations` | Marketplaces, couriers, Meta CAPI, Google Ads, Twilio, MCP, open API |
| `case_studies` | anonymized cases by concept, city and state (pizzeria, food court, restaurants in New York and Florida), Redman |
| `iiko_in_usa` | iiko to Syrve name mapping and FAQ |
| `contact_and_demo` | Demo link and contacts |

Resources: `smartypos://llms.txt`, `smartypos://llms-full.txt`. Prompt: `choose_restaurant_pos`.

Comparisons are compiled by a Syrve partner (not independent) from public sources; each competitor entry has source URLs and a checked date. Pilots are marked as pilots.

## Connect

- **Claude** (claude.ai / Desktop): Settings > Connectors > Add custom connector > URL `https://mcp.smartypos.us/mcp`.
- **Claude Code**: `claude mcp add --transport http smartypos https://mcp.smartypos.us/mcp`
- **ChatGPT**: Settings > Connectors > Advanced > Developer mode > add MCP server `https://mcp.smartypos.us/mcp` (no auth).
- **Cursor / others**: `{"mcpServers": {"smartypos": {"url": "https://mcp.smartypos.us/mcp"}}}`
- **Inspector**: `npx @modelcontextprotocol/inspector --cli https://mcp.smartypos.us/mcp --transport http --method tools/list`

## Run locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
MCP_PORT=8140 .venv/bin/python server.py      # http://127.0.0.1:8140/mcp
.venv/bin/python tests/e2e.py http://127.0.0.1:8140/mcp
```

Content lives in `data/*.json` (plus `data/llms*.txt`, copies of the website files). No secrets.

## Deployment (Ubuntu, systemd, nginx)

`deploy/smartypos-public-mcp.service` (port 8140 on 127.0.0.1), `deploy/public-mcp-limit.conf` (limit_req zone, goes in `/etc/nginx/conf.d/`), `deploy/nginx-public-mcp-locations.conf` (locations `= /mcp`, `= /mcp/`, `= /` with CORS and rate limit, inserted into the `mcp.smartypos.us` server block before `location / { return 404; }`). The private tenant MCP at `/t/<slug>/` is a separate service and is untouched.

Registry publishing: see `docs/PUBLISH.md`.

MIT License. (c) Sheno Inc.
