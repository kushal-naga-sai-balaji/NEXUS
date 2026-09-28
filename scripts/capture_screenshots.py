import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("/Users/sangineedikushal/.gemini/antigravity-ide/brain/00eb3fe2-5e94-4cc4-9cb0-ecd68369d9bb")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def capture_all():
    print("Launching Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print("Navigating to http://localhost:8000/...")
        await page.goto("http://localhost:8000/", wait_until="networkidle")
        await asyncio.sleep(2)

        # 1. Capture Main 3-Panel Cockpit
        print("1. Capturing Live Call Cockpit...")
        cockpit_path = OUTPUT_DIR / "nexus_01_live_cockpit.png"
        await page.screenshot(path=str(cockpit_path))
        print(f"   Saved: {cockpit_path}")

        # 2. Trigger 30s Briefing Modal
        print("2. Capturing 30s Deal Briefing Modal...")
        await page.click("#btn-open-briefing-modal")
        await asyncio.sleep(1)
        briefing_path = OUTPUT_DIR / "nexus_02_30s_briefing.png"
        await page.screenshot(path=str(briefing_path))
        print(f"   Saved: {briefing_path}")
        await page.click("#close-modal-briefing")
        await asyncio.sleep(0.5)

        # 3. Trigger LOKI Assistant
        print("3. Capturing LOKI AI Copilot Workspace...")
        await page.click("#loki-launcher-btn")
        await asyncio.sleep(1)
        # Type a query to show LOKI's pin-to-pin report
        await page.fill("#loki-user-input", "Tell me everything about this deal")
        await page.click("#loki-send-btn")
        await asyncio.sleep(2)
        loki_path = OUTPUT_DIR / "nexus_03_loki_workspace.png"
        await page.screenshot(path=str(loki_path))
        print(f"   Saved: {loki_path}")

        # 4. Trigger LOKI CONNECT Modal
        print("4. Capturing LOKI CONNECT Flow Graph...")
        await page.click("#loki-btn-loki-connect")
        await asyncio.sleep(1.5)
        connect_path = OUTPUT_DIR / "nexus_04_loki_connect.png"
        await page.screenshot(path=str(connect_path))
        print(f"   Saved: {connect_path}")
        await page.click("#close-modal-loki-connect")
        await asyncio.sleep(0.5)

        # 5. Trigger DEAL X-RAY Modal
        print("5. Capturing DEAL X-RAY (18 Dimensions)...")
        await page.click("#btn-header-deal-xray")
        await asyncio.sleep(1.5)
        xray_path = OUTPUT_DIR / "nexus_05_deal_xray.png"
        await page.screenshot(path=str(xray_path))
        print(f"   Saved: {xray_path}")
        await page.click("#close-modal-deal-xray")
        await asyncio.sleep(0.5)

        # 6. Capture Deals Pipeline
        print("6. Capturing Deals Pipeline View...")
        await page.click('.nav-tab[data-tab="deals"]')
        await asyncio.sleep(1)
        pipeline_path = OUTPUT_DIR / "nexus_06_deals_pipeline.png"
        await page.screenshot(path=str(pipeline_path))
        print(f"   Saved: {pipeline_path}")

        # 7. Start Live Demo and capture mid-stream
        print("7. Capturing Live Demo with Real-Time Alerts...")
        await page.click('.nav-tab[data-tab="live-call"]')
        await asyncio.sleep(0.5)
        await page.click("#btn-run-live-demo-stream")
        await asyncio.sleep(6) # wait for dialogue turns and alerts to populate
        stream_path = OUTPUT_DIR / "nexus_07_live_stream_alerts.png"
        await page.screenshot(path=str(stream_path))
        print(f"   Saved: {stream_path}")

        await browser.close()
        print("\nAll 7 screenshots captured successfully!")

if __name__ == "__main__":
    asyncio.run(capture_all())
