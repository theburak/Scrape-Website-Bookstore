from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

import warnings
warnings.filterwarnings("ignore")

url = "https://books.toscrape.com"

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')  # Start the browser maximized

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=options)

# Open the specified URL in the browser
driver.get(url)

# Define an XPath query to find links containing the text "Travel" or "Nonfiction"
XPATH_query = "//a[contains(text(),'Travel') or contains(text(),'Nonfiction')]"

# Find all elements matching the XPath query
category_elements = driver.find_elements(By.XPATH, XPATH_query)

# Print the found category elements
print(category_elements)

# Extract the URLs from the category elements and store them in a list
category_urls = [element.get_attribute("href") for element in category_elements]
print(category_urls)  # Print the list of category URLs

# Iterate over each category URL
for category_url in category_urls:
    driver.get(category_url)  # Navigate to the category page
    time.sleep(2)  # Wait for 2 seconds to ensure the page loads completely

    # Find all book elements on the category page
    books = driver.find_elements(By.XPATH, "//h3/a")
    # Extract the URLs from the book elements and store them in a list
    book_urls = [book.get_attribute("href") for book in books]
    print(book_urls)  # Print the list of book URLs

    # Iterate over each book URL
    for book_url in book_urls:
        driver.get(book_url)  # Navigate to the book page
        time.sleep(2)  # Wait for 2 seconds to ensure the page loads completely

        # Extract the book title from the page
        title = driver.find_element(By.XPATH, "//h1").text
        # Extract the book price from the page
        price = driver.find_element(By.XPATH, "//p[@class='price_color']").text
        print(title, price)  # Print the book title and price

        driver.back()  # Go back to the previous page (category page)
        time.sleep(2)  # Wait for 2 seconds to ensure the page loads completely

    break  # Exit the loop after processing the first category (for testing purposes)

book_elements_XPATH = "//div[@class='image_container']//a"

# Find all book elements on the page using the specified XPath query
book_elements = driver.find_elements(By.XPATH, book_elements_XPATH)
book_urls = [element.get_attribute("href") for element in book_elements]
print(book_urls)  # Print the list of book URLs
print(len(book_urls))  # Print the number of book URLs found

# Set the maximum number of pagination pages to scrape
max_pagination = 3

# Check if there are enough categories found
if len(category_urls) < 2:
    print("Not enough categories found.")
    driver.quit()  # Close the browser

    # Import necessary functions for URL manipulation
    from urllib.parse import urljoin, urlparse, urlunparse, parse_qs, urlencode

    # Define a function to construct pagination URLs
    def construct_pagination_url(base_url, page_number):
        parsed_url = urlparse(base_url)
        query_params = parse_qs(parsed_url.query)
        query_params['page'] = page_number
        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=new_query))
        return new_url

    # Initialize the page number
    i = 1
    # Update the URL for pagination
    update_url = url if i == 1 else construct_pagination_url(url, i)

# Set the URL to the second category URL found
url = category_urls[1]

# Initialize an empty list to store book URLs
book_urls = []

# Iterate over the pagination pages
for i in range(1, max_pagination):
    # Update the URL for the current page
    update_url = url if i == 1 else url.replace("index", f"page-{i}")
    driver.get(update_url)  # Open the updated URL in the browser

    # Find all book elements on the current page
    book_elements = driver.find_elements(By.XPATH, book_elements_XPATH)

    # Extract the URLs from the book elements and add them to the list
    temp_urls = [element.get_attribute("href") for element in book_elements]
    book_urls.extend(temp_urls)

# Print the list of book URLs
print(book_urls)

# Print the total number of book URLs found
print(len(book_urls))

# Open the first book URL in the browser
driver.get(book_urls[0])
# Find the content div element on the book page
content_div = driver.find_elements(By.XPATH, "//div[@class='content']")
print(content_div)  # Print the content div element

# Extract the inner HTML of the content div element
innerHTML = content_div[0].get_attribute("innerHTML")
print(innerHTML)  # Print the inner HTML of the content div element

# Parse the inner HTML using BeautifulSoup
soup = BeautifulSoup(innerHTML, "html.parser")

# Print the prettified HTML content of the content div
print(soup.prettify())

# Find the book name using the h1 tag
book_name = soup.find('h1').text
print(book_name)  # Print the book name

# Compile a regular expression to match the class name that starts with 'star-rating'
regex = re.compile('^star-rating ')
# Find the star rating class
star_rating_class = soup.find('p', class_=regex)['class'][1]
print(star_rating_class)  # Print the star rating class

# Initialize an empty dictionary to store book details
book_details = {}
# Find the product information table
table = soup.find("table")
if table:
    # Find all table rows in the product information table
    table_rows = table.find_all("tr")

    # Iterate over each table row
    for row in table_rows:
        key = row.find("th").text  # Extract the key from the table header
        value = row.find("td").text  # Extract the value from the table data
        book_details[key] = value  # Add the key-value pair to the book_details dictionary

print(book_details)  # Print the book details dictionary

# Function to initialize and return a Chrome WebDriver instance
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    return driver

# Function to get category URLs based on the category name
def get_category_urls(driver, url, category_name):
    driver.get(url)
    category_elements_xpath = f"//a[contains(text(), '{category_name}')]"
    category_elements = driver.find_elements(By.XPATH, category_elements_xpath)
    category_urls = [element.get_attribute("href") for element in category_elements]
    return category_urls

print(get_category_urls(get_driver(), url, 'Travel'))

# Function to get book URLs from a category page with pagination
def get_books_url(driver, url):
    max_pagination = 3
    book_urls = []
    book_elements_XPATH = "//div[@class='image_container']//a"

    for i in range(1, max_pagination):
        updated_url = url if i == 1 else url.replace("index", f"page-{i}")
        driver.get(updated_url)
        book_elements = driver.find_elements(By.XPATH, book_elements_XPATH)

        temp_urls = [element.get_attribute("href") for element in book_elements]
        book_urls.extend(temp_urls)

        if not book_elements:
            break

        temp_urls = [element.get_attribute("href") for element in book_elements]
        book_urls.extend(temp_urls)

    return book_urls

print(get_books_url(get_driver(), 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'))

# Function to get book details from a book page
def get_book_detail(driver, url):
    driver.get(url)
    content_div = driver.find_elements(By.XPATH, "//div[@class='content']")

    innerHTML = content_div[0].get_attribute("innerHTML")
    soup = BeautifulSoup(innerHTML, "html.parser")

    book_name = soup.find('h1').text

    regex = re.compile('^star-rating ')
    star_elem = soup.find("p", attrs={"class": regex})
    book_star_count = star_elem['class'][-1]

    description_elem = soup.find("div", attrs={"id": "product_description"}).find_next_sibling().text

    product_info = {}
    table_rows = soup.find("table").find_all("tr")
    for i in table_rows:
        key = i.find("th").text
        value = i.find("td").text
        product_info[key] = value

    return {'book_name': book_name, 'book_star': book_star_count, 'book_desc': description_elem, **product_info}

print(get_book_detail(get_driver(), 'https://books.toscrape.com/catalogue/a-summer-in-europe_458/index.html'))