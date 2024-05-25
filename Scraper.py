from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from func import   extract_real_estate_data, next_page
import re , time , csv 

#columns for csv 
keys_list = [
    "ID",
    "Listing Ref",
    "Location and Sector",
    "Listing Price",
    "Listing Description",
    "Bedrooms",
    "Bathrooms",
    "Area of Living Space",
    "Total Land Area",
    "Realtor",
    "Real Estate Company"
]

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# URL of the website to scrape
url = "https://www.property.co.zw/property-for-sale/harare"
driver.get(url)

try:
    # Wait until the pages number element is present
    max_pages_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[14]/div[1]/div[1]/div[5]/nav/ul/li[8]/a'))
    )
    # Extract the text value and convert it to an integer
    max_pages_text = max_pages_element.text
    max_clickthrough = int(max_pages_text) - 1
    print(f"Max pages: {max_clickthrough}")

#loop should start here
    for page in range(max_clickthrough):
        # Wait until the listings load element is present
        listing_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'result-cards'))
        )

        # Once the element is loaded, get the page source and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Find all div tags with IDs that consist of numbers
        listings_div_tags = soup.find_all('div', id=re.compile(r'^\d+$'))

        #Open Csv file
         # Write all real estate data to the CSV file
        with open('real_estate_data.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys_list)

            # Extract and print relevant information
            for div in listings_div_tags:
                div_id = div.get('id')
                print(div_id)
                real_estate_data = extract_real_estate_data(driver, div_id,soup)


                writer.writerow(real_estate_data)

            print("CSV file has been created successfully.")
                #print(real_estate_data)
        time.sleep(15)
        # Click the "Next" button to go to the next page
        next_page(driver)


    

finally:
    # Close the WebDriver
    driver.quit()

