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

# Ensure webdriver_manager downloads the correct version of ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Open the URL
url = 'https://www.ibm.com/in-en/careers/search?field_keyword_05[0]=United%20States&q=analyst'
driver.get(url)


# Step 3: Wait for the page to load completely
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.bx--card-group__cards__col'))
)

# Step 4: Parse the page with BeautifulSoup to extract the section containing the job listings
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Step 5: Extract only the <div> elements under the specific section
section = soup.find('div', {'class': 'bx--card-group__cards__row bx--row--condensed'})
job_listings = []

# Function to extract sections (Introduction, Responsibilities, etc.)
def extract_section(tag, section_title):
    if tag:
        next_tag = tag.find_next(['br', 'p', 'ul'])
        return next_tag.get_text(strip=True) if next_tag else ""
    return ""

if section:
    # Extract all job elements
    job_elements = section.find_all('div', class_='bx--card-group__cards__col')
    
    for job in job_elements:
        # Extract job title and location
        job_title_tag = job.find('div', class_='bx--card__heading')
        job_title = job_title_tag.get_text(strip=True) if job_title_tag else ''
        job_link = job.find('a')['href'] if job_title_tag else ''

        if job_link:
            main_window = driver.current_window_handle
            driver.execute_script(f"window.open('{job_link}', '_blank');")
            time.sleep(3)  # Wait for the new tab to load
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)

            # Extract job details from the job page
            job_detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract job sections
            
            requirements_tag = job_detail_soup.find('span', string="Required Technical and Professional Expertise")
            preferred_expertise_tag = job_detail_soup.find('span', string="Preferred Technical and Professional Expertise")

            # Use the extract_section function to get job details
            required_expertise = extract_section(requirements_tag, "Required Expertise")
            preferred_expertise = extract_section(preferred_expertise_tag, "Preferred Expertise")

            # Extract job specification details (Role, Location, Category, etc.)
            job_spec_section = job_detail_soup.find_all('div', {'class': 'sidebar-lists-item'})
            
            # Extract information from sidebar details
            details = {}
            for item in job_spec_section:
                text = item.get_text(strip=True)
                if 'Role:' in text:
                    details['Role'] = text.replace('Role:', '').strip()
                elif 'Location:' in text:
                    details['Location'] = text.replace('Location:', '').strip()
                elif 'Category:' in text:
                    details['Category'] = text.replace('Category:', '').strip()
                elif 'Employment Type:' in text:
                    details['Employment Type'] = text.replace('Employment Type:', '').strip()
                elif 'Travel Required:' in text:
                    details['Travel Required'] = text.replace('Travel Required:', '').strip()
                elif 'Contract Type:' in text:
                    details['Contract Type'] = text.replace('Contract Type:', '').strip()
                elif 'Company:' in text:
                    details['Company'] = text.replace('Company:', '').strip()
                elif 'Req ID:' in text:
                    details['Req ID'] = text.replace('Req ID:', '').strip()
                elif 'Projected Minimum Salary:' in text:
                    details['Projected Minimum Salary'] = text.replace('Projected Minimum Salary:', '').strip()
                elif 'Projected Maximum Salary:' in text:
                    details['Projected Maximum Salary'] = text.replace('Projected Maximum Salary:', '').strip()
                elif 'Date Posted:' in text:
                    details['Date Posted'] = text.replace('Date Posted:', '').strip()

            # Append job details to list
            job_listings.append({
                'Job Title': job_title,
                'Job Link': job_link,
                'Required Expertise': required_expertise,
                'Preferred Expertise': preferred_expertise,
                'Role': details.get('Role', ''),
                'Location': details.get('Location', ''),
                'Category': details.get('Category', ''),
                'Employment Type': details.get('Employment Type', ''),
                'Travel Required': details.get('Travel Required', ''),
                'Contract Type': details.get('Contract Type', ''),
                'Company': details.get('Company', ''),
                'Req ID': details.get('Req ID', ''),
                'Projected Minimum Salary': details.get('Projected Minimum Salary', ''),
                'Projected Maximum Salary': details.get('Projected Maximum Salary', ''),
                'Date Posted': details.get('Date Posted', '')
            })

            # Close the new tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(main_window)

# Step 6: Convert to DataFrame and Export to Excel
df = pd.DataFrame(job_listings)
df.to_excel('ibm_job_details.xlsx', index=False)

# Close the browser window
driver.quit()

print("Job details have been saved to 'ibm_job_details.xlsx'")
