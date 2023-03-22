import csv
import requests
from bs4 import BeautifulSoup

# Define the URL for the initial search page
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'

# Set the number of pages to scrape
num_pages = 20

# Set up the CSV file for writing the data
with open('amazon_data.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    # Loop through each search results page and scrape the required information
    for page in range(1, num_pages + 1):
        url = base_url + str(page)

        # Send a GET request to the search results page and get the HTML response
        response = requests.get(url)

        # Use BeautifulSoup to parse the HTML response and extract the desired information
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the search result items on the page
        search_results = soup.find_all('div', {'class': 's-result-item'})

        # Loop through each search result item and extract the desired information
        for result in search_results:
            try:
                # Get the URL of the product
                product_url = 'http://www.amazon.in' + result.find('a', {'class': 'a-link-normal'})['href']
                
            except:
                product_url = ''

            try:
                # Get the name of the product
                product_name = result.find('span', {'class': 'a-size-medium'}).text.strip()
                
            except:
                product_name = ''
            try:
                # Get the price of the product
                product_price = result.find('span', {'class': 'a-price-whole'}).text.strip()
            except:
                product_price = ''
            try:
                # Get the rating of the product
                rating = result.find('span', {'class': 'a-icon-alt'}).text.strip()
            except:
                rating = ''
            try:
                # Get the number of reviews of the product
                num_reviews = result.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text.strip()
            except:
                num_reviews = ''

            # Send a GET request to the product page and get the HTML response
            try:
                product_response = requests.get(product_url)

                # Use BeautifulSoup to parse the HTML response and extract the desired information
                product_soup = BeautifulSoup(product_response.content, 'html.parser')
                try:
                    # Get the description of the product
                    description = product_soup.find('div', {'id': 'feature-bullets'}).text.strip()
                except:
                    description = ''
                try:
                    # Get the ASIN of the product
                    asin = product_soup.find('th', string='ASIN').find_next_sibling('td').text.strip()
                except:
                    asin = ''
                try:
                    # Get the product description
                    product_description = product_soup.find('div', {'id': 'productDescription'}).text.strip()
                except:
                    product_description = ''
                try:
                    # Get the manufacturer of the product
                    manufacturer = product_soup.find('th', string='Manufacturer').find_next_sibling('td').text
                except:
                    manufacturer = ''
            
            except:
                product_response = ''
            
            writer.writerow({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': rating,
                'Number of Reviews': num_reviews,
                'Description': description,
                'ASIN': asin,
                'Product Description': product_description,
                'Manufacturer': manufacturer
            })

