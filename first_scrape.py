from playwright.sync_api import sync_playwright
import time
import csv

def scrape_brand_page(url, min_products=30):
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # ---------- STEP 1: INFINITE SCROLL ----------
        prev_count = 0
        for scroll_index in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

            curr_count = page.locator("li.product-base").count()
            if curr_count >= min_products or curr_count == prev_count:
                break
            prev_count = curr_count

        # ---------- STEP 2: EXTRACT DATA ----------
        cards = page.locator("li.product-base")

        for i in range(min(cards.count(), min_products)):
            card = cards.nth(i)

            brand = card.locator("h3.product-brand").inner_text()
            product_name = card.locator("h4.product-product").inner_text()
            selling_price = card.locator(
                "span.product-discountedPrice"
            ).inner_text()

            try:
                mrp_price = card.locator("span.product-strike").inner_text()
            except:
                mrp_price = None

            try:
                discount = card.locator(
                    "span.product-discountPercentage"
                ).inner_text()
            except:
                discount = None

             # ---------- IMAGE URL (LAZY LOADING) ----------
            image_url = None
            image_elements = card.locator("img")

            if image_elements.count() > 0:
                image_url = image_elements.first.get_attribute("src") or \
                            image_elements.first.get_attribute("data-src")

            # ---------- PRODUCT ID ----------
            product_link = card.locator("a").first.get_attribute("href")
            product_id = None
            if product_link:
                parts = product_link.split("/")
                for part in parts:
                    if part.isdigit():
                        product_id = part
                        break

            products.append({
                "product_id": product_id,
                "brand": brand,
                "product_name": product_name,
                "image_url": image_url,
                "selling_price": selling_price,
                "mrp_price": mrp_price,
                "discount": discount,
                "source_page": "brand"
            })

        browser.close()

    with open("myntra_levis.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)

scrape_brand_page("https://www.myntra.com/levis")

