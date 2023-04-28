#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd


# In[ ]:





# ####  This project has educational porpuse and aims to analyze data related to houses on sale in the Queenstown-lake region. The goal is to predict the price of a house based on a set of features extracted from the Trade Me website.

# ### Address
# ##### Extract the addresses using BeautifulSoup and requests
# 

# In[2]:


# Extract the addresses using BeautifulSoup and requests

url_template = 'https://www.trademe.co.nz/a/property/residential/sale/otago/queenstown-lakes/search?sort_order=priceasc&property_type=apartment&property_type=house&property_type=townhouse&property_type=unit&page={}'

# Create an empty list to store all the addresses
address_list = []

# Loop through all pages of search results
for page_number in range(1, 12):  
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the addresses using the appropriate tag and class selector
    addresses = soup.find_all('tm-property-search-card-address-subtitle')

    # Extract the text content of each address and append it to the address_list
    for address in addresses:
        address_list.append(address.text.strip())

# Print the list of addresses
# print(address_list)
len(address_list)


# In[3]:


address_list


# In[111]:


address_list[175]


# In[4]:


# A list to try split, strip and append methods to extract neighborhood, district, and street
addrr = address_list[:5]


# In[5]:


# Store in a variable the splited addresses
ad3 = []
for i in address_list:    
    dire = i.split(',')
    ad3.append(dire)


# In[6]:


len(ad3)


# In[194]:


# ad3


# ### neighborhood

# In[7]:


# Extract the neighborhood
neighborhood = []
for l in ad3:
        neighborhood.append(l[len(l)-2])
    


# In[8]:


# neighborhood


# In[9]:


# A method for strip text
def strip_text(list_t):
    striped = []
    for i in list_t:
        striped.append(i.strip())
    return striped
        


# In[10]:


neighborhood1 = strip_text(neighborhood)


# In[11]:


len(neighborhood1)


# In[192]:


# neighborhood1


# In[12]:


# neighborhood1 = []
# for n in neighborhood:
#     neighborhood1.append(n.strip())


# In[13]:


# neighborhood1


# ###  district

# In[14]:


# Extract district
district = []
for l in ad3:
        district.append(l[len(l)-1])


# In[15]:


len(district)


# In[16]:


district1 = strip_text(district)


# In[17]:


# district1


# ### street

# In[18]:


# Extract street
street = []
for l in ad3:
        street.append(l[0])


# In[19]:


# street


# In[20]:


street1 = strip_text(street)


# In[21]:


len(street1)


# In[22]:


# street1


# In[110]:


# street1[175] == '8 Coal Pit Road'


# ### Geopy
# #### Import geopy to find the coordinates based on the addresses

# In[23]:


from geopy.geocoders import Nominatim


# In[24]:


from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderUnavailable
import time


# In[25]:


address_check = address_list


# In[26]:


# Some addresses have more than one number on the street number and the coordinate couldn't be found.
# To avoid this take only one number for the street
address_short = []
for a in address_check:
    if '/' in a:
        ad = a.split('/')[1]
        address_short.append(ad)
    else:
        address_short.append(a)


# In[27]:


len(address_short)


# In[28]:


address_short[:10]


# In[29]:


address_list[:10]


# In[30]:


# add_check = {'address_list':address_list , 'address_short':address_short }


# In[31]:


# address_df = pd.DataFrame(add_check)


# In[33]:


# address_df.head(10)


# In[ ]:





# #### Find the coordinates, latitude and longitude based on the addresses

# In[34]:


geolocator = Nominatim(user_agent="my11-app")
latitude_list = []
longitude_list = []
for l in address_short:
    
    try:
    
        location = geolocator.geocode(l, timeout=10)    
        if location:
            latitude_list.append(location.latitude)
            longitude_list.append(location.longitude)
        else:
            latitude_list.append('none')
            longitude_list.append('none')

    except GeocoderTimedOut:
        
        latitude_list.append('none')
        longitude_list.append('none')
    

               


# In[35]:


latitude_list


# In[36]:


len(latitude_list)


# In[37]:


len(longitude_list)


# #### For some addresses the coordinates were not found, this will completed manually using excel. 

# In[38]:


add_check = {'address_list':address_list , 'address_short':address_short, 'latitude':latitude_list, 'longitude':longitude_list }


# In[39]:


address_df = pd.DataFrame(add_check)


# In[40]:


address_df.head() #tail(15)


# In[126]:


# Save to csv address, latitude and longitude to completed manually on excel using google map
# address_df.to_csv('111address_long_short')


# In[ ]:





# In[135]:


# Read the file with the coodinates completed
df_lat_lon = pd.read_csv('add_lat_long_1.csv',delimiter=';',index_col=False)


# In[136]:


df_lat_lon.head()


# In[137]:


df_lat_lon.tail()


# #### Store in a separated variables the information needed to build later the final dataframe

# In[138]:


latitude_ult = df_lat_lon['latitude']


# In[147]:


latitude_ult.in


# In[141]:


longitude_ult = df_lat_lon['longitude']


# In[148]:


longitude_ult[:6]


# In[168]:


neighb_ult = df_lat_lon['Unnamed: 4']


# In[ ]:





# In[ ]:





# ### Folium
# #### import folium to plot coordinates on a map

# In[42]:


import folium
from IPython.display import display


# In[ ]:





# In[161]:


# dividing by to have the rigth format with the '.'
latitude_ult2 = latitude_ult/ 1000000


# In[163]:


# latitude_ult2


# In[165]:


# dividing by to have the rigth format with the '.'
longitude_ult2 = longitude_ult / 1000000


# In[166]:


# longitude_ult2 # latitude_ult2


# In[171]:


geolocator = Nominatim(user_agent="my22-app")

# # Create a map object centered on a location
mapa = folium.Map(tiles='OpenStreetMap',location=[-45.0485, 168.7], zoom_start=11)


# # Add multiple markers to the map object using a loop
for lat, lon, neighb in zip(latitude_ult2, longitude_ult2, neighb_ult):
    folium.Marker(location=[lat, lon], popup=neighb).add_to(mapa)
    

# Display the map object in the notebook
display(mapa)


# In[ ]:





# ### Bedrooms

# In[44]:


# Create an empty list to store all the bedrooms
bedroom_list = []

# Loop through all pages of search results
for page_number in range(1, 12):  # assume there are 10 pages of search results
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the addresses using the appropriate tag and class selector
    bedrooms = soup.find_all('tg-icon', alt="Bedrooms" )

    # Extract the text content of each address and append it to the address_list
    for bed in bedrooms:
        bed2 = bed.next_sibling.text
        bedroom_list.append(bed2)

# Print the list of addresses
#print(bedroom_list)


# In[45]:


len(bedroom_list)


# In[46]:


bedroom_list


# In[ ]:





# In[ ]:





# In[47]:


bedroom_list1 = []
for i in bedroom_list:
    num = re.sub('[^0-9\.]', '', i)
    if num == '':
        bedroom_list1.append(0)
    else:
        bedroom_list1.append(float(num))


# In[48]:


len(bedroom_list1)


# In[ ]:





# In[49]:


# bedroom_list1


# ### Bathrooms

# In[50]:


# Create an empty list to store all the bathrooms
bathroom_list = []

# Loop through all pages of search results
for page_number in range(1, 12):  # assume there are 10 pages of search results
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    listings_attr = soup.find_all('ul',class_="tm-property-search-card-attribute-icons__features")
    
    for l in listings_attr:      
        
        if l.find('tg-icon', alt="Bathrooms"):            
            bath = l.find('tg-icon', alt="Bathrooms").next_sibling.text
            bathroom_list.append(bath)
            #print('attr')
        else:
            #print('no attr')
            bathroom_list.append('None')

# Print the list 
#print(bathroom_list)
len(bathroom_list)


# In[ ]:





# In[51]:


bathroom_list1 = []
for i in bathroom_list:
    num = re.sub('[^0-9\.]', '', i)
    if num == '':
        bathroom_list1.append(0)
    else:
        bathroom_list1.append(float(num))


# In[52]:


len(bathroom_list1)


# In[ ]:





# ### Parking

# In[53]:


# Create an empty list to store all the parking
parking_list = []

# Loop through all pages of search results
for page_number in range(1, 12):  # assume there are 10 pages of search results
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    listings_attr = soup.find_all('ul',class_="tm-property-search-card-attribute-icons__features")
    
    for l in listings_attr:  # l.find('tg-icon', alt='Total parking'):        
        
        if l.find('tg-icon', alt="Total parking"):            
            bath = l.find('tg-icon', alt="Total parking").next_sibling.text
            parking_list.append(bath)
            #print('hay attr')
        else:
            #print('no hay attr')
            parking_list.append('None')

# Print the list 
# print(parking_list)
len(parking_list)
# len(listings_attr)


# In[54]:


parking_list


# In[55]:


par = parking_list[0]


# In[56]:


par


# In[ ]:





# In[57]:


nuw = re.sub('[^0-9\.]', '', par)


# In[58]:


nuw


# In[59]:


parking_list1 = []
for i in parking_list:
    num = re.sub('[^0-9\.]', '', i)
    if num == '':
        parking_list1.append(0)
    else:
        parking_list1.append(float(num))


# In[60]:


len(parking_list1)


# In[ ]:





# ### floor_area

# In[61]:


# Create an empty list to store all the floor_area
floor_area_list = []

# Loop through all pages of search results
for page_number in range(1, 12):  
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    listings_attr = soup.find_all('ul',class_="tm-property-search-card-attribute-icons__features")
    
    for l in listings_attr:         
        
        if l.find('tg-icon', alt="Floor area"):            
            bath = l.find('tg-icon', alt="Floor area").next_sibling.text
            floor_area_list.append(bath)
            #print('hay attr')
        else:
            #print('no hay attr')
            floor_area_list.append('None')

# Print the list 
#print(floor_area_list)
len(floor_area_list)


# In[62]:


# floor_area_list


# In[63]:


# Convert the floor area into float number deleting text 
# and assigning zero where floor area is not specified.
floor_area_list1 = []
for i in floor_area_list:
    num = re.sub('[^0-9\.]', '', i)
    if num == '':
        floor_area_list1.append(0)
    else:
        floor_area_list1.append(float(num)/10)


# In[64]:


floor_area_list1


# ### Price

# In[65]:


# <div _ngcontent-frend-c738="" class="tm-property-search-card-price-attribute__price">$765,000</div>


# In[66]:


# Create an empty list to store all prices
price_list = []

# Loop through all pages of search results
for page_number in range(1, 12): 
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the addresses using the appropriate tag and class selector
    prices = soup.find_all('div', class_="tm-property-search-card-price-attribute__price")

    # Extract the text content of each address and append it to the list
    for price in prices:
        price_list.append(price.text.strip())

# Print the list 
# print(price_list)
len(price_list)


# In[67]:


price_list


# In[68]:


# Try remove all non-numeric characters 
prr = price_list[13]


# In[69]:


prr


# In[70]:


nu = re.sub('[^0-9\.]', '', prr)


# In[71]:


nu


# In[72]:


na = float(nu)


# In[73]:


# Remove all non-numeric characters from each price using a regular expression. 
# Convert into float number and assigning 'none' where price is not specified.
price_list1 = []
for i in price_list:
    num = re.sub('[^0-9\.]', '', i)
    if num == '':
        price_list1.append('none')
    else:
        price_list1.append(float(num))


# In[74]:


price_list1


# In[75]:


len(price_list1)


# ### land_area

# In[76]:


# <tg-icon _ngcontent-frend-c735="" alt="Land area" name="house-land-area" size="small" class="tm-property-search-card-attribute-icons__metric-icon o-icon o-icon--size-16" aria-hidden="false"><tg-svg class="o-svg o-svg--scale-to-fill"><tg-house-land-area-small-svg class="ng-star-inserted"><svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" aria-labelledby="tg-c6b5c8cb-fc9a-e559-1eac-778bdb6766d7" preserveAspectRatio="xMinYMid meet" focusable="false" role="img"><path d="M7.64 1.26a.93.93 0 0 0-1.27 0l-6.1 6.1a.9.9 0 0 0 0 1.27l5.1 5.1a.93.93 0 0 0 1.27 0L8 12.37l2.36 2.36a.9.9 0 0 0 1.27 0l4.1-4.1a.9.9 0 0 0 0-1.27l-8.09-8.1zm2.46 10.67l-1.2-1.2V5.07l1.2 1.2v5.66zm-6-5.85v3.85L2.17 8 4.1 6.08zM6 11.83l-.1-.1V4.27L7 3.17l.1.1v7.46L6 11.83zm5.9.1V8.07L13.83 10l-1.93 1.93z"></path><title id="tg-c6b5c8cb-fc9a-e559-1eac-778bdb6766d7">Land area</title></svg></tg-house-land-area-small-svg><!----></tg-svg></tg-icon>


# In[77]:


# Create an empty list to store all the land_area
land_area_list = []

# Loop through all pages of search results
for page_number in range(1, 12):  
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    listings_attr = soup.find_all('ul',class_="tm-property-search-card-attribute-icons__features")
    
    # Create a for loop to append the information from the listings to the empty list
    for l in listings_attr:  # l.find('tg-icon', alt='Total parking'):        
        
        if l.find('tg-icon', alt="Land area"):            
            bath = l.find('tg-icon', alt="Land area").next_sibling.text
            land_area_list.append(bath)
            
        else:
            
            land_area_list.append('None')

# Print the list 
#print(land_area_list)
len(land_area_list)


# In[78]:


land_area_list


# In[79]:


# Try convert ha into m2 and then all into float
land_a = land_area_list[230:]


# In[80]:


# land_a


# In[81]:


laa = land_a[1].strip()


# In[82]:


laa


# In[83]:


lqq = float(laa.split()[0].replace(',',''))


# In[84]:


lqq


# In[85]:


# Convert land area into float number, then into square meters.
# Assigning zero where price is not specified ('None').
land_area_list1 = []
for i in land_area_list:
    i = i.strip()
    if i == 'None':
        land_area_list1.append(0)
    elif 'ha' in i:
        ha1 = float(i.split()[0])*10000
        land_area_list1.append(ha1)
    elif 'm2' in i:
        ha2 = float(i.split()[0].replace(',',''))
        land_area_list1.append(ha2)  
    
    


# In[86]:


len(land_area_list1)


# In[87]:


land_area_list1


# In[ ]:





# ### Title

# In[88]:


# <tm-property-search-card-listing-title tmid="standard-search-card-title" _nghost-frend-c737="" id="1681346607698-3425767661-standard-search-card-title">MyKiwiHouse Passive - Architectural Plans to build</tm-property-search-card-listing-title>


# In[89]:


# Create an empty list to store all the titles
title_list = []

# Loop through all pages of search results
for page_number in range(1, 12):  
    
    # Construct the URL for the current page
    url = url_template.format(page_number)

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the addresses using the appropriate tag and class selector
    titles = soup.find_all('tm-property-search-card-listing-title')

    # Extract the text content of each address and append it to the address_list
    for t in titles:
        title_list.append(t.text.strip())

# Print the list of addresses
# print(title_list)
len(title_list)


# In[90]:


title_list


# In[ ]:





# ###  Try / Checks

# In[91]:


price = soup.find_all('div', class_="tm-property-search-card-price-attribute__price")


# In[92]:


# price


# In[ ]:





# In[94]:


url2 = 'https://www.trademe.co.nz/a/property/residential/sale/otago/queenstown-lakes/search?property_type=apartment&property_type=house&sort_order=priceasc&bedrooms_min=1&bathrooms_min=1&page=2'


# In[95]:


response = requests.get(url2)

# Check if the response contains any listings
soup = BeautifulSoup(response.content, 'html.parser')
listings_address = soup.find_all('ul',class_="tm-property-search-card-attribute-icons__features")


# In[ ]:





# In[96]:


len(listings_address)


# In[97]:


for l in listings_address:
    if l.find('tg-icon', alt='Total parking'):
        print('hay attr')
    else:
        print('no hay attr')


# In[98]:


# <tg-icon _ngcontent-frend-c735="" alt="Bedrooms" name="bedroom" size="small" class="tm-property-search-card-attribute-icons__metric-icon o-icon o-icon--size-16" aria-hidden="false"><tg-svg class="o-svg o-svg--scale-to-fill"><tg-bedroom-small-svg class="ng-star-inserted"><svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" aria-labelledby="tg-e24a845d-ddb6-ec05-6e86-62b1295e24af" preserveAspectRatio="xMinYMid meet" focusable="false" role="img"><path d="M2.8 4h3.292A1.9 1.9 0 0 1 8 5.899V7h4.102A2.901 2.901 0 0 1 15 9.897V14a.9.9 0 1 1-1.8 0v-1H2.8v1A.9.9 0 1 1 1 14V3a.9.9 0 0 1 1.8 0v1zm0 1.8V7h3.4V5.899c0-.055-.044-.099-.108-.099H2.8zm0 5.4h10.4V9.897c0-.602-.494-1.097-1.098-1.097H2.8v2.4z"></path><title id="tg-e24a845d-ddb6-ec05-6e86-62b1295e24af">Bedrooms</title></svg></tg-bedroom-small-svg><!----></tg-svg></tg-icon>


# In[99]:


# <tg-icon _ngcontent-frend-c735="" alt="Total parking" name="vehicle-car-front" size="small" class="tm-property-search-card-attribute-icons__metric-icon o-icon o-icon--size-16" aria-hidden="false"><tg-svg class="o-svg o-svg--scale-to-fill"><tg-vehicle-car-front-small-svg class="ng-star-inserted"><svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-labelledby="tg-40089cca-9ffe-3899-c805-a5109c4b83da" preserveAspectRatio="xMinYMid meet" focusable="false" role="img"><path fill-rule="evenodd" clip-rule="evenodd" d="M13.68 6.67a.49.49 0 0 1 0 .17 2.78 2.78 0 0 1 .92 2.06v2a1.81 1.81 0 0 1-.87 1.49v2a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5V12.7h-6v1.64a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2A1.78 1.78 0 0 1 1 10.9v-2a2.78 2.78 0 0 1 .93-2.06.49.49 0 0 1 0-.17l.81-3.23A1.89 1.89 0 0 1 4.58 2H11a1.89 1.89 0 0 1 1.87 1.44l.81 3.23ZM3.093 8.193A1 1 0 0 0 2.8 8.9v2h10v-2a1 1 0 0 0-1-1h-8a1 1 0 0 0-.707.293ZM11 3.8H4.58a.1.1 0 0 0-.1.07L3.93 6.1h7.72l-.55-2.23a.1.1 0 0 0-.1-.07Zm-.2 4.852a.9.9 0 1 1 1 1.497.9.9 0 0 1-1-1.497Zm-7 0a.9.9 0 1 1 1 1.497.9.9 0 0 1-1-1.497Z"></path><title id="tg-40089cca-9ffe-3899-c805-a5109c4b83da">Total parking</title></svg></tg-vehicle-car-front-small-svg><!----></tg-svg></tg-icon>


# ### Dict {}

# In[ ]:


# longitude_ult2 # latitude_ult2


# In[ ]:





# In[172]:


house_features = {'Title':title_list, 'Full Address':address_list, 'Neighborhood':neighborhood1, 'District':district1, 'Latitude':latitude_ult2,'Longitude':longitude_ult2,'Street':street1,'Bedrooms':bedroom_list1, 'Bathrooms':bathroom_list1, 'Parking':parking_list1, 'Floor Area':floor_area_list1, 'Land Area':land_area_list1, 'Price':price_list1}


# In[173]:


for k,v in house_features.items():
    print(k,len(v))


# In[174]:


# house_features


# In[175]:


import pandas as pd


# In[176]:


df = pd.DataFrame(house_features)


# In[177]:


df.head(5)


# In[121]:


df.info()


# In[185]:


# df.to_csv('house_trademe3 18-04.csv',index_label='Index')


# In[189]:


df_house = pd.read_csv('house_trademe3 18-04.csv',index_col='Index')


# In[190]:


df_house.head()


# In[ ]:




