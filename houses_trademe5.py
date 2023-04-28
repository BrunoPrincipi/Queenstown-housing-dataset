#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import the libraries / packages needed

import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import folium
from IPython.display import display
import plotly.graph_objs as go
from plotly.tools import mpl_to_plotly
import plotly.express as px


# In[2]:


# Load the dataset built
df_house = pd.read_csv('house_trademe3 18-04.csv',index_col='Index')


# In[3]:


# Create a copy of the original dataframe
df = df_house.copy()


# ### Data summarization and visualization

# In[4]:


df.head()


# In[5]:


df.tail()


# In[6]:


# The dataset contains 237 instances, 12 features, 1 label ('Price')
df.info()


# In[7]:


# df['Price'] = df['Price'].apply(lambda x: float(x) if x.isnumeric() else x)


# In[8]:


df.describe()


# #### Bedrooms

# In[9]:


# Distribution of the number of Bedrooms. The graph shows that some instances have zero rooms, 
# 'zero' in this case represents a missing value. A decision must be made regarding this later.
sns.histplot(data=df, x='Bedrooms')


# In[ ]:





# #### Bathrooms

# In[ ]:





# In[10]:


# Distribution of the number of Bathrooms
sns.histplot(data=df, x='Bathrooms')


# In[ ]:





# #### Parking

# In[11]:


# Distribution of the number of Parking. As in the case of rooms, 'zero' represents a missing 
# value and an assumption must be made later.
sns.histplot(data=df, x='Parking')


# #### Floor Area

# In[12]:


# Distribution of the square meters of Floor Area. As in the case of rooms, 'zero' represents a 
# missing value and an assumption must be made later.
# In addition to the missing values(zero),the graph shows some extreme values in the right corner.
sns.histplot(data=df, x='Floor Area')


# In[ ]:





# #### Land Area

# In[13]:


# Distribution of the number square meters of Land Area. As in the case of rooms, 'zero' 
# represents a missing value and an assumption must be made later.
# In addition to the missing values(zero),the graph shows some extreme values in the right corner.
sns.histplot(data=df, x='Land Area')


# #### Neighborhood

# In[ ]:





# In[14]:


# Neighborhood
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(data=df, x='Neighborhood', ax=ax, order=df['Neighborhood'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=75, horizontalalignment='right')
plt.show()


# In[15]:


latitude_ult2 = df['Latitude']


# In[16]:


longitude_ult2 = df['Longitude']


# In[17]:


neighb_ult = df['Neighborhood']


# In[18]:


neighb_ult.value_counts()


# In[19]:


ind_ult = df.index


# In[20]:


# ind_ult


# In[21]:


# Localization of houses on a map
geolocator = Nominatim(user_agent="my22-app")

# Create a map object centered on a location
mapa = folium.Map(tiles='OpenStreetMap',location=[-45.0485, 168.7], zoom_start=9)

# Add multiple markers to the map object using a loop
for lat, lon, neighb, ind in zip(latitude_ult2, longitude_ult2, neighb_ult, ind_ult):
    popup_text = 'I:{}, {}'.format(ind, neighb)
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(mapa)
    
# Display the map object
display(mapa)


# In[ ]:





# ### Price

# In[22]:


# On the data extracted were roughly half of the instances where the price was not especified 
# on the publication, those missing values were filled with 'none'
# To explore the 'Price', a dataframe is created without the missing values.


# In[23]:


# none values on the 'Price' feature
df['Price'].value_counts()


# In[24]:


# created a dataframe only where 'Price' is 'none'
df_no_precie = df[df['Price']== 'none']


# In[25]:


df_no_precie.info()


# In[ ]:





# In[26]:


# Create a dataframe only where the 'Price' is not 'none' to be able to graff and visualize 
# the information
df1 = df.drop(df_no_precie.index,axis=0)


# In[27]:


df1.info()


# In[28]:


# Convert the string number into float number
df1['Price'] = df1['Price'].astype(float)


# In[29]:


# Call describe method to explore the 'Price' feature
# the mean, std, min and max values show that prices are spread over a wide range that may be is 
# affected by outliers.
df1['Price'].describe()


# In[30]:


# df1.info()


# ##### Create boxplot to detect outliers

# In[31]:


plt.figure(figsize=(12,4))
sns.boxplot(data=df1, x=df1['Price'])


# In[32]:


# sns.scatterplot(data=df1, x='Floor Area', y='Price')


# ##### Detect outliers plotting the relation between 'Floor Area' and 'Price'

# In[33]:


# In the graph you can see an outlier in the upper right corner (Price == 35M). 
# Zooming in, at least two outliers can be seen in the lower left corner (Price == 14K, and 125K).
fig = px.scatter(df1, x='Floor Area', y='Price')


# In[34]:


fig.show()


# In[35]:


# Outliers detected on the graff
price_outliers = df1[(df1['Price']<200000) | (df1['Price']> 10000000)]


# In[36]:


price_outliers


# In[ ]:





# ### Dataset manipulation - Missing or wrong values

# #### Bedrooms: The assumption will be that a house must have at least 1 room. On instances with 0 rooms the value is replaced by 1

# In[37]:


df[df['Bedrooms'] == 0]


# In[38]:


df.loc[6,'Bedrooms'] = 1


# In[39]:


df.iloc[6]['Bedrooms']


# #### Parking and Land Area: The assumption will be that a house may not have parking or land area, so no changes on these features.

# In[ ]:





# #### Correcting 'Neighborhood' 
# ##### To correct the name of the neighborhood where a house is located, first a polygon of the neighborhood's coordinates is created using google earth and the library shapely.geometry , then it is checked if the location of the house match with the neighborhood's name assigned to it, and finally it is corrected if appropriate.

# In[40]:


# Library to define a polygon
from shapely.geometry import Polygon, Point


# In[ ]:





# In[41]:


# Method to extract the coordinates from the polygon created on google earth and convert it 
# into float number
def google_earth_coord(c):
    list1=[]
    
    coor = c.split(',0')
    
    for i in coor:
        long,lati = i.split(',')
        long = float(long)
        lati = float(lati)
        list1.append((long,lati))
    
    return list1


# #### The followings are the neighborhood's coordinates extracted from the polygon created on google earth

# In[42]:


town_coord = '168.6725867824327,-45.03372096976784,0 168.6626996287028,-45.02822460456138,0 168.6556323528401,-45.02835630029668,0 168.6519930216147,-45.03209619994454,0 168.6439591361041,-45.03530885302249,0 168.6482698547174,-45.03785194925482,0 168.6561607856517,-45.03799058363835,0 168.6679204925338,-45.03794733417917,0 168.6726300338443,-45.03732369104621,0 168.6741834085676,-45.03597030978613,0 168.6725867824327,-45.03372096976784'


# In[43]:


Town_Centre_poly = google_earth_coord(town_coord)


# In[44]:


# Town_Centre_poly


# In[45]:


Jacks_Point_coord = '168.7599802152084,-45.05950790476543,0 168.7393644790042,-45.05899141378895,0 168.7341301642343,-45.06805929107995,0 168.7477221342359,-45.10510798163424,0 168.7602907158777,-45.10375169373078,0 168.7635362513163,-45.07589233962541,0 168.7599802152084,-45.05950790476543'


# In[46]:


Jacks_Point_poly = google_earth_coord(Jacks_Point_coord)


# In[47]:


# Jacks_Point_poly


# In[48]:


Queenstown_Hill_coord ='168.6908265545311,-45.02871228454156,0 168.6876843728018,-45.02469311354208,0 168.6780762254942,-45.02914632690639,0 168.6676436288347,-45.02701734053662,0 168.6628068680996,-45.02812402670143,0 168.6727877405359,-45.03373363725486,0 168.6744965702981,-45.03612198931659,0 168.6866829237795,-45.0324349953688,0 168.6908265545311,-45.02871228454156'


# In[49]:


Queenstown_Hill_poly = google_earth_coord(Queenstown_Hill_coord)


# In[50]:


# Queenstown_Hill_poly


# In[51]:


Frankton_coord = '168.7386706273225,-45.00702623698549,0 168.7127356349137,-45.01463255282195,0 168.7146626817154,-45.02111226075554,0 168.7210566430261,-45.01804081793711,0 168.726378894013,-45.01934456879649,0 168.731647834949,-45.02794818243997,0 168.7461772367208,-45.03302854027898,0 168.761434913585,-45.01771372785403,0 168.7532904362893,-45.00398420520271,0 168.7386706273225,-45.00702623698549'


# In[52]:


Frankton_poly = google_earth_coord(Frankton_coord)


# In[53]:


# Frankton_poly


# In[54]:


Glenorchy_coord = '168.3801476807326,-44.86013794098796,0 168.3989656099432,-44.85851674759282,0 168.3968064544714,-44.84485683218708,0 168.3767060857413,-44.84552827891852,0 168.3801476807326,-44.86013794098796'


# In[55]:


Glenorchy_poly  = google_earth_coord(Glenorchy_coord)


# In[56]:


# Glenorchy_poly


# In[57]:


Queenstown_East_coord = '168.6540878447852,-45.02825666629791,0 168.6613183194912,-45.02817125087957,0 168.6632723894049,-45.02761480597685,0 168.6680449490386,-45.01515405051126,0 168.6611336781258,-45.01456111277075,0 168.6540878447852,-45.02825666629791'


# In[58]:


Queenstown_East_poly  = google_earth_coord(Queenstown_East_coord)


# In[59]:


# Queenstown_East_poly


# In[60]:


Sunshine_Bay_coord = '168.6260072904601,-45.03846397693103,0 168.6183971253916,-45.04260284067364,0 168.6252203302284,-45.049620925855,0 168.6331643682245,-45.04719408794052,0 168.6260072904601,-45.03846397693103'


# In[61]:


Sunshine_Bay_poly = google_earth_coord(Sunshine_Bay_coord)


# In[62]:


# Sunshine_Bay_poly


# In[63]:


Fernhill_coord = '168.6454727872839,-45.04164887913058,0 168.6361533302998,-45.03322504692615,0 168.625842094068,-45.03800724045495,0 168.6332485128085,-45.04710499947659,0 168.6454727872839,-45.04164887913058'


# In[64]:


Fernhill_poly = google_earth_coord(Fernhill_coord)


# In[65]:


# Fernhill_poly


# In[66]:


Arthurs_Point_coord = '168.676139914216,-44.97398055493404,0 168.6601315443668,-44.97892910447437,0 168.655756138606,-44.98808090628666,0 168.6713702465528,-44.99804987734834,0 168.6997637445905,-44.98171948789749,0 168.6929357474312,-44.97298088357005,0 168.676139914216,-44.97398055493404'


# In[67]:


Arthurs_Point_poly = google_earth_coord(Arthurs_Point_coord)


# In[68]:


# Arthurs_Point_poly


# In[69]:


Kingston_coord = '168.7213653982367,-45.34066662914152,0 168.7297560181767,-45.33590473496009,0 168.7139877247116,-45.32838478904507,0 168.7077033351913,-45.33089159026112,0 168.7213653982367,-45.34066662914152'


# In[70]:


Kingston_poly = google_earth_coord(Kingston_coord)


# In[71]:


# Kingston_poly


# In[72]:


Arrowtown_coord = '168.7938309854124,-44.94067055853476,0 168.7993825517569,-44.95519259834575,0 168.8468577368233,-44.966153938335,0 168.8611492648138,-44.95693313366395,0 168.8494179878396,-44.94054685871859,0 168.8305693433252,-44.93372041917318,0 168.8113643655659,-44.93563924348211,0 168.7938309854124,-44.94067055853476'


# In[73]:


Arrowtown_poly = google_earth_coord(Arrowtown_coord)


# In[74]:


Lake_Hayes_coord = '168.7749569761861,-45.00053291047041,0 168.8005601597228,-45.00997913385833,0 168.8392960462897,-44.9677678384145,0 168.8003590501768,-44.95797505383442,0 168.7857363068186,-44.99323556249108,0 168.7811545877688,-44.99660794937951,0 168.7749569761861,-45.00053291047041'


# In[75]:


Lake_Hayes_poly = google_earth_coord(Lake_Hayes_coord)


# In[76]:


Lower_Shotover_coord = '168.7756967783642,-45.01297235797291,0 168.7867990220982,-45.00541570546994,0 168.7772078955417,-45.00190051655169,0 168.7616559252174,-44.99825831963317,0 168.7597696675481,-44.99250893484599,0 168.7514921379124,-44.99164831923346,0 168.7495377998695,-44.99786734640436,0 168.7488567936864,-45.00091262502569,0 168.7482624668527,-45.00299566671596,0 168.7507263206919,-45.0043508816693,0 168.7532421706012,-45.00385740015888,0 168.7587779707847,-45.00809218246322,0 168.7756967783642,-45.01297235797291'


# In[77]:


Lower_Shotover_poly = google_earth_coord(Lower_Shotover_coord)


# In[78]:


Goldfield_Heights_coord = '168.714405681087,-45.02118416290669,0 168.7124819568652,-45.01469451143704,0 168.7035232659286,-45.01733018322442,0 168.6915169785011,-45.02095934415598,0 168.6876283537451,-45.02432983690997,0 168.6917082803959,-45.02936829073051,0 168.714405681087,-45.02118416290669'


# In[79]:


Goldfield_Heights_poly = google_earth_coord(Goldfield_Heights_coord)


# In[80]:


Kelvin_Peninsula_coord = '168.7325990540126,-45.03200628050661,0 168.7334311691741,-45.02911452801772,0 168.7284539186631,-45.02673754418298,0 168.710106479703,-45.02885188582782,0 168.6920502367969,-45.03880035948804,0 168.6776783673184,-45.04565247049001,0 168.6838362559861,-45.05240286266285,0 168.7325990540126,-45.03200628050661'


# In[81]:


Kelvin_Peninsula_poly = google_earth_coord(Kelvin_Peninsula_coord)


# In[82]:


Gibbston_coord = '168.8983055380359,-45.00580811933798,0 168.8982889926479,-45.01763711931486,0 168.9447063482972,-45.02432120276823,0 168.9891214597097,-45.04183733771549,0 168.9981629803669,-45.02927362592601,0 168.9766142621052,-45.01769273760629,0 168.9367339178198,-45.00958950361641,0 168.8983055380359,-45.00580811933798'


# In[83]:


Gibbston_poly = google_earth_coord(Gibbston_coord)


# In[84]:


Dalefield_coord = '168.7433152514104,-44.97499465976144,0 168.768500318211,-44.98971149524424,0 168.7902670169402,-44.97775163995819,0 168.7913927053565,-44.96438624511203,0 168.7854733591573,-44.93995028713742,0 168.7414510454576,-44.94834377587763,0 168.7433152514104,-44.97499465976144'


# In[85]:


Dalefield_poly = google_earth_coord(Dalefield_coord)


# In[86]:


Closeburn_coord = '168.6036765517873,-45.06029843477088,0 168.5990718776632,-45.03870542591241,0 168.4985815378419,-45.0627452165294,0 168.5035333715983,-45.08283864396196,0 168.6036765517873,-45.06029843477088'


# In[87]:


Closeburn_poly = google_earth_coord(Closeburn_coord)


# In[88]:


Arrow_Junction_coord = '168.8407480677023,-45.00603831325883,0 168.8892207340643,-45.01133424639544,0 168.8584016400034,-44.96788679167609,0 168.8462251348863,-44.96824582346253,0 168.8404280371873,-44.98228249966387,0 168.8407480677023,-45.00603831325883'


# In[89]:


Arrow_Junction_poly = google_earth_coord(Arrow_Junction_coord)


# In[ ]:





# In[ ]:





# In[90]:


# Method to check if the neighborhood's polygon match with the neighborhood's name, 
# if not it return a list with the index where the name is wrong.
def check_neighborhood(poly,neighborhood):
    to_change = []
    
    for lon, lat, nei, ind in zip(longitude_ult2, latitude_ult2, neighb_ult, ind_ult):

        # Define a datapoint
        i_point = (lon, lat)

        # Create a point object that represents the datapoint
        datapoint = Point(i_point)

        # Create a polygon object that represents the neighborhood
        neighborhood_poly_ob = Polygon(poly)

        # Check if the datapoint is located within the neighborhood polygon
        if neighborhood_poly_ob.contains(datapoint) and nei != neighborhood:
            
            to_change.append(ind)
#             print(f"The datapoint at index {ind} is wrong")
        else:
            pass
#             print("The datapoint is ok")
    return to_change


# ##### The following are the varibles created to setore the list with the index where the neighborhood's name is wrong and the code to correct it.

# In[91]:


to_town = check_neighborhood(Town_Centre_poly,neighborhood='Town Centre')


# In[92]:


to_town


# In[93]:


df.loc[to_town,'Neighborhood']


# In[94]:


df.loc[to_town,'Neighborhood'] ='Town Centre'


# In[95]:


df.loc[to_town,'Neighborhood']


# In[96]:


to_jacks = check_neighborhood(Jacks_Point_poly,neighborhood='Jacks Point')


# In[97]:


df.loc[to_jacks,'Neighborhood']


# In[98]:


df.loc[to_jacks,'Neighborhood'] = 'Jacks Point'


# In[99]:


# df.loc[to_jacks,'Neighborhood']


# In[ ]:





# In[100]:


to_hill = check_neighborhood(Queenstown_Hill_poly,neighborhood='Queenstown Hill') 


# In[101]:


df.loc[to_hill,'Neighborhood']


# In[102]:


df.loc[to_hill,'Neighborhood'] = 'Queenstown Hill'


# In[103]:


df.loc[to_hill,'Neighborhood']


# In[104]:


to_frankton = check_neighborhood(Frankton_poly,neighborhood='Frankton')


# In[105]:


df.loc[to_frankton,'Neighborhood']


# In[106]:


df.loc[to_frankton,'Neighborhood'] = 'Frankton'


# In[107]:


df.loc[to_frankton,'Neighborhood']


# In[ ]:





# In[108]:


# The output is an empty list, so no wrong neighborhood
check_neighborhood(Glenorchy_poly,neighborhood='Glenorchy')


# In[109]:


to_east = check_neighborhood(Queenstown_East_poly,neighborhood='Queenstown East')


# In[110]:


df.loc[to_east,'Neighborhood']


# In[111]:


df.loc[to_east,'Neighborhood'] = 'Queenstown East'


# In[112]:


df.loc[to_east,'Neighborhood']


# In[ ]:





# In[113]:


# The output is an empty list, so no wrong neighborhood
check_neighborhood(Sunshine_Bay_poly,neighborhood='Sunshine Bay')


# In[114]:


to_fernhill = check_neighborhood(Fernhill_poly,neighborhood='Fernhill')


# In[115]:


df.loc[to_fernhill,'Neighborhood']


# In[116]:


df.loc[to_fernhill,'Neighborhood'] = 'Fernhill'


# In[117]:


df.loc[to_fernhill,'Neighborhood']


# In[ ]:





# In[118]:


to_arthurs = check_neighborhood(Arthurs_Point_poly,neighborhood='Arthurs Point')


# In[119]:


df.loc[to_arthurs,'Neighborhood']


# In[120]:


df.loc[to_arthurs,'Neighborhood'] = 'Arthurs Point'


# In[121]:


# The output is an empty list, so no wrong neighborhood
check_neighborhood(Kingston_poly,neighborhood='Kingston')


# In[122]:


# The output is an empty list, so no wrong neighborhood
check_neighborhood(Arrowtown_poly,neighborhood='Arrowtown')


# In[ ]:





# In[ ]:





# In[123]:


to_hayes = check_neighborhood(Lake_Hayes_poly,neighborhood='Lake Hayes')


# In[124]:


df.loc[to_hayes,'Neighborhood']


# In[125]:


df.loc[to_hayes,'Neighborhood'] = 'Lake Hayes'


# In[ ]:





# In[126]:


# The output is an empty list, so no wrong neighborhood
check_neighborhood(Lower_Shotover_poly,neighborhood='Lower Shotover')


# In[ ]:





# In[127]:


to_goldfield = check_neighborhood(Goldfield_Heights_poly,neighborhood='Goldfield Heights')


# In[128]:


df.loc[to_goldfield,'Neighborhood']


# In[129]:


df.loc[to_goldfield,'Neighborhood'] = 'Goldfield Heights'


# In[130]:


df.loc[to_goldfield,'Neighborhood']


# In[131]:


to_kelvin = check_neighborhood(Kelvin_Peninsula_poly,neighborhood='Kelvin Peninsula')


# In[132]:


df.loc[to_kelvin,'Neighborhood']


# In[133]:


df.loc[to_kelvin,'Neighborhood'] = 'Kelvin Peninsula'


# In[134]:


to_gibbston = check_neighborhood(Gibbston_poly,neighborhood='Gibbston')


# In[135]:


df.loc[to_gibbston,'Neighborhood']


# In[136]:


df.loc[to_gibbston,'Neighborhood'] = 'Gibbston'


# In[137]:


# The output is an empty list, so no wrong neighborhood
check_neighborhood(Dalefield_poly,neighborhood='Dalefield')


# In[138]:


to_closeburn = check_neighborhood(Closeburn_poly,neighborhood='Closeburn')


# In[139]:


df.loc[to_closeburn,'Neighborhood']


# In[140]:


df.loc[to_closeburn,'Neighborhood'] = 'Closeburn'


# In[141]:


# The output is an empty list, so no wrong neighborhood
check_neighborhood(Arrow_Junction_poly,neighborhood='Arrow Junction')


# In[142]:


df['Neighborhood'].unique()


# In[143]:


# Check the distribution once the neighborhood were corrected
df['Neighborhood'].value_counts()


# In[ ]:





# In[144]:


neighb_ult3 = df['Neighborhood']


# In[145]:


neighb_ult3.value_counts()


# In[146]:


# Neighborhood
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(data=df, x='Neighborhood', ax=ax, order=df['Neighborhood'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=75, horizontalalignment='right')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[147]:


# Localization of houses on a map
geolocator2 = Nominatim(user_agent="my3-app")

# Create a map object centered on a location
mapa2 = folium.Map(tiles='OpenStreetMap',location=[-45.0485, 168.7], zoom_start=9)

# Add multiple markers to the map object using a loop
for lat, lon, neighb, ind in zip(latitude_ult2, longitude_ult2, neighb_ult3, ind_ult):
    popup_text = 'I:{}, {}'.format(ind, neighb)
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(mapa2)
    
# Display the map object
display(mapa2)


# In[ ]:





# #### Outliers on 'Price': 
# ##### Exploring the detected outliers in the visualization and summary section, more information about those instances was found as shown below:

# In[148]:


price_outliers.index


# In[149]:


# The intance at index 0 it is refering to an architectural plans, that explains the low price.
# This instance should be deleted.
df.loc[0]


# In[150]:


# df.loc[0] drop


# In[151]:


# The instance at index 1 it is referring to a share sale. The price reflects a quarter of the 
# true value, therefore to avoid delete the instance, the price will be multiplied by 4
df.loc[1]


# In[152]:


df.loc[1,'Price'] = 125000*4


# In[153]:


df.loc[1,'Price']


# In[154]:


# The instance at index 236 refers to a house that has characteristics of a boutique hotel, 
# not a regular house. The instance should be deleted.
df.loc[236]


# In[155]:


# Delete outliers
df.drop([0,236],axis=0,inplace=True)


# In[156]:


df.info()


# In[157]:


# Convert 'Price' into float number
df['Price'] = df['Price'].replace('none',0)


# In[158]:


df['Price'] = df['Price'].astype(float)


# In[159]:


df.info()


# In[160]:


df['Price']


# In[161]:


fig2 = px.scatter(df, x='Floor Area', y='Price')


# In[162]:


# The graph below shows the relation between 'Floor Area' and 'Price' without the outliers.
# Also the chart shows the instances where the 'Price' was not available on the web page.
# Instances where 'Price' == 0 will be use at the end to predict the price using the parameters 
# lerned by the model.
# The chart also shows the instances where 'Flor Area' == 0, 
# these are the missing values that will be treated on the next section.
fig2.show()


# #### Floor Area: imputing missing value.
# ##### Since the square meters of a house cannot be zero, it is necessary to infer the value of 'Floor Area'. To do it the Iterative Imputer will be implemented

# In[163]:


sum(df['Floor Area'] == 0)


# In[164]:


# Where are the houses with missing value located
df[df['Floor Area'] == 0]['Neighborhood'].value_counts()


# In[165]:


floor_area2 = df[df['Floor Area'] == 0].index


# In[166]:


# df.loc[floor_area2,'Floor Area']


# In[167]:


# Replace the lavues 0 fot 'NaN' to alow the IterativeImputer to detect the missing values
df['Floor Area'] = df['Floor Area'].replace(0,np.nan)


# In[168]:


df.loc[floor_area2,'Floor Area']


# In[169]:


df.info()


# In[170]:


# IterativeImputer is a sklearn predictor that perform a regression model to predict 
# missing values on numerical features


# In[171]:


# Import the packages needed
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


# In[172]:


# Method to implement IterativeImputer
def implement_iterativeimputer(df,label=None):
    
    # Create an instance of IterativeImputer
    iterative_imputer = IterativeImputer(max_iter=10000)
    
    # the code below stores in a variable the numerical features of the dataframe
    df_num = df.select_dtypes(exclude='object')
    
    # the code below drop the label to not use it as an imput to predict the feature
    df_num = df_num.drop(label,axis=1)
    
    # the code below stores in a variable the predicted missing values on numerical features
    X_num = iterative_imputer.fit_transform(df_num)
    
    # the code below creates a dataframe with the numerical features without missing values
    df_nume_final = pd.DataFrame(X_num,columns=df_num.columns,index=df_num.index)
    
    # the code below stores in a variable the categorical features of the dataframe
    df_obj = df.select_dtypes(include='object')
    df_3 = pd.concat([df_nume_final,df_obj],axis=1)
    return df_3


# In[173]:


df_2 = implement_iterativeimputer(df,label='Price')


# In[174]:


df_2.info()


# In[175]:


# Plot the new distribution of square meters on 'Floor Area' with the predicted missing values
sns.histplot(data=df_2, x='Floor Area')


# In[ ]:





# #### Prepering the dataset to build models

# In[176]:


# Add the feature 'Price' to the new dataframe whitout missing values on 'Flor Area'
df_2['Price'] = df['Price']


# In[177]:


df_2.info()


# In[178]:


# Create a dataframe with the instances where are the missing values for 'Price'
# This dataframe will be used later to predic those missing values on 'Price'
df_missing_price = df_2[df_2['Price'] == 0]


# In[179]:


df_missing_price.head(3)


# In[ ]:





# In[180]:


# Drop the instances with missing values on 'Price'
df_2.drop(df_missing_price.index,axis=0, inplace=True)


# In[181]:


# Check
sum(df_2['Price'] == 0)


# In[ ]:





# In[182]:


# Plot the relation between 'Floor Area' and 'Price' without tne missing values on 'Price'
fig3 = px.scatter(df_2, x='Floor Area', y='Price')
fig3.show()


# In[183]:


# Explore correlation between features
df_2.corr()


# In[184]:


corr_price = df_2.corr()['Price'].drop('Price').sort_values()


# In[185]:


corr_price


# In[ ]:





# In[186]:


# sns.color_palette()


# In[187]:


# Plot the correlations between the features and the label 'Price'
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x=corr_price.index, y=corr_price.values,palette='viridis')
ax.set_xticklabels(ax.get_xticklabels(), rotation=75, horizontalalignment='right')
plt.show()


# In[ ]:





# #### Categorical feature - OneHotEncoding

# In[188]:


# First it is necessary to drop features not useful


# In[189]:


df_2.head(2)


# In[190]:


df_2.columns


# In[191]:


# Assumption: Dropping features that doesn't add useful information to predict 'Price'
df_2.drop(['Title','Full Address','District','Street'],axis=1,inplace=True)


# In[192]:


df_2.info()


# In[193]:


len(df_2['Neighborhood'].unique())


# In[ ]:





# In[194]:


# OneHotEncoder is a sklearn transformer that perform one hot encoding on categorical features
# The code import the packages needed
from sklearn.preprocessing import OneHotEncoder


# In[195]:


# @


# In[196]:



# Create an instance of OneHotEncoder
onehot_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore' )

# Store in a variable the numerical features of the dataframe
df_num = df_2.select_dtypes(exclude='object')

# Store in a variable the categorical features of the dataframe
df_obj = df_2.select_dtypes(include='object')

# Store in a variable the output of one hot encoding on categorical features
df_categorical = pd.DataFrame(onehot_encoder.fit_transform(df_obj),
                                columns=onehot_encoder.get_feature_names(),
                                index=df_obj.index)    
# Concatenate the numeric and object dataframes
df_fi = pd.concat([df_num,df_categorical],axis=1)
# return df_onehot


# In[197]:


df_fi.info()


# #### Building the models

# In[198]:


# import the libraries / packages needed

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error,mean_absolute_error,median_absolute_error
from sklearn.ensemble import RandomForestRegressor


# In[199]:


# The code below store the features on the variable X 
X = df_fi.drop('Price',axis=1)


# In[200]:


X.head()


# In[201]:


# The code below store the label 'Price' on the variable y 
y = df_fi['Price']


# In[202]:


y


# In[203]:


# Split the data into train and test 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


# In[204]:


# Check the shape of the splits to fit the models
print('X_train', X_train.shape)
print('X_test', X_test.shape)
print('y_train', y_train.shape)
print('y_test', y_test.shape)


# In[ ]:





# #### StandardScaler

# In[205]:


# Create an instance of StandardScaler
stdr = StandardScaler()


# In[206]:


# Scale the features
X_train_scaled = stdr.fit_transform(X_train)
X_test_scaled = stdr.transform(X_test)


# In[207]:


# X_train_scaled


# In[208]:


# X_test_scaled


# #### Linear Regression
# ##### Without scaling the features

# In[ ]:





# In[209]:


# Creates an instance of the model
linear_regression = LinearRegression()


# In[210]:


# Fit the model
linear_regression.fit(X_train,y_train)


# In[211]:


# Creates predictions 
pred_linear_regression = linear_regression.predict(X_test)


# In[212]:


# Root Mean Squared Error (RMSE) between the truth and the predictions
RMSE_linear_r = np.sqrt(mean_squared_error(y_test,pred_linear_regression))


# In[213]:


RMSE_linear_r


# In[214]:


df_fi['Price'].mean()


# In[215]:


# Compare the error against the average house price
np.sqrt(mean_squared_error(y_test,pred_linear_regression))/df_fi['Price'].mean()


# In[ ]:





# #### Linear Regression
# ##### Scaling the features

# In[216]:


# Creates an instance of the model
linear_regression_2 = LinearRegression()


# In[217]:


# Fit the model
linear_regression_2.fit(X_train_scaled,y_train)


# In[218]:


# Creates predictions 
pred_linear_regression_2 = linear_regression_2.predict(X_test_scaled)


# In[219]:


# Root Mean Squared Error (RMSE) between the truth and the predictions
RMSE_linear_r2 = np.sqrt(mean_squared_error(y_test,pred_linear_regression_2))


# In[220]:


# Same result scaling or not the features.
RMSE_linear_r2


# #### ElasticNet

# In[221]:


# Creates an instance of the model
elastic_net = ElasticNet(max_iter=100000,random_state=42)


# In[222]:


# Creates a grid to combine parameters
param_grid = {'alpha':[.2,.3,.5,1],'l1_ratio':[.65,.85,.93,.99]}


# In[223]:


# Perform a grid search for hyperparameter tuning
grid_elastic_net = GridSearchCV(elastic_net, param_grid=param_grid,
                                scoring='neg_mean_squared_error',cv=10,verbose=1)


# In[224]:


# Fit the model
grid_elastic_net.fit(X_train_scaled,y_train)


# In[225]:


grid_elastic_net.best_params_


# In[226]:


# Creates predictions
pred_grid = grid_elastic_net.predict(X_test_scaled)


# In[227]:


# Root Mean Squared Error (RMSE) between the truth and the predictions
RMSE_elasticNet = np.sqrt(mean_squared_error(y_test,pred_grid))


# In[228]:


RMSE_elasticNet


# In[229]:


# Compare the error against the average house price
np.sqrt(mean_squared_error(y_test,pred_grid))/df_fi['Price'].mean()


# In[230]:


# @


# #### Random Forest Regressor

# In[231]:


# Creates an instance of the model
rf_model = RandomForestRegressor(random_state=101)


# In[232]:


# Creates a grid to combine parameters
param_grid_rf = {'n_estimators':[100,150,200], # number of trees inside the classifier         
               'max_samples':[0.85,0.9,0.99], # max samples
               'max_depth': [6,10,15], # the depth of the tree
              'max_features':[3,5,10,15,24]} # max features tu use


# In[233]:


# Perform a grid search for hyperparameter tuning
grid_rf = GridSearchCV(rf_model,param_grid_rf,cv=10)


# In[234]:


# Fit the model
grid_rf.fit(X_train_scaled, y_train)


# In[235]:


grid_rf.best_params_


# In[236]:


# Creates predictions
rf_prediction = grid_rf.predict(X_test_scaled)


# In[237]:


# Root Mean Squared Error (RMSE) between the truth and the predictions
RMSE_rf = np.sqrt(mean_squared_error(y_test,rf_prediction))


# In[238]:


RMSE_rf


# In[239]:


# Compare the error against the average house price
np.sqrt(mean_squared_error(y_test,rf_prediction))/df_fi['Price'].mean()


# In[240]:


# 0.21 - 0.20


# In[241]:


mean_absolute_error(y_test,rf_prediction)


# In[242]:


median_absolute_error(y_test,rf_prediction)


# In[243]:


# MAE (Mean Absolute Error) and MedAE (Median Absolute Error) 


# #### Predict the missing values on 'Price'

# In[244]:


df_missing_price.head(3)


# ##### Perform the same data cleaning process done on the train data set

# In[245]:


# Drop usless features
df_mp = df_missing_price.drop(['Title','Full Address','District','Street'],axis=1)


# In[246]:


# df_mp.head()


# In[247]:


# Store in a variable the numerical features of the dataframe
df_num2 = df_mp.select_dtypes(exclude='object')


# In[248]:


# Store in a variable the categorical features of the dataframe
df_obj2 = df_mp.select_dtypes(include='object')


# In[249]:


# Store in a variable the output of one hot encoding on categorical features
df_categorical2 = pd.DataFrame(onehot_encoder.transform(df_obj2),
                                    columns=onehot_encoder.get_feature_names(),
                                    index=df_obj2.index)  


# In[250]:


# Concatenate the numeric and object dataframes
df_mp_2 = pd.concat([df_num2,df_categorical2],axis=1)


# In[251]:


# df_mp_2.info()


# In[252]:


df_mp_2.drop('Price',axis=1,inplace=True)


# In[253]:


df_mp_2.shape


# In[254]:


X_missing_price = stdr.transform(df_mp_2)


# In[255]:


# Prediction
rf_predict_missing_price = grid_rf.predict(X_missing_price)


# In[256]:


rf_predict_missing_price.shape


# In[ ]:





# In[257]:


# Change on the dataframe the missing values on 'Price' for the predicted values
df_mp['Price'] = rf_predict_missing_price


# In[258]:


df_mp.head(5)


# In[259]:


# Plotting the relation between 'Floor Area' and 'Price' only the predicted missing values on 'Price'
fig4 = px.scatter(df_mp, x='Floor Area', y='Price')
fig4.show()


# ### Plotting on a map

# ##### Plotting on a map the houses with actual prices and with predicted prices.The blue ones are the one with atual prices. The pink ones are the houses with missing values on 'Price', which later were predicted based on the parameters learned by the model.

# #### Create the viariables to build the map

# In[260]:


# Actual 'Price'
df_2.shape


# In[261]:


lati_1 = df_2['Latitude']


# In[262]:


longi_1 = df_2['Longitude']


# In[263]:


neig_1 = df_2['Neighborhood']


# In[264]:


ind_1 = df_2.index


# In[265]:


price_1 = df_2['Price']


# In[ ]:





# In[266]:


# Predicted 'Price'
df_mp.shape


# In[267]:


lati_2 = df_mp['Latitude']


# In[268]:


longi_2 = df_mp['Longitude']


# In[269]:


neig_2 = df_mp['Neighborhood']


# In[270]:


ind_2 = df_mp.index


# In[271]:


price_2 = df_mp['Price']


# In[272]:


# Method to format the price
def nzd_format(x):
    return "${:,.2f} NZD".format(x)


# In[273]:


price_2f = price_2.apply(nzd_format)


# In[274]:


price_1f = price_1.apply(nzd_format)


# In[275]:


# Localization of houses on a map
geolocator = Nominatim(user_agent="my23-app")

# # Create a map object centered on a location
mapa = folium.Map(tiles='OpenStreetMap',location=[-45.0485, 168.7], zoom_start=9)

# Add markers from group 1 to the map object using a loop
for lat, lon, neighb, ind, price in zip(lati_1, longi_1, neig_1, ind_1,price_1f):
    popup_text = 'I:{}, {}, {}'.format(ind,neighb, price )
    folium.Marker(location=[lat, lon], popup=popup_text,icon=folium.Icon(color='darkblue')).add_to(mapa)

# Add markers from group 2 to the map object using a loop
for lat, lon, neighb, ind, price in zip(lati_2, longi_2, neig_2, ind_2,price_2f):
    popup_text = 'I:{}, {}, {}'.format(ind,neighb, price )
    folium.Marker(location=[lat, lon], popup=popup_text,icon=folium.Icon(color='pink')).add_to(mapa)    

# Display the map object
display(mapa)


# In[ ]:




