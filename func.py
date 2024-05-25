from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time,re

def extract_real_estate_data(driver, div_id,soup):
    # List of XPaths to extract
    xpaths = [
        '/div[5]/div[2]/div/div[1]',  # Location and Sector
        '/div[5]/div[1]/div[1]/a',     # Listing Price
        '/div[5]/div[2]/div/h2/a',   # Listing Description
        '/div[4]/div/a[2]'    # Realtor
       
    ]
     # List of regular expressions
    regex_list = [
        'bed\s+mr-2', #bedrooms
        'bath\s+mr-2',#bathrooms
        'building-area\s+mr-2\s+relative',#building-area
        'land-size\s+mr-2\s+relative(\s+hidden\s+md:inline)?',#land-size
        '(/for-[^"]*)',#Listing link references
        '(/estate-agents/[^"]+)' #Real Estate Company

    ]

    # Initialize variables
    location_and_sector = 0
    listing_price = 0
    listing_description = 0
    realtor = 0
    bedrooms = 0
    bathrooms = 0
    living_space_area = 0
    total_land_area = 0
    Listing_Link = None 
    real_estate_company = None
    

    # Iterate through the XPaths and assign the values to the corresponding variables
    for xpath in xpaths:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="{div_id}"]{xpath}'))
            )
            value = element.text
            if xpath == '/div[5]/div[2]/div/div[1]':
                location_and_sector = value
            elif xpath == '/div[5]/div[1]/div[1]/a':
                listing_price = value
            elif xpath == '/div[5]/div[2]/div/h2/a':
                listing_description = value
            elif xpath == '/div[4]/div/a[2]':
                realtor = value
        except Exception as e:
            print(f"Could not find element for div ID {div_id}: {e}")

            

    ##find bed element
    # Find the span tag using BeautifulSoup and the regular expression
    bed_tag = soup.find('div', id=div_id).find('span', class_=re.compile(regex_list[0]))
    # Check if bed_tag is not None (i.e., a span tag was found)
    if bed_tag is not None:
        bedrooms = bed_tag.text.strip()  # Remove any leading or trailing whitespace
    else:
        bedrooms = 0  # Set bedrooms to zero if no span tag is foun



     # Find the span tag using BeautifulSoup and the regular expression
    bath_tag = soup.find('div', id=div_id).find('span', class_=re.compile(regex_list[1]))
    # Check if bath_tag is not None (i.e., a span tag was found)
    if bath_tag is not None:
        bathrooms = bath_tag.text.strip()  # Remove any leading or trailing whitespace
    else:
        bathrooms = 0  # Set bathrooms to zero if no span tag is foun



     # Find the span living_space_area_tag using BeautifulSoup and the regular expression
    living_space_area_tag = soup.find('div', id=div_id).find('span', class_=re.compile(regex_list[2]))
    # Check if living_space_area_tag is not None (i.e., a span tag was found)
    if living_space_area_tag is not None:
        living_space_area = living_space_area_tag.text.strip()  # Remove any leading or trailing whitespace
    else:
        living_space_area = 0  # Set living_space_area to zero if no span tag is foun



    # Find the span total_area_tag using BeautifulSoup and the regular expression
    total_land_area_tag = soup.find('div', id=div_id).find('span', class_=re.compile(regex_list[3]))
    # Check if total_area_tag is not None (i.e., a span tag was found)
    if total_land_area_tag is not None:
        total_land_area = total_land_area_tag.text.strip()  # Remove any leading or trailing whitespace
    else:
        total_land_area= 0  # Set bedrooms to zero if no span tag is foun
    #print(bedrooms)


    # Find the a listing_link_tag using BeautifulSoup and the regular expression
    Listing_link_tag = soup.find('div', id=div_id).find('a', href=re.compile(regex_list[4]))
    # Check if  Listing_link_tag is not None (i.e., a a tag was found)
    if  Listing_link_tag is not None:
         Listing_Link  = Listing_link_tag['href'].strip()  # Remove any leading or trailing whitespace
    else:
         Listing_Link= None  # Set bedrooms to zero if no span tag is foun
    #print(Link_tag)


    #Find the name of the Real estate company using the img alt attribute
    real_estate_company_tag = soup.find('div', id=div_id).find('a', href=re.compile(regex_list[5])).find('img')
    # Check if  Listing_link_tag is not None (i.e., a a tag was found)
    if  real_estate_company_tag is not None:
         real_estate_company = real_estate_company_tag['alt'].strip()  # Remove any leading or trailing whitespace
    else:
         real_estate_company= None  # Set bedrooms to zero if no span tag is foun
    #print(Link_tag)


            
        

    # Return the data as a dictionary
    return {
        "ID": div_id,
        "Listing Ref": Listing_Link,
        "Location and Sector": location_and_sector,
        "Listing Price": listing_price,
        "Listing Description": listing_description,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Area of Living Space": living_space_area,
        "Total Land Area": total_land_area,
        "Realtor": realtor,
        "Real Estate Company": real_estate_company
        
        
       
    }

#Click to next page
def next_page(driver, wait_time=20):
    try:
        # Wait until the next page button is clickable
        next_page_button = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'a.next' ))
        )
        
        # Scroll to the next button if necessary
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).perform()

        # Perform a left-click explicitly
        actions.click(next_page_button).perform()
        
        # Additional wait to ensure the page loads
        time.sleep(5)
        print('Next Page ')
        
    except Exception as e:
        print(f"An error occurred: {e}")

         # Find the span tag using BeautifulSoup and the regular expression
                #span_tag = soup.find_all('span', class_=re.compile(f'{regx}'))