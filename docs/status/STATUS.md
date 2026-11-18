# SmartyPOS public MCP - project status (living document)

Updated at every milestone. Newest entries on top in the log. Plain language first, details after.

**Purpose.** Public, read-only, no-auth MCP server that lets AI agents discover information about Syrve (the international/US edition of the iiko restaurant platform) and SmartyPOS, its US implementation and support partner (Sheno Inc., Sarasota FL).

Repo: github.com/maximemmmm/smartypos-mcp - default branch `main`. Runs on the VPS in `/home/openclaw/work/smartypos-mcp`.

## What is live where (as of 2026-11-18)

_Generated automatically by `status-sync` on the VPS (daily 06:40 ET). Do not edit this table by hand - add milestones with `status-log`._

| Where | What runs | Version / commit | Notes |
|---|---|---|---|
| server checkout `/home/openclaw/work/smartypos-mcp` | working copy running in production on this VPS | `da0f39c` on `main` | last commit 2026-11-18 |
| systemd service `smartypos-public-mcp.service` | SmartyPOS public informational MCP server | `da0f39c` | service active (running) since 2026-11-18 |
| nginx `mcp.smartypos.us` | reverse proxy to this repo's service | `da0f39c` | https; public domain |

## Milestone log

### 2026-11-18
- **Status page created.** The table above is refreshed daily by `status-sync` (06:40 ET); milestones are added with `status-log`. Rule: every important step gets a line here.
- Seeded from the git history of `main` (last 90 days; sparse projects show their latest activity) and the server's reports.
- SmartyPOS public read-only MCP server (Syrve / iiko USA)

## In progress (2026-11-18)
- (nothing recorded yet - edit this section, or tell the session working on the project)
