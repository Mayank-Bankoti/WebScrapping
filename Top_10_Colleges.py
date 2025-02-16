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
url = "https://collegedunia.com/btech-courses"
driver.get(url)

# Get the page source and parse it with BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'html.parser')

soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all <tr> elements with class "jsx-1623428107"
tr_elements = soup.find_all("tr", class_="jsx-1623428107")

# Extract data
college_data = []
for tr in tr_elements:
    rank = tr.find("span", class_="rank").text.strip() if tr.find("span", class_="rank") else "N/A"
    name = tr.find("div", class_="college-name").text.strip() if tr.find("div", class_="college-name") else "N/A"
    city = tr.find("span", class_="city").text.strip() if tr.find("span", class_="city") else "N/A"
    rating = tr.find("span", class_="jsx-1623428107").text.strip() if tr.find("span", class_="jsx-1623428107") else "N/A"
    cutoff = tr.find("span", class_="cutoff-data").text.strip() if tr.find("span", class_="cutoff-data") else "N/A"
    date = tr.find("div", class_="date").text.strip() if tr.find("div", class_="date") else "N/A"
    fees = tr.find("div", class_="fees").text.strip() if tr.find("div", class_="fees") else "N/A"

    college_data.append({
        "Rank": rank,
        "Name": name,
        "City": city,
        "Rating": rating,
        "Cutoff": cutoff,
        "Admission Date": date,
        "Fees": fees
    })

# Print extracted data
for college in college_data:
    print(college)
df = pd.DataFrame(college_data, columns=["Rank", "Name", "City", "Rating", "Cutoff", "Admission Date", "Fees"])
# Close the WebDriver
driver.quit()
