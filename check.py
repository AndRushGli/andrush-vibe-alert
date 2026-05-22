from playwright.sync_api import sync_playwright
import requests
import re
import time
import os

URL = "https://vibefestival.ro/hu/jegyek"

BOT_TOKEN = "8758488011:AAHXlneA-wFV7aN_2r3T7Gmiv2VdMjx7yqU"
CHAT_ID = "7183147881"

SELECTOR = "#product-card-715 strong"

def notify(price):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": f"🚨 VIBE PASS OLCSÓBB: {price} RON\n{URL}"
        }
    )

def extract_price(text):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None

def check_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)
        page.wait_for_timeout(8000)

        text = page.locator(SELECTOR).inner_text()
        print("RAW:", text)

        price = extract_price(text)

        if price and price < 300:
            notify(price)

        browser.close()


# 🔥 FOREVER LOOP (EZ A RENDER LÉNYEG)
while True:
    try:
        check_price()
    except Exception as e:
        print("ERROR:", e)

    time.sleep(60)  # 1 perc
