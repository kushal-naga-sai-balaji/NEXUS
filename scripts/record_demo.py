import asyncio
import os
import sys
from pathlib import Path

# Ensure custom browser path is set
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(Path(__file__).parent.parent / ".browsers")

from playwright.async_api import async_playwright

async def record_demo_video():
    video_dir = Path(__file__).parent.parent / "frontend" / "demo_videos"
    video_dir.mkdir(parents=True, exist_ok=True)

    chrome_binary = Path(__file__).parent.parent / ".browsers" / "chromium-1243" / "chrome-mac-arm64" / "Google Chrome for Testing.app" / "Contents" / "MacOS" / "Google Chrome for Testing"

    print(f"🚀 Starting Playwright Chromium with binary: {chrome_binary}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=str(chrome_binary) if chrome_binary.exists() else None
        )
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1400, "height": 900}
        )

        page = await context.new_page()

        print("Navigating to http://localhost:8000 ...")
        await page.goto("http://localhost:8000", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # 1. Show Deal Cockpit
        print("Scene 1: Deal Cockpit & Buying Committee...")
        await page.wait_for_selector("#cockpit-deal-header")
        await page.wait_for_timeout(2500)

        # 2. Click Agent Learning Curve
        print("Scene 2: Agent Learning Curve...")
        await page.click("#tab-btn-learning")
        await page.wait_for_timeout(1500)

        # Click through learning curve stages
        for stage in range(1, 5):
            stage_btn = page.locator(f".stage-step-card >> nth={stage - 1}")
            if await stage_btn.count() > 0:
                await stage_btn.click()
                await page.wait_for_timeout(1500)

        # 3. Click Live Objection Coach
        print("Scene 3: Live Objection Coach...")
        await page.click("#tab-btn-coaching")
        await page.wait_for_timeout(1500)

        # Click the CFO Datadog 32% discount preset
        preset = page.locator(".preset-chip >> nth=0")
        if await preset.count() > 0:
            await preset.click()
            await page.wait_for_timeout(3000)

        # 4. Click Pre-Call Tactical Briefing
        print("Scene 4: Pre-Call Tactical Briefing...")
        await page.click("#tab-btn-briefing")
        await page.wait_for_timeout(1500)
        await page.click("#btn-generate-briefing")
        await page.wait_for_timeout(3500)

        # 5. Click Hindsight Memory Bank
        print("Scene 5: Hindsight Memory Bank (4 Biomimetic Tiers)...")
        await page.click("#tab-btn-memory")
        await page.wait_for_timeout(2000)

        # Click Opinion tier filter
        opinion_filter = page.locator(".tier-tab-btn.purple")
        if await opinion_filter.count() > 0:
            await opinion_filter.click()
            await page.wait_for_timeout(2000)

        # 6. Click Memory Contrast Mode
        print("Scene 6: Memory Contrast Mode (Judges Choice)...")
        await page.click("#tab-btn-contrast")
        await page.wait_for_timeout(3000)

        # 7. Click Deal Evidence & Artifacts
        print("Scene 7: Deal Evidence & Artifacts...")
        await page.click("#tab-btn-artifacts")
        await page.wait_for_timeout(2000)

        quote_tab = page.locator(".artifact-tab-btn >> nth=1")
        if await quote_tab.count() > 0:
            await quote_tab.click()
            await page.wait_for_timeout(2500)

        # Finish video recording
        print("Saving video recording...")
        video_path = await page.video.path()
        await context.close()
        await browser.close()

        # Rename to a user-friendly name
        target_video = video_dir / "nexus_agent_demo.webm"
        if os.path.exists(video_path):
            if os.path.exists(target_video):
                os.remove(target_video)
            os.rename(video_path, target_video)
            print(f"✅ Demo Video successfully recorded and saved to: {target_video}")
            return str(target_video)
        return video_path

if __name__ == "__main__":
    asyncio.run(record_demo_video())
