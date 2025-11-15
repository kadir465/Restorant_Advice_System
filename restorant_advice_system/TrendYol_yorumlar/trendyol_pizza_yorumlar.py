import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

class TrendYolPizzaYorumlar:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.url = "https://tgoyemek.com/arama?searchQuery=pizza"

    def arama_yap_ve_veri_cek(self):
        print(f"Sayfa açılıyor: {self.url}")
        self.driver.get(self.url)

        try:
            selector = "a[href^='/restoranlar/']"
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            restaurant_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Toplam {len(restaurant_elements)} restoran bulundu.")
        except Exception as e:
            print(f"Hata var: {e}")
            self.driver.quit()
            return

        urls_to_visit = []
        for element in restaurant_elements:
            link = element.get_attribute("href")
            if link and link not in urls_to_visit:
                urls_to_visit.append(link)

        print("\n--- Toplam URL ---\n")
        for url in urls_to_visit:
            print(url)

        yorumlar = []

        for url in urls_to_visit:
            try:
                print(f"\nRestoran sayfası açılıyor: {url}")
                self.driver.get(url)

                yorum_button_xpath = "/html/body/div[1]/main/div[3]/div/div[1]/div/div[2]/button[2]"
                self.wait.until(EC.element_to_be_clickable((By.XPATH, yorum_button_xpath)))
                yorum_button = self.driver.find_element(By.XPATH, yorum_button_xpath)
                if yorum_button:
                    yorum_button.click()

                    scroll_pause_time = 1
                    last_height = self.driver.execute_script("return document.body.scrollHeight")
                    while True:
                      self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                      time.sleep(scroll_pause_time)
                      new_height = self.driver.execute_script("return document.body.scrollHeight")
                      if new_height == last_height:
                        break
                      last_height = new_height

                self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")
                ))
                yorum_elements = self.driver.find_elements(By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")

                print(f"Toplam {len(yorum_elements)} tane yorum bulundu.")


                for yorum_element in yorum_elements:
     
                    yorum_text = yorum_element.text.strip()
                    yorumlar.append(yorum_text)
                    print("- Yorum-")
                    print(yorum_text)
                else:
                    print("yorumu yok")
                    continue
            except Exception as e:
                print(f"Hata oluştu: {e}")
                continue

        self.driver.quit()

        df = pd.DataFrame({"Yorumlar": yorumlar})
        df.to_csv("trendyol_pizza_yorumlar.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    pizza_yorumlar = TrendYolPizzaYorumlar()
    pizza_yorumlar.arama_yap_ve_veri_cek()
