from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Start time
start_time = datetime.now()
print(f'Crawl starting time: {start_time.time()}')

# Initialize job list
job_list = []

# Function to generate URL
def generate_url(index):
    if index == 1:
        return "https://www.naukri.com/software-developer-jobs?k=software%20developer"
    else:
        return f"https://www.naukri.com/software-developer-jobs-{index}?k=software%20developer"

# Function to extract rating
def extract_rating(rating_a):
    if rating_a is None or rating_a.find('span', class_="main-2") is None:
        return "None"
    return rating_a.find('span', class_="main-2").text

# Function to parse job data
def parse_job_data_from_soup(page_jobs):
    for job in page_jobs:
        job = BeautifulSoup(str(job), 'html.parser')
        try:
            job_title = job.find('a', class_="title").text.strip()
            company_name = job.find('a', class_="subTitle").text.strip()
            rating = extract_rating(job.find('span', class_="main-2"))

            job_details = job.find('ul', class_="mt-8").find_all('li')
            experience = job_details[0].text.strip() if len(job_details) > 0 else "Not Specified"
            location = job_details[1].text.strip() if len(job_details) > 1 else "Not Specified"
            
            min_requirements = job.find('div', class_="job-description").text.strip() if job.find('div', class_="job-description") else "N/A"

            all_tech_stack = [li.text for li in job.find_all('li', class_="dot-gt")]
            print("titlr",job_title)
            # Append job data to list
            job_list.append({
                "Job Title": job_title,
                "Company Name": company_name,
                "Rating": rating,
                "Experience": experience,
                "Location": location,
                "Minimum Requirements": min_requirements,
                "Tech Stack": ", ".join(all_tech_stack)
            })

        except AttributeError:
            continue  # Skip jobs that don't have full details

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Scraping loop
start_page = 1
page_end = 5  # Reduce for testing; increase for full crawl

for i in range(start_page, page_end + 1):
    print(f"Scraping page {i}...")
    url = generate_url(i)
    driver.get(url)

    sleep(randint(5, 10))  # Random delay to avoid detection

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_soup = soup.find_all("div", class_="srp-jobtuple-wrapper")

    parse_job_data_from_soup(page_soup)

# Close the browser
driver.quit()

# Convert data to DataFrame
df = pd.DataFrame(job_list)
print(df.head())

# Save data to CSV
df.to_csv("naukri_jobs.csv", index=False)
print("Data saved to naukri_jobs.csv")
