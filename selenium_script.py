import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(
    'https://shopee.vn/Son-Kem-Perfect-Diary-M%C3%A0u-L%C3%AC-T%C3%B4ng-M%C3%A0u-C%E1%BB%95-%C4%90i%E1%BB%83n-L%C3'
    '%A2u-Tr%C3%B4i-2.5g-i.277411443.7254565873?sp_atk=a68e6490-46b2-4da8-9f26-affa04027d69')

comment = list()
variation = []
rating = []
datetime = []
n = 5  # number of page to load, 6 comment each page
try:

    for i in range(n):

        # load page
        time.sleep(10)
        if i == 0:
            driver.execute_script("window.scrollTo(0, window.scrollY + 5200)")
            # Thêm code filter bình luận chỉ có rating ở đây
        else:
            driver.execute_script("window.scrollTo(0, window.scrollY + 1200)")
        time.sleep(10)

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
        time.sleep(10)
    # driver.quit()
finally:

    # Thêm code lưu data sang dataframe ở đây
    driver.quit()
