from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager  # <-- FIXED
from selenium.webdriver.chrome.service import Service
import time

# ---------- APNI SETTINGS YAHAN CHANGE KARO ----------
REACTION_TYPE = "Love"   # "Like", "Love", "Care", "Haha", "Wow", "Sad"
COMMENT_TEXT = "Awesome post! 🔥"   # Comment text (empty karo toh sirf reaction)
DELAY_BETWEEN_POSTS = 20   # Seconds (20 se kam mat rakho)
# -----------------------------------------------------

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

print("🚀 Facebook khol raha hoon...")
driver.get("https://facebook.com")

input("👉 Ab browser mein apna email/password daal kar login karo, phir yahan ENTER daba do...")

print("✅ Login ho gaya! Feed par reaction aur comment dal raha hoon...")
driver.get("https://facebook.com")

post_count = 0
while True:
    try:
        posts = driver.find_elements(By.XPATH, "//div[@role='article']")
        for post in posts:
            post_count += 1
            print(f"\n📌 Post #{post_count} process ho raha hai...")
            try:
                like_btn = post.find_element(By.XPATH, ".//div[@aria-label='Like' and @role='button']")
                if like_btn:
                    actions = ActionChains(driver)
                    actions.move_to_element(like_btn).perform()
                    time.sleep(1)
                    
                    if REACTION_TYPE != "Like":
                        reaction_emoji = driver.find_element(By.XPATH, f"//div[@aria-label='{REACTION_TYPE}']")
                        reaction_emoji.click()
                        print(f"   ✅ {REACTION_TYPE} reaction diya.")
                    else:
                        like_btn.click()
                        print("   ✅ Like kiya.")
                
                time.sleep(2)
                
                if COMMENT_TEXT.strip() != "":
                    try:
                        comment_box = post.find_element(By.XPATH, ".//div[@aria-label='Write a comment…' or @aria-label='Write a comment...']")
                        comment_box.click()
                        time.sleep(0.5)
                        comment_box.send_keys(COMMENT_TEXT)
                        time.sleep(0.5)
                        post_comment_btn = post.find_element(By.XPATH, ".//div[@aria-label='Comment' and @role='button']")
                        post_comment_btn.click()
                        print(f"   💬 Comment likha: '{COMMENT_TEXT}'")
                    except Exception as e:
                        print(f"   ⚠️ Comment skip: {str(e)[:40]}")
            
            except Exception as e:
                print(f"   ⚠️ Skip (already reacted): {str(e)[:40]}")
            
            time.sleep(DELAY_BETWEEN_POSTS)
        
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(5)
        print("\n⬇️ Next posts ke liye scroll kar raha hoon...")
        
    except KeyboardInterrupt:
        print("\n🛑 Bot band kiya.")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(10)
