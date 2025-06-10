import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")  # Optional: to start Chrome maximized
options.add_argument("--disable-infobars")  # Optional: to disable info bars
options.add_argument("--disable-extensions")  # Optional: to disable extensions

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Open the URL
url = 'https://www.att.jobs/search-jobs/analyst/United%20States/117/1/2/6252001/39x76/-98x5/50/2'
driver.get(url)

# Step 2: Handle the pop-up (e.g., GDPR consent or other overlay)
try:
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "igdpr-alert"))  # Wait for the GDPR alert to be visible
    )
    close_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")  # Find Accept button
    close_button.click()  # Click to accept
    time.sleep(2)  # Wait for the pop-up to disappear
except Exception as e:
    print(f"No pop-up appeared or it was already closed: {e}")

# Step 3: Click the "Show All" button to load all job listings
try:
    show_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-show-all'))
    )
    show_all_button.click()  # Click the "Show All" button
    time.sleep(5)  # Wait for the content to load after clicking
except Exception as e:
    print(f"Error clicking the 'Show All' button: {e}")

# Step 4: Parse the page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Step 5: Extract job listings from the section
section = soup.find('section', {'id': 'search-results-list'})
job_listings = []

if section:
    job_elements = section.find_all('li')  # Extract all <li> elements within this section
    for job in job_elements:
        # Extract job title and location
        job_title_tag = job.find('h2', class_='headline__small')
        job_title = job_title_tag.get_text(strip=True) if job_title_tag else 'N/A'


        # Extract job link
        job_link = job_title_tag.find('a')['href'] if job_title_tag and job_title_tag.find('a') else 'N/A'

        if job_link != 'N/A':
            # Open job details in a new tab
            main_window = driver.current_window_handle
            driver.execute_script(f"window.open('https://www.att.jobs{job_link}', '_blank');")
            time.sleep(3)  # Wait for the new tab to load

            # Switch to the new tab and extract job details
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)

            # Parse the job details page
            job_detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract job description and other details
            job_location_tag = job_detail_soup.find('p', class_='section11__location')
            job_location = job_location_tag.get_text(strip=True) if job_location_tag else 'N/A'

            job_description = job_detail_soup.find('div', class_='ats-description').find_all('p')[1].get_text(separator="\n", strip=True)

            # Extract Key Roles and Responsibilities
            key_roles_header = job_detail_soup.find('b', string=lambda text: text and 'Key Roles and Responsibilities' in text)
            key_roles_text = ""
            if key_roles_header:
                key_roles = key_roles_header.find_next('ul')
                key_roles_text = "\n".join([li.get_text(strip=True) for li in key_roles.find_all('li')])

            # Extract Experience
            experience_header = job_detail_soup.find('b', string=lambda text: text and 'Experience' in text)
            experience_text = ""
            if experience_header:
                experience = experience_header.find_next('ul')
                experience_text = "\n".join([li.get_text(strip=True) for li in experience.find_all('li')])


            # Extract Perks and Benefits
            perks_text = ""
            perks_header = job_detail_soup.find('b', string=lambda text: text and 'Joining our team comes with amazing perks and benefits:' in text)
            if perks_header:
                perks = perks_header.find_next('ul')
                perks_text = "\n".join([li.get_text(strip=True) for li in perks.find_all('li')])



            # Extract Job ID
            job_id = job_detail_soup.find('span', class_='job-id job-info').get_text(strip=True).split(' ')[1]

            # Extract Date Posted
            date_posted = ""
            date_posted_header = job_detail_soup.find('span', class_='job-date job-info')
            if date_posted_header:
                date_posted = date_posted_header.get_text(strip=True).split("Date posted")[-1].strip()

            # Append all extracted data to job_listings
            job_listings.append({
                'Job Title': job_title,
                'Job Location': job_location,
                'Job Link': f'https://www.att.jobs{job_link}',
                'Job Description': job_description,
                'Key Roles and Responsibilities': key_roles_text,
                'Experience': experience_text,
                'Perks and Benefits': perks_text,
                'Job ID': job_id,
                'Date Posted': date_posted
            })

            # Close the new tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(main_window)

# Step 6: Convert job listings to a DataFrame and Export to Excel
df = pd.DataFrame(job_listings)
df.to_excel('att_job_details_divya.xlsx', index=False)

# Close the browser window
driver.quit()

print("Job details have been saved to 'att_job_details_divya.xlsx'")
