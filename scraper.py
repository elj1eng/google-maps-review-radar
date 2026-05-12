import time
import re
import os
import shutil
from playwright.sync_api import sync_playwright
from constants import CSS_SELECTORS, BROWSER_CONFIG

class MapsScraper:
    def __init__(self, url):
        self.url = url
        self.profile_path = os.path.join(os.getcwd(), "temp_profile")

    def fetch_html(self):
        if os.path.exists(self.profile_path): 
            shutil.rmtree(self.profile_path)

        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                self.profile_path, 
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                viewport=BROWSER_CONFIG["VIEWPORT"]
            )
            page = context.pages[0]
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 1. Navigate & Initial Load
            page.goto(self.url, wait_until="domcontentloaded")
            page.wait_for_selector(CSS_SELECTORS["BUSINESS_TITLE"], timeout=BROWSER_CONFIG["TIMEOUT"])
            time.sleep(1)
            page.reload(wait_until="domcontentloaded")
            
            # 2. Open Reviews
            trigger = page.locator(CSS_SELECTORS["REVIEWS_TAB"]).first
            trigger.wait_for(state="visible")
            trigger.click(force=True)
            time.sleep(2)

            # 3. Sort by Newest
            try:
                page.locator(CSS_SELECTORS["SORT_BUTTON"]).filter(has_text="Sort").click(force=True)
                page.locator(CSS_SELECTORS["NEWEST_OPTION"]).filter(has_text="Newest").click(force=True)
                # Wait for the menu to close to confirm click
                page.locator(CSS_SELECTORS["NEWEST_OPTION"]).filter(has_text="Newest").wait_for(state="hidden")
                time.sleep(2)
            except Exception as e:
                print(f"Sort Warning: {e}")

            # 4. Dynamic Scroll
            pane = page.locator(CSS_SELECTORS["SCROLL_PANE"]).first
            pane.focus()
            
            print("Scrolling review list dynamically...")
            for i in range(BROWSER_CONFIG["SCROLL_LIMIT"]):
                prev_count = page.locator(f".{CSS_SELECTORS['REVIEW_CARD']}").count()
                page.keyboard.press("End")
                
                try:
                    # Wait until card count increases rather than using static sleep
                    page.wait_for_function(
                        f"document.querySelectorAll('.{CSS_SELECTORS['REVIEW_CARD']}').length > {prev_count}",
                        timeout=BROWSER_CONFIG["DYNAMIC_WAIT_MS"]
                    )
                except:
                    break # Reached bottom or load failed

            html = page.content()
            context.close()
            shutil.rmtree(self.profile_path, ignore_errors=True)
            return html