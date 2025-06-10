import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

# Ensure webdriver_manager downloads the correct version of ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the URL
url = "https://jobs.aa.com/search/?q=Analyst&locationsearch=united+states&pageNumber=0&facetFilters=%7B%7D&sortBy=&markerViewed=&carouselIndex="
driver.get(url)

def extract_section_data(soup, heading):
    section = soup.find('h2', string=lambda text: text and heading in text)
    if section:
        paragraph = section.find_next('div')
        if paragraph:
            return paragraph.get_text(strip=True)
    return None

def extract_list_data(soup, heading):
    section = soup.find('b', string=lambda text: text and heading in text)
    if section:
        ul = section.find_next('ul')
        if ul:
            first_li = ul.find('li')
            return first_li.text.strip() if first_li else None
    return None

# Function to scrape data from the current page and click the "Next" button
def scrape_page():
    # Wait for the page to load completely
    time.sleep(3)

    # Parse the page with BeautifulSoup to extract the section containing the job listings
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract job listings
    job_listings = []
    section = soup.find('div', {'class': 'JobsSearch_searchResultContainer__6tXwz'})
    if section:
        job_elements = section.find_all('li', class_='JobsList_jobCard__8wE-Z')

        for job in job_elements:
            job_details = {}

            job_title_tag = job.find('a', class_='jobCardTitle JobsList_jobCardTitle__pRNjw')
            job_details['Job Title'] = job_title_tag.get_text(strip=True) if job_title_tag else 'N/A'

            footer = job.find('div', {'data-testid': 'jobCardFooter'})
            if footer:
                footer_divs = footer.find_all('div', class_='JobsList_jobCardFooterDesktop__hP+-D')

                if len(footer_divs) >= 4:
                    job_details['Job Location'] = footer_divs[0].find_all('span')[1].text.strip() if len(footer_divs[0].find_all('span')) > 1 else 'N/A'
                    job_details['Country'] = footer_divs[1].find_all('span')[1].text.strip() if len(footer_divs[1].find_all('span')) > 1 else 'N/A'
                    job_details['Date Posted'] = footer_divs[2].find_all('span')[1].text.strip() if len(footer_divs[2].find_all('span')) > 1 else 'N/A'
                    job_details['Job Code'] = footer_divs[3].find_all('span')[1].text.strip() if len(footer_divs[3].find_all('span')) > 1 else 'N/A'

            job_link = job.find('a')['href'] if job.find('a') else 'N/A'
            job_details['Job Link'] = job_link

            if job_link != 'N/A':
                main_window = driver.current_window_handle
                driver.execute_script(f"window.open('{job_link}', '_blank');")
                time.sleep(3)

                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)

                time.sleep(3)

                job_detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

                job_details["Intro"] = extract_section_data(job_detail_soup, "Intro")
                job_details["Why you'll love this job"] = extract_section_data(job_detail_soup, "Why you'll love this job")
                job_details["What you'll do"] = extract_section_data(job_detail_soup, "What you'll do")
                job_details["Minimum Qualifications"] = extract_list_data(job_detail_soup, "Minimum Qualifications- Education & Prior Job Experience")
                job_details["Preferred Qualifications"] = extract_list_data(job_detail_soup, "Preferred Qualifications- Education & Prior Job Experience")
                job_details["Skills, Licenses & Certifications"] = extract_list_data(job_detail_soup, "Skills, Licenses & Certifications")
                job_details["What you'll get"] = extract_section_data(job_detail_soup, "What you'll get")

                driver.close()
                driver.switch_to.window(main_window)

            job_listings.append(job_details)

    return job_listings


# Main scraping loop to handle pagination
all_job_listings = []

while True:
    # Scrape the current page
    job_listings = scrape_page()
    all_job_listings.extend(job_listings)

    try:
        # Use WebDriverWait to explicitly wait for the "Next" button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="goToNextPageBtn"]'))
        )
        # Check if the "Next" button is visible and clickable
        if next_button.is_enabled():
            next_button.click()
            time.sleep(3)  # Wait for the page to load after clicking "Next"
        else:
            print("No more pages to scrape.")
            break
    except Exception as e:
        break

# Convert to DataFrame and Export to Excel
df = pd.DataFrame(all_job_listings)
df.to_excel('Equinox_job_details.xlsx', index=False)

# Close the browser window
driver.quit()

print("Job details with pagination have been saved to 'job_details_with_footer_and_pagination.xlsx'")
