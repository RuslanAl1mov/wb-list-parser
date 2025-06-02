from pprint import pprint
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException


class WBParser():
    
    def get_prod_link(self, articul: str) -> str:
        """
        Автоматически подставляет артикул товара в ссылку 
        и возвращает полноценную ссылку.
        :param articul: артикул товара
        """
        return f"https://www.wildberries.ru/catalog/{articul}/detail.aspx"


    def get_driver(self, headless: bool = True, timeout: int = 30) -> webdriver.Chrome:
        """
        Создаёт и настраивает экземпляр ChromeDriver.
        :param headless: запускать ли в headless-режиме (без GUI).
        :param timeout:   базовый тайм-аут для page load (сек).
        """
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(timeout)
        return driver


    def parse_page(self, url: str, wait_sec: int = 25) -> dict:
        """
        Загружает страницу и возвращает нужные данные
        """
        driver = self.get_driver(headless=False)
        result: dict = {}
        try:
            driver.get(url)
            wait = WebDriverWait(driver, wait_sec)

            # 1. Название товара
            product_name_el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-page__title")))
            result["name"] = product_name_el.text.strip()
            
            # 2. Категория товара 
            categories = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "breadcrumbs__link")))
            if len(categories) >= 3:
                result["category"] = categories[2].text.strip()
            else:
                result["category"] = " > ".join([el.text.strip() for el in categories])
                
            # 3. Ждем загрузки блоков фото и собираем ссылки на фото товаров
            photos: list = []
            small_photo_elems = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "slide__content")))
            time.sleep(1.5)
            actions = ActionChains(driver)
            for small_photo_block in small_photo_elems:
                try:
                    small_img_el = small_photo_block.find_element(By.TAG_NAME, "img")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", small_img_el)
                    time.sleep(0.5)
                    actions.move_to_element(small_img_el).perform()
                    big_img_el = driver.find_element(By.CSS_SELECTOR, "img.j-zoom-image")
                    big_img_src = big_img_el.get_attribute("src")
                    photos.append(big_img_src)
                    if len(photos) >= 4 and small_img_el:
                        try:
                            photo_slider_bitton = driver.find_element(By.CSS_SELECTOR, "button.swiper-button-next")
                            if photo_slider_bitton:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", small_img_el)
                                actions.move_to_element(photo_slider_bitton).click().perform()
                                time.sleep(0.5)
                        except ElementNotInteractableException:
                            pass
                except NoSuchElementException:
                    """
                        Мы ищем img внутри блока с фотографией тег img, но подобная ошибка выпадает если внутри 
                        блока не img, а video.
                    """
                    continue
            result["photos"] = photos

            # 4. Находим кнопку для раскрытия спсика с параметрами товара
            params_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.product-page__btn-detail")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", params_button)
            actions.move_to_element(params_button).click().perform()
            time.sleep(1)
            
            # 5. Парсим параметры товара
            try:
                # Находим кнопку "Характеристики и описание"
                params_container = driver.find_element(By.CSS_SELECTOR, "div.product-params")
                tables = params_container.find_elements(By.CSS_SELECTOR, "table.product-params__table")
                
                # Парсим все таблицы с описанием
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-params table.product-params__table")))
                characteristics: dict = {}
                for table in tables:
                    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr.product-params__row")
                    for row in rows:
                        # ключ - название характеристики
                        key_el = row.find_element(By.CSS_SELECTOR, "th.product-params__cell span.product-params__cell-decor span")
                        key_text = key_el.text
                        # значение хаарктеристики
                        val_el = row.find_element(By.CSS_SELECTOR, "td.product-params__cell span")
                        val_text = val_el.text

                        characteristics[key_text] = val_text                    
                result["characteristics"] = characteristics
            except TimeoutException:
                result["characteristics"] = {}
            
            return result

        except TimeoutException:
            print(f"[!] Timeout: не удалось найти нужный элемент за {wait_sec} секунд.")
            return None
        
        except Exception as e:
            print(e)
            return None

        finally:
            driver.quit()


if __name__ == "__main__":
    ARTICULS = ["258235213", "7250481", "392030137"]
    DATA = {}
    parser = WBParser()
    for articul in ARTICULS:
        prod_link = parser.get_prod_link(articul)
        prod_data = parser.parse_page(prod_link)
        
        if prod_data:
            prod_data["articul"] = articul
            prod_data["url"] = prod_link
        
        DATA[articul] = prod_data

    pprint(DATA)
