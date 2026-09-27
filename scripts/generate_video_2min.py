import asyncio
import os
import shutil
import sys
import time
from pathlib import Path
from playwright.async_api import async_playwright

async def safe_hover(page, selector, timeout=4000):
    try:
        loc = page.locator(selector)
        if await loc.count() > 0:
            await loc.first.hover(timeout=timeout)
            return True
    except Exception as e:
        print(f"Notice: safe_hover skipped {selector}: {e}")
    return False

async def safe_click(page, selector, timeout=4000):
    try:
        loc = page.locator(selector)
        if await loc.count() > 0:
            await loc.first.click(timeout=timeout)
            return True
    except Exception as e:
        print(f"Notice: safe_click skipped {selector}: {e}")
    return False

async def generate_2min_demo_video():
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_video_dir = base_dir / "temp_video_rec"
    temp_video_dir.mkdir(parents=True, exist_ok=True)

    chrome_binary = Path("/Users/sangineedikushal/Documents/Hackathon 3.0/.browsers/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")

    print(f"🎬 Starting 2-Minute Screen Recording with Playwright Chromium (1080p)...")
    print(f"Browser binary: {chrome_binary}")

    start_time = time.time()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=str(chrome_binary) if chrome_binary.exists() else None,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(temp_video_dir),
            record_video_size={"width": 1920, "height": 1080}
        )

        page = await context.new_page()

        # ==========================================
        # PHASE 1: [0:00 - 0:25] (25s) Deal Cockpit & Account Overview
        # ==========================================
        print("▶️ [0:00 - 0:25] Phase 1: Intro & Deal Cockpit Overview...")
        await page.goto("http://localhost:8000", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Smooth hover over brand & status
        await safe_hover(page, ".logo-container")
        await page.wait_for_timeout(2000)

        # Hover over Deal Header
        await safe_hover(page, "#cockpit-deal-header")
        await page.wait_for_timeout(3500)

        # Inspect Stakeholders Heatmap (Elena Vance, Marcus Reynolds, David Sterling)
        stakeholders = page.locator(".stakeholder-card")
        st_count = await stakeholders.count()
        for i in range(min(st_count, 3)):
            await stakeholders.nth(i).hover()
            await page.wait_for_timeout(2500)

        # Hover over Competitor Threat Radar
        await safe_hover(page, "#competitor-radar-container")
        await page.wait_for_timeout(3000)

        # Smooth scroll down to timeline
        await page.evaluate("window.scrollBy({ top: 380, behavior: 'smooth' })")
        await page.wait_for_timeout(4000)
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await page.wait_for_timeout(3000)

        # ==========================================
        # PHASE 2: [0:25 - 0:50] (25s) Pre-Call Tactical Briefing
        # ==========================================
        print("▶️ [0:25 - 0:50] Phase 2: Generating Pre-Call Briefing...")
        await safe_click(page, "#tab-btn-briefing")
        await page.wait_for_timeout(2500)

        # Click Generate Tactical Briefing
        await safe_hover(page, "#btn-generate-briefing")
        await page.wait_for_timeout(1500)
        await safe_click(page, "#btn-generate-briefing")
        await page.wait_for_timeout(4500)

        # Scroll through the generated tactical dossier
        await page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
        await page.wait_for_timeout(4000)
        await page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
        await page.wait_for_timeout(4000)
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await page.wait_for_timeout(3000)

        # ==========================================
        # PHASE 3: [0:50 - 1:30] (40s) Live Objection Coach (The Star Moment!)
        # ==========================================
        print("▶️ [0:50 - 1:30] Phase 3: Live Objection Coach (CFO 32% Discount Trap)...")
        await safe_click(page, "#tab-btn-coaching")
        await page.wait_for_timeout(2500)

        # Click the CFO Datadog 32% discount preset chip
        preset = page.locator(".preset-chip >> nth=0")
        if await preset.count() > 0:
            await preset.hover()
            await page.wait_for_timeout(2000)
            await preset.click()
            await page.wait_for_timeout(2500)

        # Click Handle Objection with Hindsight
        await safe_hover(page, "#btn-submit-objection")
        await page.wait_for_timeout(1500)
        await safe_click(page, "#btn-submit-objection")
        await page.wait_for_timeout(4500)

        # Scroll to inspect response
        await page.evaluate("window.scrollBy({ top: 380, behavior: 'smooth' })")
        await page.wait_for_timeout(4000)

        # Highlight Hindsight Recalls Cited
        citations = page.locator(".recall-evidence-card")
        c_count = await citations.count()
        for i in range(min(c_count, 2)):
            await citations.nth(i).hover()
            await page.wait_for_timeout(3000)

        # Highlight Counter-Strategy
        await safe_hover(page, ".counter-strategy-box")
        await page.wait_for_timeout(4500)

        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await page.wait_for_timeout(2500)

        # ==========================================
        # PHASE 4: [1:30 - 1:50] (20s) Hindsight Memory Bank (4 Tiers)
        # ==========================================
        print("▶️ [1:30 - 1:50] Phase 4: Hindsight Memory Bank (4 Biomimetic Tiers)...")
        await safe_click(page, "#tab-btn-memory")
        await page.wait_for_timeout(2500)

        # Step through tiers: World -> Experience -> Observation -> Opinion
        tier_buttons = page.locator(".tier-tab-btn")
        t_count = await tier_buttons.count()
        for i in range(t_count):
            await tier_buttons.nth(i).click()
            await page.wait_for_timeout(2200)

        # Search for Datadog in Memory Bank
        search_input = page.locator("#memory-search-query")
        if await search_input.count() > 0:
            await search_input.fill("Datadog")
            await page.wait_for_timeout(1200)
            await safe_click(page, "#btn-search-memory")
            await page.wait_for_timeout(3500)

        # ==========================================
        # PHASE 5: [1:50 - 2:05] (15-20s) Cognitive Learning Curve & Reflection
        # ==========================================
        print("▶️ [1:50 - 2:05] Phase 5: Cognitive Learning Curve & Reflection...")
        await safe_click(page, "#tab-btn-learning")
        await page.wait_for_timeout(2500)

        # Step through the 4 stages (Day 1 Discovery to Day 60 Close)
        for stage in range(1, 5):
            stage_btn = page.locator(f".stage-step-card >> nth={stage - 1}")
            if await stage_btn.count() > 0:
                await stage_btn.hover()
                await stage_btn.click()
                await page.wait_for_timeout(2500)

        # Strategic Reflection
        await safe_click(page, "#tab-btn-reflection")
        await page.wait_for_timeout(2000)
        await safe_click(page, "#btn-trigger-reflect")
        await page.wait_for_timeout(4000)

        # Return to Cockpit for clean closing shot
        await safe_click(page, "#tab-btn-cockpit")
        await page.wait_for_timeout(3500)

        # Finish recording
        print("💾 Finalizing video file...")
        video_path = await page.video.path()
        await context.close()
        await browser.close()

    total_duration = time.time() - start_time
    print(f"⏱️ Total recording execution time: {total_duration:.1f} seconds")

    target_video = output_dir / "nexus_demo_2min.webm"
    if os.path.exists(video_path):
        if os.path.exists(target_video):
            os.remove(target_video)
        shutil.move(video_path, target_video)
        print(f"✅ 2-Minute Demo Video successfully recorded!")
        print(f"📁 Saved to: {target_video} ({os.path.getsize(target_video) / (1024*1024):.2f} MB)")

    # Clean up temp dir
    shutil.rmtree(temp_video_dir, ignore_errors=True)
    return str(target_video)

if __name__ == "__main__":
    asyncio.run(generate_2min_demo_video())
