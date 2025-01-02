from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

# Khởi tạo trình duyệt Firefox
driver = webdriver.Firefox()

# Mở trang web
url = "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?end=2023&locations=VN&start=2017&view=chart"
driver.get(url)

time.sleep(5)  # Đợi trang web tải hoàn tất
# Tìm biểu đồ và di chuột để lấy dữ liệu
chart = driver.find_element(By.CLASS_NAME, 'd3-chart')
actions = ActionChains(driver)
actions.move_to_element(chart).perform()

data = []
for year in range(2017, 2024):
    # Di chuột theo từng điểm
    actions.move_by_offset(50, 0).perform()
    time.sleep(1)  # Đợi tooltips hiển thị

    # Lấy dữ liệu từ tooltips
    tooltip = driver.find_element(By.CLASS_NAME, 'tooltips')
    value = tooltip.text
    print(value)

    # Tách dữ liệu thành năm và GDP
    if value:
        parts = value.split('\n')
        if len(parts) == 2:
            year_text = parts[0].split('(')[-1].replace(')', '')  # Lấy phần năm
            gdp_value = parts[1] + ' USD'
            data.append([year_text, gdp_value])

# Đóng trình duyệt
driver.quit()

# Xử lý dữ liệu thành DataFrame với 2 cột
df = pd.DataFrame(data, columns=['Year', 'GDP'])
print(df)

# Lưu vào file CSV hoặc Excel
df.to_csv('GDP.csv', index=False, encoding='utf-8')
print("Dữ liệu đã được lưu vào CSV thành công!")






