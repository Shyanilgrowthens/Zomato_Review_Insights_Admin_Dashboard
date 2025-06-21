from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

# Setup headless browser
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
url = 'https://www.zomato.com/kolkata/cal-on-ballygunge/reviews'
driver.get(url)

# Wait for reviews to appear
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "p[class*='sc-'][class*='hreYiP']"))
)

all_reviews = []

for page in range(1, 20):
    print(f"\n🔄 Scraping page {page}...")
    time.sleep(3)

    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Get review blocks (metadata: name, rating, time)
    review_blocks = soup.find_all("div", class_="sc-dgAbBl ceFzZe")
    
    # Get all review texts separately (second logic)
    review_text_tags = soup.select("p[class*='sc-'][class*='hreYiP']")

    if not review_blocks or not review_text_tags:
        print("⚠ No reviews or review texts found. Ending.")
        break

    print(f"✅ Found {len(review_blocks)} reviews on page {page}")

    for i in range(min(len(review_blocks), len(review_text_tags))):  # Ensure sync
        block = review_blocks[i]
        review_text_tag = review_text_tags[i]

        try:
            # Review text from 2nd code logic
            review_text = review_text_tag.get_text(strip=True) if review_text_tag else "N/A"

            # Rating
            rating_tag = block.find("div", class_="sc-1q7bklc-1 cILgox")
            rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

            # Time ago
            time_tag = block.find("p", class_="sc-1hez2tp-0 fKvqMN time-stamp")
            time_ago = time_tag.get_text(strip=True) if time_tag else "N/A"

            # Reviewer name
            reviewer_name_tag = block.find_previous("p", class_="sc-1hez2tp-0 sc-lenlpJ dCAQIv")
            reviewer_name = reviewer_name_tag.get_text(strip=True) if reviewer_name_tag else "N/A"

            review_data = {
                "reviewer": reviewer_name,
                "rating": rating,
                "time_ago": time_ago,
                "review_text": review_text
            }

            all_reviews.append(review_data)

            print("-" * 80)
            print(f"👤 Reviewer: {reviewer_name}")
            print(f"⭐ Rating: {rating}")
            print(f"🕒 Time Ago: {time_ago}")
            print(f"💬 Review: {review_text}")

        except Exception as e:
            print(f"⚠ Error parsing review #{i + 1}: {e}")

    # Try to go to next page
    try:
        next_btn = driver.find_elements(By.CSS_SELECTOR, "a.sc-hWWTYC.sc-eOnLuU.sc-igaqVs.hQyaKa")
        if next_btn:
            driver.execute_script("arguments[0].click();", next_btn[-1])
            print("➡ Clicked to next page.")
        else:
            print("🚫 No next button found.")
            break
    except Exception as e:
        print(f"🚫 Pagination error: {e}")
        break

driver.quit()

# Save to JSON
with open("zomato_reviews.json", "w", encoding="utf-8") as f:
    json.dump(all_reviews, f, ensure_ascii=False, indent=2)

print("\n✅ Scraping complete.")
print(f"Total reviews scraped: {len(all_reviews)}")