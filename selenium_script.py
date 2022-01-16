import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(
    'https://shopee.vn/product/9277307/2288984704?smtt=0.31320430-1642307124.9&fbclid'
    '=IwAR2ImR10gU6NF_QyV1CNhwptBh57LogiebxvYj3LHdIsYthYFrrAk1rGP-Q '
)

comment = []
variation = []
rating = []
datetime = []
tag_name = []
count = 0
n = 100  # number of page to load, 6 comments each page
try:

    for i in range(n):

        # load page
        if i == 0:
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, window.scrollY + 4200)")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, window.scrollY + 2200)")
            # Thêm code filter bình luận chỉ có rating ở đây
            rating_filter = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class = 'product-rating-overview__filters']"))
            )

            button = rating_filter.find_element(By.XPATH, ".//div[starts-with(text(), 'Có Bình luận')]")
            button.click()

        time.sleep(3)

        # collect comment
        product = driver.find_elements(By.CLASS_NAME, 'shopee-product-rating__main')

        for ele in product:
            try:
                comment.append(ele.find_element(By.XPATH, ".//*[@class = '_3NrdYc']").text)

            except:
                comment.append('NULL')

        variations = driver.find_elements(By.CLASS_NAME, 'shopee-product-rating__variation')
        for var in variations:
            variation.append(var.text)

        datetimes = driver.find_elements(By.CLASS_NAME, 'shopee-product-rating__time')
        for date in datetimes:
            datetime.append(date.text)

        ratings_list = driver.find_elements(By.CLASS_NAME, 'shopee-product-rating')
        for rating_element in ratings_list:
            rating.append(len(rating_element.find_elements(By.XPATH, ".//*[@class = 'shopee-svg-icon "
                                                                     "icon-rating-solid--active icon-rating-solid']")))

        # next page
        button = driver.find_element(By.XPATH, "//button[@class='shopee-icon-button shopee-icon-button--right ']")
        current_last_button = driver.find_elements(By.XPATH,
                                                   "//button[@class='shopee-button-no-outline shopee-button-no-outline--non-click']")
        if len(current_last_button) == 1 and i > 10:
            count += 1
            if count == 3:
                break
        button.click()
        # time.sleep(5)

        if (i % 1000) == 0:
            data = {'comment': comment, 'variation': variation, 'datetime': datetime, 'rating': rating}
            df = pd.DataFrame(data)
            df.to_csv('son_review.csv', encoding='utf-8', index=False)

    # driver.quit()
finally:
    driver.quit()

# Thêm code lưu data sang dataframe ở đây
data = {'comment': comment, 'variation': variation, 'datetime': datetime, 'rating': rating}
df = pd.DataFrame(data)
df.to_csv('son_review.csv', encoding='utf-8', index=False)
