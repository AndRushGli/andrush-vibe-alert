from playwright.sync_api import sync_playwright
import requests
import re

URL = "https://vibefestival.ro/hu/jegyek"

BOT_TOKEN = "8758488011:AAHXlneA-wFV7aN_2r3T7Gmiv2VdMjx7yqU"
CHAT_ID = "7183147881"

SELECTOR = "#product-card-715 strong"


def notify(price):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": f"🚨 VIBE PASS olcsóbb lett: {price} RON (+ kezelési költség)\nhttps://vibefestival.ro/hu/jegyek"
        }
    )


def extract_price(text):
    # kiveszi az első 3 számjegyet (499, 250, stb.)
    match = re.search(r"\d{2,3}", text)
    if match:
        return int(match.group())
    return None


def check_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)
        page.wait_for_timeout(8000)

        price_text = page.locator(SELECTOR).inner_text()
        print("RAW:", price_text)

        browser.close()

        price = extract_price(price_text)

        if price:
            print("PARSED PRICE:", price)

            if price < 600:
                notify(price)


check_price()
