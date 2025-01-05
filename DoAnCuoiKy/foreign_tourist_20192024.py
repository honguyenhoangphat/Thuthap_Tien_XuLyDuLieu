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
driver.get("https://vietnamtourism.gov.vn/statistic/international?year=2019&period=t1")

data = []
years = ['2019','2020','2021','2022','2023','2024']
months = ['t1', 't2', 't3','t4','t5','t6','t7','t8','t9','t10','t11','t12']

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
            EC.presence_of_element_located((By.XPATH, "//tr[@class='total-row']"))
        )
    time.sleep(5)
    for month in months:
        
        time.sleep(1)
        data = []
        try:
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
            # Tìm tất cả các dòng <tr> rồi lọc theo class trong Python
            rows = driver.find_elements(By.TAG_NAME, "tr")
            
            filtered_rows = [row for row in rows if 'data-row' in row.get_attribute('class') or 'total-row' in row.get_attribute('class')]
            
            if not filtered_rows:  # Nếu không tìm thấy bất kỳ dòng dữ liệu nào
                print(f"Không có dữ liệu cho {month}/{year}. Thêm dữ liệu mặc định.")
                row_data = [year, month, 'Không có dữ liệu', 0, 0, 0, 0, pd.NA, pd.NA]
                data.append(row_data)
            else:
                for row in filtered_rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = [cell.text if cell.text.strip() else pd.NA for cell in cells]
                    while len(row_data) < 8:
                        row_data.append(pd.NA)
            
                    if 'total-row' in row.get_attribute('class'):
                        row_data.insert(0, 'Tổng cộng')
                    else:
                        row_data.insert(0, month)
                    
                    row_data.insert(0, year)
                    data.append(row_data)

            
        except TimeoutException:
            print(f"Timeout cho {month}/{year}. Thêm dữ liệu mặc định.")
            row_data = [year, month, 'Không có dữ liệu (Timeout)', 0, 0, 0, 0, 0, pd.NA, pd.NA]
            data.append(row_data)         
        df = pd.DataFrame(data, columns=["Năm","Tháng","Chỉ tiêu", "Ước tính mỗi tháng", "Tổng lượt khách cả năm", "So với tháng trước (%)", "So sánh tháng này ở năm trước(%)","So sánh tổng lượt khách với cùng kỳ năm trước (%)","",""])
        file_path = 'foreign_tourist.csv'
        if not os.path.isfile(file_path):
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(file_path, index=False, mode='a', header=False, encoding='utf-8-sig')
        print(f"Đã lưu dữ liệu cho {month}/{year} vào CSV.")           
        driver.execute_script("window.scrollTo(0,300);")
        time.sleep(2)
# Tạo DataFrame từ dữ liệu thu thập được

print("Du lieu da duoc luu thanh cong")
# Đóng trình duyệt sau khi hoàn thành
driver.quit()
