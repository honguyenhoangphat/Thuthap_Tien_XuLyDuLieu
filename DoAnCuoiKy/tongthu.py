from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Truy cập trang web
url = "https://vietnamtourism.gov.vn/statistic/receipts"  # Đặt URL trang web chứa bảng
driver.get(url)

# Đợi bảng hiển thị (chờ tối đa 10 giây)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "receipts-statistic-table"))
)

# Tìm bảng dữ liệu
table = driver.find_element(By.CLASS_NAME, "receipts-statistic-table")

# Thu thập các dòng trong bảng
rows = table.find_elements(By.TAG_NAME, "tr")

data = []

# Duyệt qua từng dòng và lấy dữ liệu từ các ô (td)
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    row_data = [cell.text for cell in cells]
    if row_data:  # Bỏ qua các dòng rỗng
        data.append(row_data)

# Đóng trình duyệt
driver.quit()

# Tạo DataFrame từ dữ liệu thu thập được
df = pd.DataFrame(data, columns=["Năm", "Tổng thu từ khách du lịch (nghìn tỷ đồng)", "Tốc độ tăng trưởng (%)"])

# Lưu vào file CSV hoặc Excel
df.to_csv('tong_thu_du_lich.csv', index=False, encoding='utf-8')
print("Dữ liệu đã được lưu vào CSV thành công!")

# df.to_excel('tong_thu_du_lich.xlsx', index=False,  engine='openpyxl')
# print("Dữ liệu đã được lưu vào file Excel thành công!")
