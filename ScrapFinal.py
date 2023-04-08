from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title=soup.find("span", attrs={"id":'productTitle'}).text.strip()

    except AttributeError:
        title = ""

    return title

# Function to extract Product Price
def get_price(soup):

    try:
        price=soup.find("span", attrs={"class":'a-price'}).find("span", attrs={"class": "a-offscreen"}).text

    except AttributeError:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating=soup.find("span",attrs={'class':"a-size-medium a-color-base"}).text.strip()
        s=rating
        acc_rat=s[0]+s[1]+s[2]

    
    except AttributeError:
        acc_rat = ""	

    return acc_rat

# Function to extract Number of User Reviews
def get_descrip(soup):
    try:
        descrip=soup.find("div",attrs={'class':'a-expander-partial-collapse-content'}).text.strip()

    except AttributeError:
        descrip = ""	

    return descrip

# Function to extract Availability Status
def get_author(soup):
    try:
        author=soup.find("span", attrs={'class':'author notFaded'}).find("a",attrs={'class':"a-link-normal"}).text

    except AttributeError:
        author = ""	

    return author

if __name__ == '__main__':

    # add your user agent 
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.amazon.in/s?k=romantic+books&i=stripbooks&ref=nb_sb_ss_ts-doa-p_2_8"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"Title":[], "Price":[], "Rating":[],"Description":[], "Author":[],"LINK":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        linkz="https://www.amazon.com" + link
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['Title'].append(get_title(new_soup))
        d['Price'].append(get_price(new_soup))
        d['Rating'].append(get_rating(new_soup))
        d['Description'].append(get_descrip(new_soup))
        d['Author'].append(get_author(new_soup))
        d['LINK'].append(linkz)

    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['Title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Title'])
    amazon_df['Price'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Price'])
    amazon_df['Rating'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Rating'])
    amazon_df['Description'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Description'])
    amazon_df['Author'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Author'])
    amazon_df['LINK'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['LINK'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)