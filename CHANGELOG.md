# Changelog: smartypos-mcp (public informational MCP server)

Times are US Eastern. Newest first.

## 2026-11-24 ET: Redman brand names removed
- What: the Redman group and its venue names are replaced by "Restaurant group (3 restaurants: bar & grill, barbecue, deli), Russia" in case_studies, ai, features, README, tool description and llms files.
- Rollback: git revert the commit, then sudo systemctl restart smartypos-public-mcp.

## 2026-11-23 ET: restaurant names removed from the public data
- What: case studies, features, AI, integrations, README, tool description and llms files now use anonymized labels (concept, city, state) with the same numbers as smartypos.us. No restaurant names, no site URLs of clients. llms files copied from the site (webroot) after its 2026-11-23 update. Case study URLs point to the new anonymous pages.
- Why: owner request, same as the site.
- Rollback: git revert the commit, then sudo systemctl restart smartypos-public-mcp.
