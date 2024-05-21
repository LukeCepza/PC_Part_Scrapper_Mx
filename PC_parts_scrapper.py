import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests.exceptions import RequestException

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
]

def get_soup(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            # Randomly select a User-Agent
            headers = {
                "User-Agent": random.choice(user_agents),
            }

            # Use requests session to handle cookies and headers
            session = requests.Session()
            session.headers.update(headers)

            # Use Selenium to handle dynamic content loading
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument(f"user-agent={headers['User-Agent']}")
            driver = webdriver.Chrome(options=options)

            driver.get(url)
            time.sleep(1)  # Wait for the content to load, adjust as needed

            page_source = driver.page_source
            driver.quit()

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # Introduce a random delay to mimic human behavior
            time.sleep(random.uniform(1, 2))  # Sleep for a random duration between 1 and 3 seconds

            print(url)
            return soup

        except RequestException as e:
            retries += 1
            print(f"Request failed: {e}. Retrying ({retries}/{max_retries})...")
            time.sleep(2 ** retries)  # Exponential backoff

        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/{max_retries})...")
            time.sleep(2 ** retries)  # Exponential backoff

    print(f"Failed to fetch {url} after {max_retries} retries.")
    return None

def extract_products_amazon(soup, limit = 9999):
    products = []
    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    count = 0
    for container in product_containers:
        if count >= limit:
            break        
        try:
            model = container.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
            price = container.find('span', {'class': 'a-offscreen'}).text
            link = container.find('a', {'class': 'a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
            full_link = "https://www.amazon.com.mx" + link
            products.append({'Model': model, 'Price': price, 'Link': full_link})
            count += 1
        except AttributeError:
            continue

    return products

def get_data_amazon(data, components,websites):
    for part, query in components.items():
        url = websites["Amazon"] + query.replace(" ", "+")
        soup = get_soup(url)
        if soup:
            print("Retreived succesfully.")
            products = extract_products_amazon(soup, limit = 5)
            for product in products:
                data.append(["Amazon", part, query, product['Price'], product['Model'], product['Link']])
        else:
            print("Failed to retrieve the page.")
    return data


def extract_products_cyberpuerta(soup):
    products = []
    product_containers = soup.find_all('div', {'class': 'emproduct_right'})
    for container in product_containers:
        try:
            model = container.find('a').text
            price = container.find('label', {'class': 'price'}).text
            link = container.find('a')['href']
            full_link = link
            products.append({'Model': model, 'Price': price, 'Link': full_link})
        except AttributeError:
            continue

    return products

def get_data_cyberpuerta(data, components, websites):    
    for part, query in components.items():
        url = websites["Cyberpuerta"] + query.replace(" ", "+")
        soup = get_soup(url)
        if soup:
            print("Retreived succesfully.")
            products = extract_products_cyberpuerta(soup)
            for product in products:
                data.append(["Cyberpuerta", part, query, product['Price'], product['Model'],  product['Link']])
        else:
            print("Failed to retrieve the page.")
    return data

def extract_google_shopping_data(soup, limit = 9999):
    products = []
    product_containers = soup.select('div.sh-dgr__grid-result')
    count = 0
    for container in product_containers:
        if count >= limit:
            break        
        try:
            model = container.find('h3', {'class': 'tAxDx'}).text.strip()
            price = container.find('span', {'class': 'a8Pemb OFFNJ'}).text.strip()
            link = container.find('a', {'class': 'shntl'})['href']

            # Ensure the link is complete
            if link.startswith("/url"):
                full_link = "https://www.google.com" + link
            elif link.startswith("http"):
                full_link = link
            else:
                continue

#            full_link = "https:" + link.split("https:")[1]
            products.append({'Model': model, 'Price': price, 'Link': full_link})
            count += 1
        except AttributeError:
            continue
    return products


def get_data_google_shopping(data, components, websites):
    for part, query in components.items():
        url = websites["Google"] + query.replace(" ", "+")
        soup = get_soup(url)
        if soup:
            print("Retreived succesfully.")
            products = extract_google_shopping_data(soup, limit = 15)
            for product in products:
                data.append(["Google", part, query, product['Price'], product['Model'],  product['Link']])
        else:
            print("Failed to retrieve the page.")
    return data

# Updated clean_price function to handle various formats
def clean_price(price):

    # Check if the price starts with a dollar sign
    if price.startswith('$'):
        # Remove the dollar sign and any commas, then convert to float
        price = price.replace('$', '').replace(',', '')
        try:
            return float(price)
        except ValueError:
            return float('NaN')
    elif price.startswith('M'):
        # Remove the dollar sign and any commas, then convert to float
        price = price.replace('MXN', '').replace(',', '')
        try:
            return float(price)
        except ValueError:
            return float('NaN')
    else:
        # Return None for non-monetary values
        return float('NaN')
    
