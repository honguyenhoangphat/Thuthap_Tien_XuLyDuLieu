from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo WebDriver
geckodriver_path = r"C:/Users/Admin/Documents/Thuthap_Tien_XuLyDuLieu/DoAnCuoiKy/geckodriver.exe"
ser = Service(geckodriver_path) # Khởi tạo đối tượng dịch vụ với geckodriver

# Tạo tùy chọn
options = webdriver.firefox.options.Options()
options.binary_location ="C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options=options, service=ser)
# Mở trang web
driver.get("https://vietnamtourism.gov.vn/statistic/international?year=2019&period=t1")

data = []

years = [2019,2020]
months = ['t1', 't2', 't3']


for year in years:
    year_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "statistic-year"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year_dropdown)
    time.sleep(2)
    year_select = Select(year_dropdown)
    try:
        year_select.select_by_value(str(year))
    except:
        year_select.select_by_visible_text(str(year))
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='data-row']"))
        )
    time.sleep(1)
    for month in months:
        time.sleep(1)
        month_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "statistic-month"))
        )
        month_select = Select(month_dropdown)
        month_select.select_by_value(month)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='data-row']"))
        )
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
# Tìm tất cả các dòng có class 'data-row'
        rows = driver.find_elements(By.XPATH, "//tr[@class='data-row']")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            if row_data:  # Chỉ thêm nếu dòng có dữ liệu
                row_data.insert(0, month)
                row_data.insert(0, year)
                data.append(row_data)
        driver.execute_script("window.scrollTo(0,300);")
        time.sleep(2)
# Tạo DataFrame từ dữ liệu thu thập được
df = pd.DataFrame(data, columns=["Tháng","Năm","Chỉ tiêu", "Tháng 12/2018", "Ước tính tháng 1/2019", "Tháng 1 so với tháng trước (%)", "Tháng 1 so với tháng 1/2018 (%)","So sánh với năm trước"])
df.to_csv('data_sl_customers',index=False,encoding='utf-8')
print("Du lieu da duoc luu thanh cong")
# Đóng trình duyệt sau khi hoàn thành
driver.quit()
