# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 21:15:04 2023

@author: Ronnie Chan
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import re
pio.templates.default = 'ggplot2'

# *******************************************************************************
# Load Datasets
auto = pd.read_csv('../data/automotive_cleaned.csv', parse_dates = ['Date']).drop('Unnamed: 0', axis = 1)
food = pd.read_csv('../data/food_cleaned.csv', parse_dates = ['Date']).drop('Unnamed: 0', axis = 1)
consumer = pd.read_csv('../data/consumer_cleaned.csv', parse_dates = ['Date']).drop('Unnamed: 0', axis = 1)
medical = pd.read_csv('../data/medical_cleaned.csv', parse_dates = ['Date']).drop('Unnamed: 0', axis = 1)
all_items = pd.read_csv('../data/all_items_cleaned.csv', parse_dates = ['Date']).drop('Unnamed: 0', axis = 1)


# select data recorded from 2011 to 2022 for a more accurate interpretation
get_df = lambda df: df.query("Year<2023")

auto = get_df(auto)
food = get_df(food)
consumer = get_df(consumer)
medical = get_df(medical)
all_items = get_df(all_items)

# ********************************** PLOTS ************************************
# *****************************************************************************
# PLOTS FOR ALL ITEMS
# >>> Bar chart - All Items

bar_allItems = go.Figure()
colors_list = px.colors.diverging.Geyser[::2]
list_df = [auto, food, consumer, medical]
labels_df = ['Vehicles', 'Food', 'Consumer', 'Medical']

for (df, name_df, color) in zip(list_df, labels_df, colors_list):
    df = pd.DataFrame(df.query("Year>2017").groupby('Year')['Nb_affected_models'].count())
    bar_allItems.add_trace(go.Bar(x = df.index, 
                                  y = df['Nb_affected_models'], 
                                  name = name_df, 
                                  marker = {'color': color}))
# set title and texts
bar_allItems.update_layout(legend_title = 'Legend', 
                           xaxis_title = 'Year', 
                           yaxis_title = 'Number of Recalled Items', 
                           title = 'Overview of Recalled Items in Canada from 2011 to 2022')

bar_allItems.update_xaxes(dtick="M1", tickformat="%b\nY")


# >>> Line Chart - All Items

list_df = [all_items, auto, food, consumer, medical]
labels_df = ['All Items', 'Vehicles', 'Food', 'Consumer', 'Medical']
colors = px.colors.diverging.Geyser

line_allItems = go.Figure()
for (df, name_df, color) in zip(list_df, labels_df, colors):
    
    df = pd.DataFrame(df.groupby('Year')['Nb_affected_models'].count())
    line_allItems.add_trace(go.Scatter(x = df.index, 
                                       y = df['Nb_affected_models'], 
                                       name = name_df, 
                                       marker = {'color':color}))

# set title and x-axis
line_allItems.update_layout(xaxis_title = 'Year', 
                            yaxis_title = 'Number of Recalled Items', 
                            legend_title = 'Legend', 
                            title = 'Overview of Recalled Items in Candada from 2011 to 2022',
                            hovermode="x unified")

line_allItems.update_xaxes(dtick="M1", tickformat="%b\nY")


# >>> Pie Chart - All Items

pie_allItems = go.Figure()
all_counts = all_items['Recall Category'].value_counts()
pie_allItems.add_trace(go.Pie(values = all_counts, 
                              labels = all_counts.index, 
                              showlegend = False, hole = 0.4,
                              textinfo = 'label+percent', textposition= 'inside', 
                              marker = {'colors': px.colors.diverging.Geyser[::2]}))

# ********************************** PLOTS ************************************
# *****************************************************************************
# PLOTS FOR VEHICLES
# >>> Bar chart - Vehicles

# find the most common issue for each brand
auto_brands = pd.DataFrame(auto.Brand.value_counts().head(10))
brand_issues = []
for brand in auto_brands.index:
    df = auto.loc[auto.Brand == brand]
    issue = df.Issue.mode()[0]
    brand_issues.append(issue)

# Bar plot with the most common issue for each brand
bar1_auto = go.Figure(data=[go.Bar(x = auto_brands.Brand, 
                                   y = auto_brands.index,
                                   text = [brand for brand in brand_issues], orientation = 'h',
                                   textposition = 'inside', marker = {'color': px.colors.diverging.Geyser})])

# set title and text 
bar1_auto.update_layout(xaxis_title = 'Number of Recalled Vehicles', 
                        yaxis_title = 'Brand',
                        title ='Top 10 Brands/Issues of the Vehicle Recalls',
                        hovermode="x")


# >>> Bar chart - Vehicles

auto_gr = auto.Issue.value_counts().head(10)
bar2_auto = go.Figure(data=[go.Bar(x = auto_gr, 
                                   y = auto_gr.index, orientation = 'h', 
                                   marker = {'color': px.colors.diverging.Geyser})])

# set title and text 
bar2_auto.update_layout(xaxis_title = 'Number of Recalled Vehicles', 
                        yaxis_title = 'Brand',
                        title ='Top 10 Issues of the Vehicle Recalls' ,
                        hovermode="x")

# ********************************** PLOTS ************************************
# *****************************************************************************
# PLOTS FOR FOOD
# >>> Line chart - Food

# Create dataframe for each Recall class to plot Timeseries
class1 = food.loc[food['Recall class'] == 'Class 1']
class2 = food.loc[food['Recall class'] == 'Class 2']
class3 = food.loc[food['Recall class'] == 'Class 3']

# create list
df_food_list = [class1,class2,class3]
food_class = ['Class 1', 'Class 2', 'Class 3']

# Plot Line Chart
colors = px.colors.diverging.Geyser[::2]
line_food = go.Figure()
lines_chart = []
for (df, name_df, color) in zip(df_food_list, food_class, colors):
        
    df = pd.DataFrame(df.groupby('Year')['Item'].count())
    lines_chart.append(go.Scatter(x = df.index, 
                                  y = df['Item'], 
                                  name = name_df, 
                                  marker = {'color': color}))

line_food.add_traces(lines_chart)

# set title and x-axis
line_food.update_layout(xaxis_title = 'Year', 
                        yaxis_title = 'Number of Recalled Items', 
                        legend_title = 'Recall Class', 
                        title ='Recalled Food Items in Canada from 2011 to 2022',
                        hovermode="x")

line_food.update_xaxes(dtick="M1", tickformat="%b\nY")


# >>> Interactive plots - Pie Charts - Food

# prepare data for pie charts
def clean_food_subissue(subissue):
    """
    This functions helps cleaning the 'Sub Issue' column string entry by removing the redundant repetitive values.
    
    :param [subissue]: subissue with the following format: "Food Category - [Sub Iissue], [Sub Iissue], ..."
    :type [subissue]: string
    
    :return : subissue 
    :rtype: string
    """
    if ' - ' in subissue:
        subissue = subissue.split(' - ')[1].split(',')[0]
    else:
        subissue = f'{subissue}-Not Specified'
    
    if subissue == 'pathogenic E. coli':
        subissue = 'E. coli O157:H7'
    
    if re.search(r"\bFish\b|\bCrustacean\b", subissue):
        subissue = 'Fish/Crustacean/Shellfish'
    return subissue


# create dataframes for the anaylysis of food issues
foodIssue = pd.DataFrame(food['Food_Issue'].value_counts())

# create a dataframe for Microbiological issue and clean Microbiological 'Sub Issue' column
microbiological = food.query("Food_Issue == 'Microbiological Contamination'")
microbiological['Sub Issue'] = microbiological['Sub Issue'].apply(lambda subissue: clean_food_subissue(subissue))
microbiological = pd.DataFrame(microbiological['Sub Issue'].value_counts())

# create a dataframe for Allergen issue and clean Allergen 'Sub Issue' column
allergen = food.query("Food_Issue == 'Allergen'")
allergen['Sub Issue'] = allergen['Sub Issue'].apply(lambda subissue: clean_food_subissue(subissue))
allergen = pd.DataFrame(allergen['Sub Issue'].value_counts())


# Plot Pie Charts - Food
pie_food = go.Figure()
pie_food.add_traces(go.Pie(values = foodIssue.Food_Issue, 
                           labels = foodIssue.index, 
                           showlegend = False,
                           textinfo = 'label+percent', textposition = 'inside', 
                           marker = {'colors': px.colors.diverging.Geyser})) 

pie_food.add_traces(go.Pie(values = microbiological['Sub Issue'], 
                           labels = microbiological.index, 
                           showlegend = False,
                           textinfo = 'label+percent', textposition = 'inside', 
                           marker = {'colors': px.colors.diverging.Geyser})) 
    
pie_food.add_traces(go.Pie(values = allergen['Sub Issue'], 
                           labels = allergen.index, 
                           showlegend = False,
                           textinfo = 'label+percent', textposition = 'inside', 
                           marker = {'colors': px.colors.diverging.Geyser})) 

# set dropdown buttons
pie_food.update_layout(
    updatemenus=[
        dict(
            type = "buttons",
            direction = "down",
            pad = {'r':2, "t" :2},
            showactive = True,
            x = 0.2, xanchor = "right",
            y = 1.1, yanchor = "top",
            
            buttons=list([
                
                dict(label="Food Issues",
                     method="update",
                     args=[{"visible": [True, False, False]},
                           {"title": 'Issues of Food Recalls'}]),
                
                dict(label="Food Issues - Microbiological",
                     method="update", 
                     args=[{"visible": [False, True, False]},
                           {"title": "Food Recalls - Microbiological Issue"}]),
                
                dict(label="Food Issues - Allergen",
                     method="update", 
                     args=[{"visible": [False, False, True]},
                           {"title": "Food Recalls - Allergen Issue"}])
            ]),
        )
    ])

# set title and x-axis
pie_food.update_layout(title ='Issues of Food Recalls')

# ********************************** PLOTS ************************************
# *****************************************************************************
# PLOTS FOR CONSUMER PRODUCT
# >>> Bar chart #1 - CONSUMER

consumer_issues = consumer['Issue'].value_counts().head(10)
bar1_consumer = go.Figure(data=[go.Bar(x = consumer_issues.values, 
                                       y = consumer_issues.index,
                                       orientation = 'h', 
                                       marker = {'color': px.colors.diverging.Geyser})])

# set title and text 
bar1_consumer.update_layout(xaxis_title = 'Number of Recalled Items', 
                            yaxis_title = 'Issues', hovermode="x",
                            title ='Top 10 Issues of Product Recalls')

# >>> Bar chart #2 - CONSUMER

# prepare the dataframe for the plots
consumer_categories = pd.DataFrame(consumer['Category'].value_counts()).head(10)
percent = pd.DataFrame(consumer['Category'].value_counts(normalize = True)) * 100

# find the most common issue for each category
consumer_issues = []
for category in consumer_categories.index:
    df = consumer.loc[consumer.Category == category]
    issue = df.Issue.mode()[0]
    consumer_issues.append(issue)

# Bar plot with the most common issue for each brand
bar2_consumer = go.Figure(data=[go.Bar(x = consumer_categories.Category, 
                                       y = consumer_categories.index, 
                                       orientation = 'h',
                                       text = [f'{issue} - {round(percent)}%' for (issue, percent) in zip(consumer_issues, percent.Category)],
                                       textposition = 'inside',
                                       marker = {'color': px.colors.diverging.Geyser})])

# set title and text 
bar2_consumer.update_layout(xaxis_title = 'Number of Recalled Items', 
                            yaxis_title = 'Category', 
                            title ='Top 10 Categories/Issues of Product Recalls',
                            hovermode="x")

# ********************************** PLOTS ************************************
# *****************************************************************************
# PLOTS FOR MEDICAL PRODUCT
# >>> Line chart - Medical

# Create dataframe for each Recall class
type1 = medical.loc[medical['Recall class'] == 'Type I']
type2 = medical.loc[medical['Recall class'] == 'Type II']
type3 = medical.loc[medical['Recall class'] == 'Type III']

# create list
df_medical_list = [type1, type2, type3]
medical_type = ['Type I', 'Type II', 'Type III']
colors = px.colors.diverging.Geyser[::2]

# Plot Line Chart - Medical
line_medical = go.Figure()
lines_chart = []

for (df, name_type, color) in zip(df_medical_list, medical_type, colors):
        
    df = pd.DataFrame(df.groupby('Year')['Item'].count())
    lines_chart.append(go.Scatter(x = df.index, 
                                  y = df['Item'], 
                                  name = name_type, 
                                  marker = {'color':color}))
 
line_medical.add_traces(lines_chart)   # plot lines

# set title and x-axis
line_medical.update_layout(xaxis_title = 'Year', 
                           yaxis_title = 'Number of Recalled Items', 
                           legend_title = 'Recall Class', 
                           title ='Recalled Medical Items in Canada from 2018 to 2022',
                           hovermode="x")

line_medical.update_xaxes(dtick="M1", tickformat="%b\nY")


# >>> Bar Chart - Medical

medical_gr = medical['Issue'].value_counts().head(5)
bar_medical = go.Figure(data=[go.Bar(x = medical_gr.values, 
                                     y = medical_gr.index,
                                     orientation = 'h', 
                                     marker = {'color': px.colors.diverging.Geyser})])

# set title and text 
bar_medical.update_layout(xaxis_title = 'Number of Recalled Items', 
                          yaxis_title = 'Issues', 
                          hovermode="x",
                          title ='Top 5 Issues of Product Recalls')