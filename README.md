# Data Analysis on Canada Recalls

This repository contains the files for my final capstone project at Concordia Data Science Bootcamp. The project focuses on analyzing Canada's recall records from 2011 to March 2023. The analysis will involve the following tasks:

1. Data scraping to collect the datasets.
2. Data cleaning to preprocess the raw data.
3. Categorization of data into segments such as vehicles, food, customer and medical products, and issues of the recalls.
4. Visualization of the analyzed data using Plotly.
5. Deployment of the findings in the application (see [GitHub repo](https://github.com/chanronnie/canada-recalls-app)).


## Table of Contents

* [Technologies](#technologies)
* [Installation](#installation)
* [Data](#data)
* [Contents](#contents)
* [Dashboard Preview](#dashboard-preview)


## Technologies
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-grey?style=for-the-badge)

## Installation
```
pip install beautifulsoup4
pip install plotly
```
## Data
Items recalled by the government of Canada are scrapped from the [Canada Recalls](https://recalls-rappels.canada.ca/en/search/site) website. I used Python and BeautifulSoup to perform the data scraping process.
There are a total of 14,218 recalled items to be collected from the website covering the period from 2011 to March 2023.


## Contents
* Acess the raw and processed datasets: [data](/data) 
* View the Python code for data scraping: [Data Scraping.ipynb](Data%20Scraping.ipynb)
* View the Python code for data cleaning: [Data Cleaning.ipynb](Data%20Cleaning.ipynb)
* View my data analysis project on Jovian: [Notebook](https://jovian.com/ronniekkc/canada-recalls-data-analysis)

📍 App link: [recallsdashboard.pythonanywhere.com](https://recallsdashboard.pythonanywhere.com/)

## Dashboard Preview
Please feel free to adjust the window size to your convenience if it appears too big.</br>
If you encounter any issues or have suggestions, please open an issue.

<img width="469" alt="preview5" src="https://github.com/chanronnie/CanadaRecalls_CapstoneProject/assets/121308347/4c3a8e54-7294-43b9-9a64-fade3b5c353e">

