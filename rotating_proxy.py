from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://engineering.careers360.com/colleges/ranking")

# Get page source and parse with BeautifulSoup
html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, "html.parser")

# Extract college details
college_data = []
college_cards = soup.find_all("div", class_="card_block")

for card in college_cards:
    college_name = card.find("h3", class_="college_name").text.strip() if card.find("h3", class_="college_name") else "N/A"
    nirf_rank = card.find("strong").text.strip() if card.find("strong") else "N/A"
    rating = card.find("span", class_="star_text").text.strip() if card.find("span", class_="star_text") else "N/A"
    ownership = card.find("strong", class_="strong_ownership").text.strip() if card.find("strong", class_="strong_ownership") else "N/A"
    
    # Extract fees
    fees = []
    for fee_tag in card.find_all("li"):
        if "Fees" in fee_tag.text:
            fees.append(fee_tag.text.strip())
    fees = ", ".join(fees) if fees else "N/A"
    
    # Extract important links
    important_links = {}
    for link in card.find_all("a", href=True):
        if "admission" in link["href"]:
            important_links["Admission"] = link["href"]
        elif "placement" in link["href"]:
            important_links["Placement"] = link["href"]
        elif "courses" in link["href"]:
            important_links["Courses"] = link["href"]
        elif "facilities" in link["href"]:
            important_links["Facilities"] = link["href"]
    
    college_data.append({
        "College Name": college_name,
        "NIRF Rank": nirf_rank,
        "Rating": rating,
        "Ownership": ownership,
        "Fees": fees,
        "Admission Link": important_links.get("Admission", "N/A"),
        "Placement Link": important_links.get("Placement", "N/A"),
        "Courses Link": important_links.get("Courses", "N/A"),
        "Facilities Link": important_links.get("Facilities", "N/A")
    })

# Convert to DataFrame and save to CSV
df = pd.DataFrame(college_data)
df.to_csv("colleges_data.csv", index=False)

print("Data saved successfully to colleges_data.csv")
print(df)
