from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
# cái này có mấy tháng nó không lấy được tên tháng
# Khởi động trình duyệt
driver = webdriver.Chrome()

# Truy cập trang web
url = "https://tradingeconomics.com/vietnam/inflation-cpi"  # Thay bằng link chính xác của trang
driver.get(url)

# Chờ trang load hoàn tất
time.sleep(5)  # Đợi biểu đồ load (tùy trang có thể cần tăng lên 10s nếu mạng chậm)

# Lấy dữ liệu từ biểu đồ (dữ liệu từ SVG hoặc Highcharts)
chart_values = driver.find_elements(By.CSS_SELECTOR, "div.highcharts-label span")
x_labels = driver.find_elements(By.CSS_SELECTOR, "span[style*='rotate(0deg)']")  # Nhãn trục x (tháng, năm)

# Trích xuất dữ liệu
data = []
for i, value in enumerate(chart_values):
    month = x_labels[i].text if i < len(x_labels) else "Unknown"
    inflation_rate = value.text
    data.append([month, inflation_rate])

# Tạo DataFrame
df = pd.DataFrame(data, columns=["Month", "Inflation Rate"])

# Lưu vào file Excel
# df.to_excel("vietnam_inflation_rate.xlsx", index=False)
df.to_csv('ty_le_lam_phat.csv', index=False, encoding='utf-8')
# Đóng trình duyệt
driver.quit()
print("Dữ liệu đã được thu thập và lưu thành công!")
