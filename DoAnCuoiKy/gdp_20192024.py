from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.common.exceptions import TimeoutException
# Khởi động trình duyệt
geckodriver_path = r"C:/Users/Admin/Documents/Thuthap_Tien_XuLyDuLieu/DoAnCuoiKy/geckodriver.exe"
ser = Service(geckodriver_path) # Khởi tạo đối tượng dịch vụ với geckodriver

# Tạo tùy chọn
options = webdriver.firefox.options.Options()
options.binary_location ="C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options=options, service=ser)

# Truy cập trang web
url = "https://tradingeconomics.com/vietnam/gdp"
driver.get(url)
time.sleep(5)

# Click vào nút "10Y" để hiển thị dữ liệu 10 năm
ten_year_button = driver.find_element(By.XPATH, "//a[contains(@data-span_str,'5Y')]")
ten_year_button.click()
time.sleep(5)

# Di chuyển chuột lần lượt qua từng điểm trên biểu đồ
chart_points = driver.find_elements(By.CSS_SELECTOR, ".highcharts-point")

data = []
actions = ActionChains(driver)

for gdp in chart_points:
    try:
        # Di chuột qua từng điểm
        actions.move_to_element(gdp).perform()
        time.sleep(1)  # Chờ tooltip hiện

        # Lấy dữ liệu từ tooltip
        tooltip = driver.find_element(By.CSS_SELECTOR, "div.tooltip-box")
        date = tooltip.find_element(By.CSS_SELECTOR, "span.tooltip-date").text
        gdp_value = tooltip.find_element(By.CSS_SELECTOR, "span.tooltip-value").text
        gdp_value_clean = float(gdp_value.replace("USD Billion", "").strip())

        print(f"{date} - {gdp_value_clean}")
        data.append([date, gdp_value_clean])

    except Exception as e:
        print(f"Lỗi: {e}")
        continue

# Tạo DataFrame và lưu dữ liệu
df = pd.DataFrame(data, columns=["Year", "GDP (Billion USD)"])
df.to_csv('gdp_20192024.csv', index=False, encoding='utf-8')

# Đóng trình duyệt
driver.quit()
print("Dữ liệu đã được thu thập và lưu thành công!")
