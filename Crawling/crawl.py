import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def crawl_tokopedia_data():
    url = "https://www.tokopedia.com/unilever/product"
    driver = webdriver.Chrome()
    driver.get(url)

    # Inisialisasi list kosong untuk menyimpan data
    data = []
    platform = "Tokopedia"
    id = 0

    # Fungsi untuk mengklik tombol "Selanjutnya"
    def click_next_button():
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="btnShopProductPageNext"]')
            next_button.click()
            time.sleep(3)
            return True
        except NoSuchElementException:
            return False

    while True:
        search_results = driver.find_elements(By.CLASS_NAME, "css-1sn1xa2")

        for search_result in search_results:
            # Temukan semua elemen "hotel-card" dalam "seo-search-result"
            product_name = search_result.find_element(By.CSS_SELECTOR, '[data-testid="linkProductName"]').text
            price = search_result.find_element(By.CSS_SELECTOR, '[data-testid="linkProductPrice"]').text

            try:
                price_before = search_result.find_element(By.CSS_SELECTOR, '[data-testid="lblProductSlashPrice"]').text
            except NoSuchElementException:
                price_before = "without discount"

            try:
                discount = search_result.find_element(By.CSS_SELECTOR, '[data-testid="lblProductDiscount"]').text
            except NoSuchElementException:
                discount = "without discount"

            link_element = search_result.find_element(By.TAG_NAME, "a")

            driver.execute_script("window.open(arguments[0], '_blank');", link_element.get_attribute("href"))

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])

            # Tunggu hingga tab baru terbuka (Anda bisa menambahkan waktu tunggu sesuai kebutuhan)
            time.sleep(3)  # Tunggu beberapa detik untuk memastikan tab baru terbuka

            # Di sini Anda dapat menambahkan kode untuk mengambil data dari tab/jendela baru
            try:
                category_list = driver.find_elements(By.CLASS_NAME, "css-d5bnys")
                if len(category_list) >= 3:
                    category = category_list[2].text
                else:
                    category = "-"
            except NoSuchElementException:
                category = "-"

            try:
                description = driver.find_element(By.CSS_SELECTOR, '[data-testid="lblPDPDescriptionProduk"]').text
            except NoSuchElementException:
                description = "-"

            id += 1
            data.append([id, product_name, price, price_before, discount, category, description, platform, datetime.now()])

            # Kembali ke tab/jendela sebelumnya
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        if not click_next_button():
            print("Halaman selanjutnya tidak tersedia atau sudah selesai.")
            break  # Keluar dari loop jika tombol "Selanjutnya" tidak ditemukan

    # Tutup WebDriver
    driver.quit()

    # Nama kolom-kolom
    columns = ['id', 'product_name', 'price', 'price_before', 'discount', 'category', 'description', 'platform', 'datetime']

    # Buat DataFrame
    df = pd.DataFrame(data, columns=columns)
    df.to_excel('data_product.xlsx')

if __name__ == "__main__":
    crawl_tokopedia_data()
