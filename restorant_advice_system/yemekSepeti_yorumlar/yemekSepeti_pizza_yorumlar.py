import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

class YemekSepetiDonerYorumları:
    def __init__(self):
        options=webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver=webdriver.Chrome(options=options)
        self.wait=WebDriverWait(self.driver,20)
        self.url="https://www.yemeksepeti.com/restaurants/new?lng=29.01074&lat=41.07683&vertical=restaurants&query=pizza"

    def arama_yap_ve_veri_cek(self):
        print(f"sayfa açılıyor {self.url}")
        self.driver.get(self.url)
        try:
            print("siteye giriliyor")
            selector = "a[data-testid^='vendor-tile-new-link-']"

            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,selector)))
            restaurant_element=self.driver.find_elements(By.CSS_SELECTOR,selector)
            print(f"toplam {len(restaurant_element)} restornt bulundu")
        except Exception as e:
            print(f"hata verdi {e}")
            self.driver.quit()
            return
    
        urls_to_visit=[]

        for element in restaurant_element:
            link=element.get_attribute("href")
            if link and link not in urls_to_visit:
                urls_to_visit.append(link)
        
        print("\n--- toplam url ---\n")
        for url in urls_to_visit:
            print(url)

        yorumlar=[]

        for url in urls_to_visit:
            try:
                print(f"\n restoarant sayfası açıldı {url}")
                self.driver.get(url)

                yorum_button_xpath="//button[.//span[contains(text(), 'Yorumlar')]]"
                self.wait.until(EC.element_to_be_clickable((By.XPATH,yorum_button_xpath)))
                yorum_button=self.driver.find_element(By.XPATH,yorum_button_xpath)

                if yorum_button:
                    yorum_button.click()
                
                    self.wait.until(EC.presence_of_all_elements_located((
                      By.CSS_SELECTOR,".info-reviews-modal-description"
                    )))
                    yorum_elements=self.driver.find_elements(
                       By.CSS_SELECTOR,".info-reviews-modal-description"
                     )
                    print(f"toplam {len(yorum_elements)}tane yorum bulundu.")

                for yorum_element in yorum_elements:
                    yorum_text=yorum_element.text.strip()
                    yorumlar.append(yorum_text)
                    print("-yorum-")
                    print(yorum_text)
                else:
                    print("yorum yok")
                    continue

            except Exception as e:
                print(f"hata var {e}")
                continue
        
        self.driver.quit()

        df=pd.DataFrame(yorumlar,columns=["Yorumlar"])
        df.to_csv("yemeksepeti_pizza_yorumlar.csv",index=False,encoding="utf-8-sig")

if __name__=="__main__":
    doner_yorum=YemekSepetiDonerYorumları()
    doner_yorum.arama_yap_ve_veri_cek()

