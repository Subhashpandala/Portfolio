import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configure the webdriver with appropriate options
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment for headless mode

# Ensure webdriver_manager downloads the correct version of ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Open the URL
url = 'https://careers.ti.com/search-jobs/?keyword=analyst&location=United%20States&country=US&radius=25'
driver.get(url)

# Step 2: Wait for the page to load completely
# Use WebDriverWait to wait for the job listings section to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'widget-jobsearch-results-list'))
)

# Parse the HTML content using BeautifulSoup
html_content = driver.page_source  # Get the current page source from Selenium
soup = BeautifulSoup(html_content, 'html.parser')

# Find the section containing job listings
section = soup.find('div', {'id': 'widget-jobsearch-results-list'})

# Initialize a list to store job listings
job_listings = []

if section:
    # Extract all job elements
    job_elements = section.find_all('div', class_='job')

    for job in job_elements:
        # Extract job title
        job_title_tag = job.find('div', class_='jobTitle')
        job_title = job_title_tag.get_text(strip=True) if job_title_tag else 'N/A'

        # Extract job location
        job_location_tag = job.find('div', class_='joblist-location')
        job_location = job_location_tag.get_text(strip=True) if job_location_tag else 'N/A'

        # Extract job posting date
        job_date_tag = job.find('div', class_='joblist-posdate')
        job_date = job_date_tag.get_text(strip=True) if job_date_tag else 'N/A'

        # Extract job link
        job_link_tag = job.find('a', href=True)
        job_link = job_link_tag['href'] if job_link_tag else 'N/A'

        # Open the job link in a new tab if the link is available
        if job_link != 'N/A':
            main_window = driver.current_window_handle
            driver.execute_script(f"window.open('{job_link}', '_blank');")
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  # Wait for the new tab to load
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)

            # Extract job details from the job page
            job_detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract Business Summary
            job_summary = ""
            job_summary_header = job_detail_soup.find('b', string=lambda text: text and 'Business Summary' in text)
            if job_summary_header:
                job_summary = job_summary_header.find_parent('p').find_next('p').text.strip()

            # Extract responsibilities
            responsibilities = []
            responsibilities_header = job_detail_soup.find('span', string=lambda text: text and 'Primary Responsibilities:' in text)
            if responsibilities_header:
                responsibilities = [li.text.strip() for li in responsibilities_header.find_next('ul').find_all('li')]

            # Extract minimum requirements
            minimum_requirements = []
            min_req_header = job_detail_soup.find(['strong','p'], string=lambda text: text and 'Minimum requirements' in text)
            if min_req_header:
                minimum_requirements = [li.text.strip() for li in min_req_header.find_next('ul').find_all('li')]

            # Extract preferred qualifications
            preferred_qualifications = []
            pref_qual_header = job_detail_soup.find('strong', string=lambda text: text and 'Preferred qualifications' in text)
            if pref_qual_header:
                preferred_qualifications = [li.text.strip() for li in pref_qual_header.find_parent('p').find_next('ul').find_all('li')]

            # Extract Why TI
            why_ti = []
            why_ti_tag = job_detail_soup.find('b', string=lambda text: text and "Why TI?" in text)
            if why_ti_tag:
                why_ti = [li.text.strip() for li in why_ti_tag.find_parent('p').find_next('ul').find_all('li')]

            # Store job details
            job_listings.append({
                'Job Title': job_title,
                'Job Location': job_location,
                'Posted on': job_date,
                'Job Link': job_link,
                'Job Summary': job_summary,
                'Primary Responsibilities': "\n".join(responsibilities),
                'Minimum Requirements': "\n".join(minimum_requirements),
                'Preferred Qualifications': "\n".join(preferred_qualifications),
                'Why TI': "\n".join(why_ti)
            })

            # Close the job detail tab and switch back to the main window
            driver.close()
            driver.switch_to.window(main_window)

# Step 6: Convert to DataFrame and Export to Excel
df = pd.DataFrame(job_listings)
df.to_excel('Texas_instruments_job_details.xlsx', index=False)

# Close the browser window
driver.quit()

print("Job details have been saved to 'Ti_job_details.xlsx'")
