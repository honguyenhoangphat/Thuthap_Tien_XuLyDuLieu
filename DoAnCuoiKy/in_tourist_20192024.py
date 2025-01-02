from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.common.exceptions import TimeoutException

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
driver.get("https://vietnamtourism.gov.vn/statistic/domestic")

data = []
years = ['2019','2020','2021','2022','2023','2024']
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
    time.sleep(3)
    rows = driver.find_elements(By.XPATH, "//tr[@class='data-row']")

    data = []
    try:
# Tìm tất cả các dòng có class 'data-row'
        rows = driver.find_elements(By.XPATH, "//tr[@class='data-row']")
        if not rows:  # Nếu không tìm thấy bất kỳ dòng dữ liệu nào
            print(f"Không có dữ liệu cho {year}. Thêm dữ liệu mặc định.")
            row_data = [year,0,0,0,0,0,0,0,0,0,0,0,0]
            data.append(row_data)
        else:
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text if cell.text.strip() else pd.NA for cell in cells]
                row_data.insert(0, year)
                while len(row_data) <= 14:
                    row_data.append(0)
                data.append(row_data)

    except TimeoutException:
        print(f"Timeout cho {year}. Thêm dữ liệu mặc định.")
        row_data = [year, 'Không có dữ liệu (Timeout)', 0, 0, 0, 0, 0,0,0,0,0,0,0]
        data.append(row_data)         
    df = pd.DataFrame(data, columns=['Năm','Chỉ tiêu', 'Tháng 1','Tháng 2','Tháng 3','Tháng 4','Tháng 5','Tháng 6',
                'Tháng 7','Tháng 8','Tháng 9','Tháng 10','Tháng 11','Tháng 12', 'Tổng'])
    file_path = 'in_tourist.xlsx'
    if not os.path.isfile(file_path):
        df.to_excel(file_path, index=False, engine='openpyxl')
    else:
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row, header=False)
    print(f"Đã lưu dữ liệu cho {year} vào Excel.")           
    driver.execute_script("window.scrollTo(0,300);")
    time.sleep(2)
# Tạo DataFrame từ dữ liệu thu thập được

print("Du lieu da duoc luu thanh cong")
# Đóng trình duyệt sau khi hoàn thành
driver.quit()
