#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Example of scraping from Indeed
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 

import pandas as pd
import numpy as np
import time
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Create function to retrieve job URLs by page
def scan_page_jobs(driver, URL, url_pre):
    driver.get(URL)
    
    # Get full list
    job_locator = str('.//a[@class="jcs-JobTitle css-jspxzf eu4oa1w0"]/span')
    job_spans = driver.find_elements(By.XPATH, job_locator)

    # Extract from elements
    job_titles = []; job_urls = []; job_ids = []
    for e in job_spans:
        title_ = None
        title_ = e.get_attribute('title')
        if title_:
            job_titles.append(e.get_attribute('title'))
        else:
            job_titles.append('')
    
        jk_ = None
        jk_ = e.get_attribute('id')
        if jk_:
            jk_ = jk_.replace('jobTitle-','')
            job_ids.append(jk_)
            job_urls.append(url_pre+jk_)
        else:
            job_urls.append('')
    
    # Get next page URL
    next_page_url = None
    try:
        next_page_a = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
    except NoSuchElementException:
        next_page_a = None

    if next_page_a:
        next_page_url = next_page_a.get_attribute('href')
    
    # Return lists
    return job_ids, job_titles, job_urls, next_page_url

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Scrape the job urls list
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
driver = None
driver = webdriver.Safari()

# Entry point URLs
url_ny_data = 'https://www.indeed.com/jobs?q=data&l=New+York%2C+NY&fromage=14'

# Input variables!
location_filename = 'ny'
location_data = 'New York, US'
url_used = url_ny_data
target_len = 300 # jobs to be scraped

# Initialize empty df
Job_Info = pd.DataFrame({'Job ID':[],'Job Title':[], 'Job URL':[]})

# Proceed till target len
st_ = time.time()
print("-------- Start")
iterations = 0
while len(list(Job_Info['Job ID'])) < target_len:
    job_url_prefix = str('https://www.indeed.com/viewjob?jk=')
    
    # Calculate destination URL
    if iterations==0:
        #dest_url = url_ny_data # Entry page URL
        dest_url = url_used
    else: # Go to next page ULR (from previous iteration)
        if next_page_url:
            dest_url = next_page_url
        else:
            break
    # Call function
    job_ids, job_titles, job_urls, next_page_url = scan_page_jobs(driver, dest_url, job_url_prefix)
    # Append to overall df
    Job_Info_i = pd.DataFrame({'Job ID':job_ids,'Job Title':job_titles, 'Job URL':job_urls})
    Job_Info = pd.concat([Job_Info, Job_Info_i], ignore_index=True)
    # Print to track progress
    elapsed_ = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-st_))
    print(":: {} job-urls scraped in: {}".format(len(list(Job_Info['Job ID'])), elapsed_))
    # Add waiting time
    time.sleep(round(random.uniform(0.7, 3.5), 1))
    iterations += 1

# Add locations on each row
main_loc = [str(location_data)] * len(list(Job_Info['Job ID']))
Job_Info['Main Location'] = main_loc
    
print("-------- Completed!!")
driver.quit()


#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Scrape job descriptions
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
driver = None
driver = webdriver.Safari()

Job_Descr = []; Company_Name = []; Salary = []

st_ = time.time()
last_print = 0
print("-------- Start")
for j in list(Job_Info['Job URL']):
    driver.get(str(j))
        
    # Scrape Employer
    try:
        Company_Name.append(driver.find_element(By.CSS_SELECTOR, 'div[data-company-name="true"]').text)
    except NoSuchElementException:
        Company_Name.append('')
        
    # Scrape Salary
    try:
        Salary.append(driver.find_element(By.XPATH, './/div[@id="salaryInfoAndJobType"]/span').text)
    except NoSuchElementException:
        Salary.append('')
        
    # Scrape JD
    try:
        Job_Descr.append(driver.find_element(By.CSS_SELECTOR, 'div[id="jobDescriptionText"]').text)
    except NoSuchElementException:
        Job_Descr.append('')
    
    if len(Company_Name) - last_print >= 15:
        elapsed_ = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-st_))
        print(":: {} job details scraped in: {}".format(len(Company_Name), elapsed_))
        last_print = len(Company_Name)
    time.sleep(round(random.uniform(0.7, 3.5), 1))
        
Job_Info['Company_Name'] = Company_Name
Job_Info['Salary'] = Salary
Job_Info['Job Description'] = Job_Descr

print("-------- Completed!!")
# Save to csv
today = str(date.today()).replace('-','')
_Path = r'/Users/name/Desktop'
Job_Info.to_csv(_Path+'/jobs_info_'+location_filename+'_'+today+'.csv', header=True, index=False, sep='|', mode='w')
driver.quit()
