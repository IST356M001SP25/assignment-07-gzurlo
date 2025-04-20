import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")

    menu_items = []
    
    # Get all menu sections
    menu_sections = page.query_selector_all('h2.menu-title')
    
    for section in menu_sections:
        title = section.inner_text().strip()
        
        # Get the parent element of the section (two levels up)
        section_parent = section.evaluate('node => node.parentElement.parentElement')
        
        # Get all menu items within this section
        items = section_parent.query_selector_all('div.menu-item')
        
        for item in items:
            item_text = item.inner_text()
            try:
                menu_item = extract_menu_item(title, item_text)
                menu_items.append(menu_item.to_dict())
            except Exception as e:
                print(f"Error processing item in {title}: {e}")
                continue
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(menu_items)
    df.to_csv('cache/tullys_menu.csv', index=False)
    
    print(f"Successfully scraped {len(menu_items)} menu items")   
    context.close()
    browser.close()
with sync_playwright() as playwright:
    tullyscraper(playwright)