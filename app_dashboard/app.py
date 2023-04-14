# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 16:45:46 2023

@author: Ronnie Chan
"""

# import libraries
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from dash import Dash, Output, Input, dcc, html, ctx
import dash_mantine_components as dmc
import warnings
warnings.filterwarnings("ignore")

# import plots/graphs from the file "figures.py"
from figures import (all_items,
                     bar_allItems, pie_allItems, line_allItems, 
                     bar1_auto, bar2_auto, 
                     line_food, pie_FoodIssue, pie_Microbiological, pie_Allergen,
                     bar1_consumer, bar2_consumer, 
                     bar_medical, line_medical)

# *********************************** APP *************************************
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.SANDSTONE],
           suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])

server = app.server

def create_button(icon_code, button_name, id_button):
    """
    This function creates a button from Dash-Bootstrap-Components library with the given icon and name.
    
    :param [icon_code]: code of the icon from DashIconify library
    :param [button_name]: label of the button
    :param [id_button]: ID of the button
    :type [icon_code]: string
    :type [button_name]: string
    :type [id_button]: string
    
    :return: a button of Dash Bootstrap Component library
    :rtype: dbc.Button

    """
    dash_icon = DashIconify(icon=icon_code, style={"marginRight": 10, 'font-size': '30px'})
    button_style = style={'font-size': '20px','border-radius': '5px', 'display':'inline-block'}
    return dbc.Button([dash_icon, button_name], 
                      id = id_button, 
                      n_clicks=0, 
                      outline = False, 
                      style = button_style,
                      color="dark", className="mx-1")
    

# create buttons with Icons
button_group = dbc.ButtonGroup([
    
    create_button("material-symbols:overview-outline", "Overview", "button-overview"),
    create_button("material-symbols:car-crash-rounded", "Vehicles", "button-vehicles"),
    create_button("mdi:food-fork-drink", "Food", "button-food"),
    create_button("material-symbols:shopping-cart-rounded", "Consumer", "button-consumer"),
    create_button("material-symbols:health-metrics-rounded", "Medical", "button-medical")
    
    ],style={"width": "100%"}
)


# app layout
app.layout = dbc.Container([dbc.Card(dbc.CardBody([
  
    dbc.Row([
             # Title 
             dbc.Col([html.H1(children = "Analytics Dashboard for Canada Recalls", 
                              style={'display':'inline-block', 'font-size':'40px'}, 
                              className = 'text-white text-start mt-3 ms-2')], 
                     style = {'background':'black'}, width = 2),
        
             # Line Plot 
             dbc.Col([dbc.Card(dbc.CardBody([
                 html.P(dcc.Graph(id = 'linechart', figure = line_allItems))]), className = 'border-0')],width = 7), 
            
            # Display Total number of recalls
             dbc.Col([
                 html.H4('Total Number of Recalled Items', className = 'text-start mt-4 ms-2'), 
                 html.Div('From 2011 to 2022', className = 'text-start ms-2'),
                 html.Div(f"{all_items.shape[0]:,}", className = 'd-flex justify-content-center align-items-center p-5 m-5',
                          style={'font-size':'80px', "font-weight": "bold", 'color':'grey'})],
                                
                 className = 'border-0 bg-white', width = 3)],
             justify="center"),
    
    html.Br(),
    
    # Buttons
    dbc.Row([dbc.Col(style = {'background':'black'}, width = 2),
             dbc.Col(button_group, width = 10)]),
    
    html.Br(),
    
    # Text and Graphs at the bottom
    dbc.Row([
        
            # Presentation of my project
            dbc.Col([html.P("This is an interactive analytics dashboard for the items being recalled \
                            by the Governement of Canada from 2011 to 2022. The data is obtained \
                            from doing a data scraping process.",
                            className = 'text-white fs-6 text mt-4 ms-2 me-2'),
                     html.Div(dcc.Link("Source: Recalls and safety alerts", href = 'https://recalls-rappels.canada.ca/en/search/site'), className = 'ms-2'),
                     html.Div("Author: Ronnie Chan", className = 'text-white text-start ms-2 me-2 mt-3'),
                     html.Div("Updated: 2023-04-13", className = 'text-white text-start ms-2'),
                     
                     # Links to my codes
                     html.Div([dbc.Button(
                         [DashIconify(icon='radix-icons:github-logo', style={"marginRight": 5, 'font-size': '20px'}), "GitHub Repo"],
                         href="https://github.com/chanronnie/Capstone-Project",
                         external_link=True,
                         color="dark", 
                         className="text-start ms-2")
                         ]),
                     
                     html.Div([dbc.Button(
                         [DashIconify(icon='logos:jupyter', style={"marginRight": 5, 'font-size': '20px'}), "Data Analysis Notebook"],
                         href="https://jovian.com/ronniekkc/canada-recalls-data-analysis",
                         external_link=True,
                         color="dark", 
                         className="text-start m-2"
                         )]),
                     
                     
                    ],style = {'background':'black'}, width = 2),
        
            # Plots at the bottom of the webpage
            dbc.Col([dbc.Card(dbc.CardBody([
                html.P(id = 'graphLeft', children = [])]),className = 'border-0')], width = 5),

            dbc.Col([dbc.Card(dbc.CardBody([
                 html.P(id = 'graphRight', children = [])]),className = 'border-0')], width = 5)],
             
            justify="center"),
    

    ]),style = {'background':'#EFEFEF'})
], fluid=True)


# callback for the Buttons
@app.callback(
    [Output(component_id='graphLeft', component_property='children'), 
    Output(component_id='graphRight', component_property='children')],
    [Input(component_id='button-overview', component_property="n_clicks"),
     Input(component_id='button-vehicles', component_property="n_clicks"),
     Input(component_id='button-food', component_property="n_clicks"),
     Input(component_id='button-consumer', component_property="n_clicks"),
     Input(component_id='button-medical', component_property="n_clicks")]
)


def display_graphs(b1,b2,b3,b4,b5):
    """
    This function returns 2 outputs (or 2 graphs) after clicking one of the buttons.
    
    :param[b1,b2,b3,b4,b5]: buttons of type Dash-Bootstrap-Components
    :type [b1,b2,b3,b4,b5]: dbc.Button
    
    :return : 2 plots of the corresponding button chosen
    :rtype: Plotly figures
    
    """
    
    button_clicked = ctx.triggered_id

    figLeft = None
    figRight = None
    plot_figure= lambda fig: dcc.Graph(figure = fig)
    
    # display the graphs of all recalled items as default (if no button is clicked)
    if button_clicked is None:
        figLeft = bar_allItems
        figRight = pie_allItems
    
    # Display plots if "Overview" is selected
    if button_clicked == 'button-overview':
        figLeft = bar_allItems
        figRight = pie_allItems
    
    # Display plots if "Vehicles" is selected
    elif button_clicked=='button-vehicles': 
        figLeft = bar1_auto
        figRight = bar2_auto
    
    # Display plots if "Food" is selected
    elif button_clicked=='button-food': 
        
        # for Food category
        # create segmented controls to let users to choose which Pie Chart to visualize
        segmented_controls = dbc.Row([
            
            dmc.SegmentedControl(
                id="segmented",
                value="foodIssue",
                radius = 'md',
                data=[
                    {"value": "foodIssue", "label": "Food Issues"},
                    {"value": "microbiological", "label": "Food Issues - Microbiological"},
                    {"value": "allergen", "label": "Food Issues - Allergen"},
                    ],
                )
            , dbc.Col([dcc.Graph(id = 'pie_food', figure = {}, style = {'margin-bottom':-45})],style = {'margin-bottom':10})])
        
        return plot_figure(line_food), segmented_controls
    
    # Display plots if "Consumer Product" is selected
    elif button_clicked=='button-consumer': 
        figLeft = bar1_consumer
        figRight = bar2_consumer
    
    # Display plots if "Medical Product" is selected
    elif button_clicked=='button-medical': 
        figLeft = line_medical
        figRight = bar_medical
    
    return plot_figure(figLeft), plot_figure(figRight)


# callback for the Selected Controls (Food Category)
@app.callback(
    Output(component_id='pie_food', component_property='figure'), 
    Input("segmented", "value")
)
                
def select_value(value):
    """
    This function returns the corresponding Food Pie Chart 
    
    :param [value]: value selected from the selected controls in the food category
    :value [value]: string
    
    :return : pie chart describing the food issues
    :rtype : plotly go.Figure()
    
    """
    
    if value == 'foodIssue':
        return pie_FoodIssue
    elif value == 'microbiological':
        return pie_Microbiological
    elif value == 'allergen':
        return pie_Allergen
            


if __name__ == '__main__':
    app.run_server(debug=False)