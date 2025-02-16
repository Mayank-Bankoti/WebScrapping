
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Set up Chrome options
chrome_options = Options()
chrome_options.headless = True  # Run in headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the URL
url = "https://engineering.careers360.com/colleges/ranking"
driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract data
college_name = soup.find('h3', class_='college_name').text.strip()
nirf_rank = soup.find('div', class_='align-center').find('strong').text.strip()
rating = soup.find('strong').text.strip()
ownership = soup.find('strong', class_='strong_ownership').text.strip()
review_count = soup.find('span', class_='review_text').text.strip()
rating_value = soup.find('span', class_='star_text').text.strip().split()[0]  # Extract numeric rating

# Extract course and fees (Handling Deprecation Warning)
courses = soup.find_all('ul', class_='snippet_list')
course_details = []
for course in courses:
    course_name = course.find('a').text.strip()
    fee_span = course.find('span', class_='gray_text')
    fee = fee_span.find_next_sibling(string=True).strip() if fee_span and fee_span.find_next_sibling(string=True) else "N/A"
    course_details.append((course_name, fee))

# Create DataFrame
df = pd.DataFrame({
    'College Name': [college_name],
    'NIRF Rank': [nirf_rank],
    'Rating': [rating],
    'Ownership': [ownership],
    'Review Count': [review_count],
    'Rating Value': [rating_value],
    'Courses': [", ".join([c[0] for c in course_details])],
    'Fees': [", ".join([c[1] for c in course_details])]
})
