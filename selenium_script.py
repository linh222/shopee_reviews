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
    'https://shopee.vn/Son-Kem-Perfect-Diary-M%C3%A0u-L%C3%AC-T%C3%B4ng-M%C3%A0u-C%E1%BB%95-%C4%90i%E1%BB%83n-L%C3'
    '%A2u-Tr%C3%B4i-2.5g-i.277411443.7254565873?sp_atk=a68e6490-46b2-4da8-9f26-affa04027d69')

comment = []
variation = []
rating = []
datetime = []
tag_name = []
n = 3  # number of page to load, 6 comments each page
try:

    for i in range(n):

        # load page
        time.sleep(5)
        if i == 0:
            driver.execute_script("window.scrollTo(0, window.scrollY + 4200)")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, window.scrollY + 2200)")
            # Thêm code filter bình luận chỉ có rating ở đây
            rating_filter = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class = 'product-rating-overview__filters']"))
            )
            print(rating_filter.text)
            button = rating_filter.find_element(By.XPATH, ".//div[starts-with(text(), 'Có Bình luận')]")
            button.click()
        else:
            driver.execute_script("window.scrollTo(0, window.scrollY + 1200)")
        time.sleep(5)

        # collect comment
        comments = driver.find_elements(By.CLASS_NAME, '_3NrdYc')
        for cmt in comments:
            comment.append(cmt.text)

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
        button.click()
        time.sleep(5)

        if (i % 1000) == 0:
            data = {'comment': comment, 'variation': variation, 'datetime': datetime, 'rating': rating}
            df = pd.DataFrame(data)
            df.to_csv('son_review.csv', encoding='utf-8', index=False)

    # driver.quit()
finally:
    # Thêm code lưu data sang dataframe ở đây
    data = {'comment': comment, 'variation': variation, 'datetime': datetime, 'rating': rating}
    df = pd.DataFrame(data)
    df.to_csv('son_review.csv', encoding='utf-8', index=False)
    driver.quit()
