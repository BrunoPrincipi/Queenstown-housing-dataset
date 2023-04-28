# Predicting House Prices in the Queenstown-Lake Region


![image](https://user-images.githubusercontent.com/125404145/235096490-a92d4201-9f76-4b9f-b01f-0d754f26090d.png)



![image](https://user-images.githubusercontent.com/125404145/235096085-84f18ae8-ebc0-41a0-b60b-f7e75ef65382.png)





## Project Overview
This project aims to analyze data related to houses on sale in the Queenstown-Lake region and predict their prices based on a set of features extracted from the Trade Me website. The project has an educational purpose and serves as a practice and introduction to machine learning fundamentals. 

The dataset used in this project was collected by extracting information from the Trade Me website using Python libraries such as Beautifulsoup, requests, and regular expressions. The data contains information about houses on sale in the Queenstown-Lake region (New Zealand), including their features such as location, size, number of rooms, etc.

In addition, the project uses `shapely.geometry` to check if a house has the correct neighborhood name based on its coordinates, ensuring the accuracy of the data and improving the performance of the machine learning model.

To visualize the data, `geopy` and `folium` libraries are used to plot the houses on a map of the region. This helps to better understand the data and identify any patterns or trends.

The project uses a supervised learning approach to build a machine learning model that predicts the price of a house based on the given features. The models are trained on a portion of the dataset and tested on the remaining data to evaluate its performance.

## Technologies used:
- Python
- Beautifulsoup
- Requests
- Regular expressions
- Shapely
- Geopy
- Folium
- Scikit-learn
- Pandas
- NumPy


## Goals and Results:

Goals:
- Learn and experiment extracting information from a website to build a datast from scratch.
- Learn and experiment how different data cleaning/preprocessing tasks affect model predictions.
- Learn and experiment how the different hyperparameters affect model predictions.
- Predict the sale price of the houses based on the given features.

Results:
To evaluate the performance of the models, Root Mean Squared Error (RMSE) was chosen as the metric. The best performance was achieved by the Random Forest Regressor model, with an RMSE value of 310569. When compared to the mean price of the dataset (NZD $1.494.764), the RMSE represents an average error of approximately 20% of the mean. This is not ideal, but still suggests that the model has some predictive power, it's worth noting that the dataset used in this project is small, with only 237 instances (all houses available to extract from the website, on 04/18/2023, in the specified region), and more than half of these instances do not specify the price value (label) for the house. Given these limitations, there is still room for improvement in the model's performance. Future work could involve collecting more data, feature engineering, or other techniques to address these limitations.

## Files inside this repo
This Project includes:
  - 1 csv file contains the dataset(house_trademe3 18-04.csv).
  - 1 executable file, where the cleaning and pre-processing of the data was performed. Also where the models     were built (houses_trademe5.py).
  - 1 .py file where the data extraction from the web page is shown in order to build the database(scarping_trademe_2).
  - 1 file as documentation with information about the dataset, cleaning process, results and   conclusions(documentation trademe house.docx).

To run the executable file will be needed to download first the dataset (house_trademe3 18-04.csv)


## To DO

Improve the data set by collecting more data from different sources.

Apply different techniques such as feature engineering to obtain better prediction models.

Try with different algorithms like Gradient Boosting or AdaBoost.

# Contact Details
Email: principi.bruno@gmail.com
