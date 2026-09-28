import asyncio
import os
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("/Users/sangineedikushal/Documents/Hackathon 3.o/docs/videos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/Users/sangineedikushal/.gemini/antigravity-ide/brain/00eb3fe2-5e94-4cc4-9cb0-ecd68369d9bb")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

TEMP_VIDEO_DIR = Path("/Users/sangineedikushal/Documents/Hackathon 3.o/docs/videos/temp_rec")
TEMP_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

async def record_demo():
    print("🎬 Starting NEXUS Video Recording via Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(TEMP_VIDEO_DIR),
            record_video_size={"width": 1920, "height": 1080}
        )
        
        page = await context.new_page()
        video_handle = page.video

        print("1. Opening NEXUS Cockpit (1080p)...")
        await page.goto("http://localhost:8000/", wait_until="networkidle")
        await asyncio.sleep(3)

        # 2. Open 30s Deal Briefing
        print("2. Opening 30-Second Pre-Meeting Deal Briefing...")
        await page.click("#btn-open-briefing-modal")
        await asyncio.sleep(4)
        await page.click("#close-modal-briefing")
        await asyncio.sleep(1.5)

        # 3. Open LOKI Workspace & Query
        print("3. Demonstrating LOKI AI Copilot Workspace...")
        await page.click("#btn-header-toggle-loki")
        await asyncio.sleep(1.5)
        await page.fill("#loki-user-input", "Why is this deal at risk?")
        await page.click("#loki-send-btn")
        await asyncio.sleep(4) # Let viewer see Answer, Why, Evidence
        await page.click("#loki-btn-close-panel")
        await asyncio.sleep(1.5)

        # 4. Open LOKI Connect Causal Graph
        print("4. Opening LOKI CONNECT Causal Flow Graph...")
        await page.click("#btn-header-loki-connect")
        await asyncio.sleep(2.5)
        
        nodes = await page.query_selector_all(".loki-chain-node")
        if len(nodes) >= 5:
            await nodes[1].click()
            await asyncio.sleep(2)
            await nodes[4].click()
            await asyncio.sleep(2)
        
        await page.click("#close-modal-loki-connect")
        await asyncio.sleep(1.5)

        # 5. Open DEAL X-RAY
        print("5. Opening DEAL X-RAY 18-Dimension Diagnostic...")
        await page.click("#btn-header-deal-xray")
        await asyncio.sleep(4)
        await page.click("#close-modal-deal-xray")
        await asyncio.sleep(1.5)

        # 6. Start Live Demo Call
        print("6. Launching Real-Time Live Sales Call Simulation...")
        await page.click("#btn-run-live-demo-stream")
        
        # Dialogue streams turn by turn (approx 16-18s)
        # Turn 1: Discovery
        # Turn 2: December deadline detected
        # Turn 3: Competitor X pricing objection detected + Deal #1024 citation
        # Turn 4: Suggested TCO reframe
        # Turn 5: 24/7 Support SLA detected
        # Turn 6: Commitment locked
        # Turn 7: Auto-summary modal opens
        print("   Streaming dialogue, audio wave, and real-time objection coaching...")
        await asyncio.sleep(18)

        # 7. Approve Meeting Summary Modal
        print("7. Approving Post-Meeting Summary to Persistent Deal Memory...")
        try:
            await page.wait_for_selector("#btn-approve-summary-commit", state="visible", timeout=8000)
            await asyncio.sleep(2)
            await page.click("#btn-approve-summary-commit")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"   Summary click note: {e}")
        
        # Ensure modal overlay is closed
        await page.evaluate("() => { const m = document.getElementById('modal-post-meeting-summary'); if(m) m.style.display = 'none'; }")
        await asyncio.sleep(1)

        # 8. Check Tasks Tab
        print("8. Inspecting Follow-up Tasks created by LOKI...")
        await page.click('.nav-tab[data-tab="tasks"]')
        await asyncio.sleep(3)

        # 9. Check Deals Pipeline Kanban
        print("9. Inspecting Deals Pipeline Kanban...")
        await page.click('.nav-tab[data-tab="deals"]')
        await asyncio.sleep(3)

        # 10. Return to Live Cockpit for final scene
        print("10. Returning to Live Call Cockpit...")
        await page.click('.nav-tab[data-tab="live-call"]')
        await asyncio.sleep(3)

        print("Finalizing recording and flushing video...")
        await context.close()
        await browser.close()

        video_path = await video_handle.path()
        print(f"Raw Playwright video created at: {video_path}")

        final_dest = OUTPUT_DIR / "nexus_demo_walkthrough.webm"
        artifact_dest = ARTIFACT_DIR / "nexus_demo_walkthrough.webm"
        
        shutil.copy(video_path, final_dest)
        shutil.copy(video_path, artifact_dest)
        print(f"🎉 Video successfully recorded and saved to: {final_dest}")
        print(f"🎉 Artifact copy saved to: {artifact_dest}")

if __name__ == "__main__":
    asyncio.run(record_demo())
