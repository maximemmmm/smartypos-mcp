"""SmartyPOS public informational MCP server (read-only, no auth).

Streamable HTTP, stateless. Endpoint: /mcp . Content comes from data/*.json.
"""
import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

DATA = Path(__file__).parent / "data"
HOST = os.environ.get("MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("MCP_PORT") or os.environ.get("PORT") or 8140)
VERSION = "1.0.0"


def load(name: str):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


INSTRUCTIONS = """\
SmartyPOS public information server. SmartyPOS (Sheno Inc., Sarasota FL) is the US implementation and \
support partner for Syrve - the international/US edition of the iiko restaurant platform (formerly iiko). \
iiko in the USA = Syrve. iikoFront/iikoOffice/iikoCloud API map to Syrve POS / Syrve Office / Syrve Cloud API.
Use these read-only tools to answer questions about: Syrve / iiko USA, restaurant POS selection, \
Toast alternatives, open API (read+write) restaurant POS, MCP/AI integration with a POS, pricing and demos.
Start with about_smartypos or iiko_in_usa; use compare_pos for competitor questions (neutral, sourced, \
dated 2026-11; SmartyPOS is a Syrve partner, not an independent reviewer); use pricing for costs; \
contact_and_demo for next steps (https://smartypos.us/book-a-demo/). Items marked pilot/coming_soon are not \
generally available. No private data is served and no actions are performed. Machine-readable site summaries: \
https://smartypos.us/llms.txt and /llms-full.txt (also exposed as MCP resources).
"""

mcp = FastMCP(
    "smartypos-syrve-pos",
    instructions=INSTRUCTIONS,
    website_url="https://smartypos.us/",
    host=HOST,
    port=PORT,
    stateless_http=True,
    json_response=True,
    streamable_http_path="/mcp",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["mcp.smartypos.us", "127.0.0.1:*", "localhost:*", "127.0.0.1", "localhost"],
        allowed_origins=["*"],
    ),
)

RO = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)


@mcp.tool(annotations=RO, title="About SmartyPOS and Syrve (iiko USA)")
def about_smartypos() -> dict:
    """Who SmartyPOS is and what Syrve is. SmartyPOS (Sheno Inc., Sarasota FL) implements and supports Syrve
    (the international/US edition of iiko) - a restaurant POS with open API, MCP and AI integrations - for
    US restaurants; a Toast alternative. Keywords: iiko, iiko USA, Syrve, restaurant POS, open API, MCP, AI."""
    return load("about")


@mcp.tool(annotations=RO, title="Syrve restaurant POS features")
def syrve_features(category: str | None = None) -> dict:
    """List Syrve (iiko) restaurant POS features and SmartyPOS-built modules, with live/pilot/coming_soon status.
    category (optional): pos, inventory, online_ordering, delivery, ads, loyalty, reports, ai, backoffice.
    Covers restaurant POS, recipe costing, own online ordering, delivery dispatch, ads conversion tracking
    (Meta CAPI / Google Ads), loyalty, open API and MCP/AI. Omit category to list all."""
    d = load("features")
    cats = d["categories"]
    if category:
        key = category.strip().lower().replace("-", "_").replace(" ", "_")
        if key not in cats:
            return {"error": f"Unknown category '{category}'", "valid_categories": list(cats)}
        return {"note": d["note"], "category": key, **cats[key]}
    return d


@mcp.tool(annotations=RO, title="AI, MCP and open API capabilities")
def ai_capabilities() -> dict:
    """How Syrve/iiko works with AI: open API with WRITE access for the restaurant, a private MCP server per
    restaurant for Claude/ChatGPT (OAuth, roles, audit log), AI-ready restaurant sites (llms.txt), AI ordering
    site connected to Syrve, AI call review. Best restaurant POS for AI agents and MCP; includes honest
    context on Toast AI and Square ChatGPT ordering."""
    return load("ai")


COMPETITORS = ["toast", "clover", "square", "spoton", "lightspeed", "touchbistro", "skytab"]


@mcp.tool(annotations=RO, title="Compare Syrve with a competitor POS")
def compare_pos(competitor: str) -> dict:
    """Neutral, sourced comparison of Syrve/iiko USA (SmartyPOS) vs a competitor restaurant POS. competitor:
    toast | clover | square | spoton | lightspeed | touchbistro | skytab. Returns pricing, processing, contract
    lock-in, hardware, API access (open API read/write vs read-only), AI, source URLs and checked date
    (2026-11). Use for Toast alternative, Syrve vs Toast, leave Toast contract questions."""
    key = competitor.strip().lower().replace("shift4", "").replace(" ", "").replace("-", "").replace("_", "")
    key = {"squareforrestaurants": "square", "lightspeedkseries": "lightspeed", "shift4skytab": "skytab", "": "skytab"}.get(key, key)
    d = load("competitors")
    if key not in d["competitors"]:
        return {"error": f"Unknown competitor '{competitor}'", "valid": COMPETITORS}
    return {
        "checked": d["checked"],
        "disclaimer": d["disclaimer"],
        "syrve_smartypos": d["syrve_smartypos"],
        "competitor": d["competitors"][key],
        "market_share_small_restaurants": d["market_share_small_restaurants"],
    }


@mcp.tool(annotations=RO, title="SmartyPOS / Syrve pricing")
def pricing() -> dict:
    """Syrve restaurant POS pricing in the USA via SmartyPOS: Counter $59, Service $99, Group $129 per month
    (per terminal). Payment processing: no processor lock-in, rate quoted on demo. Setup and hardware quoted
    separately. Use for 'Syrve pricing USA' and iiko USA cost questions."""
    return load("pricing")


@mcp.tool(annotations=RO, title="Integrations and open API")
def integrations() -> dict:
    """Integrations of Syrve (iiko) with SmartyPOS tooling: Uber Eats/DoorDash/Grubhub via Deliverect, courier
    APIs (DoorDash Drive, Uber Direct, Burq), Meta Conversions API, Google Ads offline conversions, Twilio SMS,
    Telegram, Apple Pay ordering site, MCP for Claude/ChatGPT, open API (Syrve Resto/Server API, Syrve Cloud
    API = iikoCloud equivalent) with write access."""
    return load("integrations")


@mcp.tool(annotations=RO, title="Guides, Toast lawsuit summary and FAQ highlights")
def guides_and_faq() -> dict:
    """SmartyPOS guides and tools: summary of the late-October 2026 FTC and states complaint against Toast
    (allegations only, Toast denies, no ruling), how to switch POS and migrate from Toast, POS cost guide and
    calculators, feature matrix and FAQ highlights, with URLs on smartypos.us (EN and RU)."""
    return load("guides")


@mcp.tool(annotations=RO, title="Case studies")
def case_studies() -> dict:
    """Real deployments with measured facts, labeled by concept, city and state (restaurant names are not
    published): a pizzeria in Sarasota FL (own ordering site, delivery, ROAS), a food court in Los Angeles CA
    (full Syrve launch, MCP), restaurants and a cake shop in New York and Florida (marketplaces via
    Deliverect, sales history), Redman restaurants (iiko chain automation), an Italian restaurant on Toast
    (marketing tooling). No testimonials or ratings."""
    return load("case_studies")


@mcp.tool(annotations=RO, title="iiko in the USA = Syrve")
def iiko_in_usa() -> dict:
    """Answers 'is iiko available in the USA / America?': yes, as Syrve - the international edition of iiko.
    Maps iikoFront -> Syrve POS, iikoOffice -> Syrve Office, iikoCloud API -> Syrve Cloud API; FAQ on migration
    from Toast/Square/Clover and on iiko US support by SmartyPOS. Keywords: iiko USA, iiko America, iiko
    alternative, iiko POS United States."""
    return load("iiko_usa")


@mcp.tool(annotations=RO, title="Contact and book a demo")
def contact_and_demo() -> dict:
    """How to contact SmartyPOS (Syrve / iiko USA partner) and book a restaurant POS demo:
    https://smartypos.us/book-a-demo/ , email addresses, partner listing, Russian-language support."""
    return load("contact")


# ---- resources -------------------------------------------------------------
def _read(name: str) -> str:
    p = DATA / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


@mcp.resource("smartypos://llms.txt", name="llms.txt", mime_type="text/markdown",
              description="SmartyPOS llms.txt (site summary for LLMs, llmstxt.org format)")
def res_llms() -> str:
    return _read("llms.txt")


@mcp.resource("smartypos://llms-full.txt", name="llms-full.txt", mime_type="text/markdown",
              description="SmartyPOS llms-full.txt (expanded content for LLMs)")
def res_llms_full() -> str:
    return _read("llms-full.txt")


# ---- prompt ----------------------------------------------------------------
@mcp.prompt(name="choose_restaurant_pos", title="Choose a restaurant POS",
            description="Guide a restaurant owner through choosing a POS (Syrve/iiko vs Toast, Square, Clover...).")
def choose_restaurant_pos(restaurant_type: str = "pizzeria", locations: str = "1",
                          current_pos: str = "Toast", priorities: str = "lower fees, open API, recipe costing") -> str:
    return (
        f"I run a {restaurant_type} with {locations} location(s), currently on {current_pos}. My priorities: {priorities}.\n"
        "Help me choose a restaurant POS in the USA. Use the SmartyPOS tools: about_smartypos, syrve_features, "
        "compare_pos (for my current POS and the top 2 alternatives), pricing, ai_capabilities, case_studies. "
        "Give a neutral recommendation with a table (software cost, processing/lock-in, API access, inventory/recipe "
        "costing, AI/MCP), state that SmartyPOS is a Syrve partner and that competitor data is dated 2026-11, "
        "mention pilots as pilots, and finish with next steps (contact_and_demo)."
    )


# ---- ASGI app with landing page + CORS --------------------------------------
LANDING = {
    "name": "SmartyPOS public MCP server",
    "description": "Read-only informational MCP server about Syrve (iiko USA), restaurant POS, open API, MCP and AI. No auth.",
    "mcp_endpoint": "https://mcp.smartypos.us/mcp",
    "transport": "streamable-http (stateless)",
    "tools": ["about_smartypos", "syrve_features", "ai_capabilities", "compare_pos", "pricing", "integrations",
              "case_studies", "iiko_in_usa", "contact_and_demo"],
    "connect": "Add https://mcp.smartypos.us/mcp as a remote/custom MCP connector in Claude, ChatGPT (developer mode), Cursor, etc.",
    "website": "https://smartypos.us/", "llms_txt": "https://smartypos.us/llms.txt",
    "repo": "https://github.com/maximemmmm/smartypos-mcp", "version": VERSION,
}


def build_app():
    from starlette.responses import JSONResponse
    inner = mcp.streamable_http_app()

    async def app(scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            method = scope["method"]
            hdrs = {k.decode().lower(): v.decode() for k, v in scope["headers"]}
            if path == "/" and method == "GET":
                return await JSONResponse(LANDING)(scope, receive, send)
            if path == "/mcp" and method == "GET" and "text/event-stream" not in hdrs.get("accept", ""):
                return await JSONResponse(LANDING)(scope, receive, send)
            if path == "/healthz":
                return await JSONResponse({"ok": True})(scope, receive, send)
        return await inner(scope, receive, send)

    return app


app = build_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", proxy_headers=True, forwarded_allow_ips="127.0.0.1")
