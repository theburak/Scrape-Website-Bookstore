from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import openpyxl

# Scrape All Books "Title", "Price", "Stock Availability"
# ChromeDriver settings
service = Service('C:/WebDriver/chromedriver.exe')  # Specify the path to chromedriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run the browser in the background
driver = webdriver.Chrome(service=service, options=options)

# Create an Excel file
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "Books"
sheet.append(["Title", "Price", "Stock Availability"])

# Navigate to the website
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

for page in range(1, 51):  # There are 50 pages
    url = base_url.format(page)
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    if not books:
        break

    for book in books:
        # Extract book details
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        stock_status = book.find('p', class_='instock availability').text.strip()

        # Write to the Excel file
        sheet.append([title, price, stock_status])

# Close the browser
driver.quit()

# Save the Excel file
wb.save("books.xlsx")
print("Data has been saved to 'books.xlsx'.")