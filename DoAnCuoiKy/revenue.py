from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Khoi tao Firefox
driver = webdriver.Firefox()

# Mo trang web
url = "https://www.gso.gov.vn/px-web-2/?pxid=V1003&theme=Th%C6%B0%C6%A1ng%20m%E1%BA%A1i%2C%20gi%C3%A1%20c%E1%BA%A3"
driver.get(url)

wait = WebDriverWait(driver, 20)
# Chuyển vào iframe (nếu có)
try:
    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(iframe)
except:
    print("Không tìm thấy iframe, tiếp tục mà không cần chuyển iframe.")

# Click nút cho tỉnh, thành phố
select_all_city_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_ctl01_VariableValueSelect_VariableValueSelect_SelectAllButton"]')
))
select_all_city_button.click()

# Click nút cho năm
select_all_year_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_ctl02_VariableValueSelect_VariableValueSelect_SelectAllButton"]')
))
select_all_year_button.click()

# Click nút "Tiếp tục"
continue_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_ButtonViewTable"]')
))
continue_button.click()

# Đợi bảng
time.sleep(15)

# 1. Thu thập tiêu đề năm (dòng <thead>, tr[2])
header_row = driver.find_elements(By.XPATH, '//*[@id="ctl00_ctl00_ContentPlaceHolderMain_cphMain_Table1_Table1_DataTable"]/thead/tr[2]/th')

# Chỉ lấy văn bản của các th (năm)
header = [col.text.strip() for col in header_row]

# 2. Thu thập dữ liệu bảng (dòng <tbody>)
rows = driver.find_elements(By.XPATH, '//*[@id="ctl00_ctl00_ContentPlaceHolderMain_cphMain_Table1_Table1_DataTable"]/tbody/tr')

data = []
for row in rows:
    cols = row.find_elements(By.XPATH, './/th | .//td')  # Lấy cả th (tên tỉnh) và td (giá trị)
    cols = [col.text.strip() for col in cols]
    data.append(cols)

# Chuyển dữ liệu vào DataFrame và đặt tiêu đề
df = pd.DataFrame(data, columns=['Tỉnh/Thành phố'] + header)  # Dòng đầu là tên tỉnh/thành phố và các năm

# Lưu vào file CSV với tiêu đề (header)
df.to_csv('doanh_thu_du_lich.csv', index=False, encoding='utf-8-sig')

print("Đã lưu dữ liệu vào doanh_thu_du_lich.csv")

# Đóng trình duyệt
driver.quit()