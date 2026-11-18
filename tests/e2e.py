"""End-to-end check against the live endpoint: python tests/e2e.py [url]"""
import asyncio, sys, json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = sys.argv[1] if len(sys.argv) > 1 else "https://mcp.smartypos.us/mcp"

async def main():
    async with streamablehttp_client(URL) as (r, w, _):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            print("initialize:", init.serverInfo.name, "| instructions:", len(init.instructions or ""), "chars")
            tools = (await s.list_tools()).tools
            print("tools:", [t.name for t in tools])
            assert all(t.annotations and t.annotations.readOnlyHint for t in tools)
            calls = [("about_smartypos", {}), ("syrve_features", {}), ("syrve_features", {"category": "ai"}),
                     ("syrve_features", {"category": "bogus"}), ("ai_capabilities", {}), ("pricing", {}),
                     ("integrations", {}), ("case_studies", {}), ("iiko_in_usa", {}), ("contact_and_demo", {})]
            calls += [("compare_pos", {"competitor": c}) for c in
                      ["toast", "clover", "square", "spoton", "lightspeed", "touchbistro", "skytab", "Shift4 SkyTab", "nope"]]
            for name, args in calls:
                res = await s.call_tool(name, args)
                txt = res.content[0].text
                assert not res.isError, (name, txt)
                print(f"  {name}{args}: {len(txt)} chars, ok")
            print("resources:", [str(x.uri) for x in (await s.list_resources()).resources])
            for u in ["smartypos://llms.txt", "smartypos://llms-full.txt"]:
                c = (await s.read_resource(u)).contents[0].text
                print("  ", u, len(c), "chars")
            print("prompts:", [p.name for p in (await s.list_prompts()).prompts])
            p = await s.get_prompt("choose_restaurant_pos", {"restaurant_type": "pizzeria"})
            print("  prompt ok:", p.messages[0].content.text[:60])
asyncio.run(main())
