from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re, time, csv

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Dictionary codes to attach to URL to get different apartments based on amenities
amenity_dict = {
     "Borehole": 837,
    "fully furnished": 880,
    "Swimming Pool": 863,
    "Club House": 32453,
    "Double Storey": 843,
    "Entertainment Area": 841,
    "Fitness Center": 3425435,
    "Flatlet /Cottage": 840,
    "Good Zesa": 853,
    "Gravel Roads": 325345,
    "Internet Connection": 838,
    "Municipal Water": 847,
    "Sewer System": 453245,
    "Solar System": 43533,
    "Split Level": 849,
    "Tarred Roads": 43254,
    "Carpot": 857,
    "Electric Fence": 859,
    "Electric Gate": 861,
    "Garden": 855,
    "Parking Bay": 1000004,
    "Paved": 34252,
    "Tiled": 1000000,
    "Tennis Code": 865,
    "Verandah": 867,
    "Walled": 869,
    "Water Tank": 882,
    "Workshop": 1000003,
    "Air Condition": 871,
    "Burglar Alarm": 873,
    "Fireplace": 878,
    "Fitted Kitchen": 876,
    "Fully Carpeted": 874,
    "Main En Suite": 1000001,
    "Study/ Office": 1000002,
    "Wooden floor": 324554
}

# Function to get listings by amenity
def listings_by_amenity(driver, amenity_dict):
    all_listings = {}
    for descriptor, url_code in amenity_dict.items():
        try:
            # Construct URL with amenity code
            url = f"https://www.property.co.zw/property-for-sale/harare?amenities={url_code}"
            driver.get(url)
            time.sleep(5)  # Wait for the page to load, adjust as necessary

            # Parse the page source with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Find all div tags with IDs that consist of numbers
            listings_div_tags = soup.find_all('div', id=re.compile(r'^\d+$'))

            # Create a list for the descriptor and add the listing IDs
            listings = []
            for div in listings_div_tags:
                div_id = div.get('id')
                listings.append(div_id)
            
            # Store the listings in the dictionary with the descriptor as the key
            all_listings[descriptor] = listings

            print(f"Collected {len(listings)} listings for {descriptor}")
        except Exception as e:
            print(f"Error collecting listings for {descriptor}: {e}")

    return all_listings

# Example usage
if __name__ == "__main__":
    try:
        # Call the function to get listings by amenity
        listings = listings_by_amenity(driver, amenity_dict)

        # Write the listings to the CSV file
        with open('amenities_file.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Amenity', 'id_list'])
            for amenity, id_list in listings.items():
                writer.writerow([amenity, ', '.join(id_list)])

        print("CSV file has been created successfully.")
    finally:
        # Close the WebDriver
        driver.quit()
