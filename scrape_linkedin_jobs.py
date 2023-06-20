from bs4 import BeautifulSoup
import pandas as pd
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

url = 'https://be.linkedin.com/jobs/big-data-jobs-brussels?countryRedirected=1'

 # Set up Firefox webdriver
options = Options()
options.headless = False  # Set to True if you don't want the browser to open visibly
driver = webdriver.Firefox(options=options)  # Replace with appropriate path to Firefox WebDriver

# Load the page
driver.get(url)
# Wait for the page to load and scroll to the bottom to trigger dynamic loading
time.sleep(3)  # Adjust sleep duration as needed

# Simulate scrolling to load more job listings
body = driver.find_elements(By.TAG_NAME,'body')
num_scrolls = 8  # Adjust the number of scrolls based on the number of job listings you want to retrieve

for _ in range(num_scrolls):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)  # Adjust sleep duration as neede

# Bs4 to scrape our page
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all elements of researched jobs
liste = soup.find('ul', class_='jobs-search__results-list')
results = liste.find_all('li')

# Store rows in dictionary 
jobs =[]
data={}
for result in results:
    data = {
        'job_title': result.find('h3',class_="base-search-card__title").text.strip(),
        'co_name': result.find('h4', class_='base-search-card__subtitle').text.strip(),
        'Location':result.find('span', class_='job-search-card__location').text.strip(),
        'url': result.find('a')['href']
    }
    jobs.append(data)

# Close browser
driver.quit()

# Get in a pandas dataframe
df = pd.DataFrame(jobs)
print(df)

# Cretae .csv file
df.to_csv('scrapper-jobs-be.csv', index=False)

# xml_data= df.to_xml()
# with open('jobs-data-be.xlsx', 'w') as file:
#     file.write(xml_data)