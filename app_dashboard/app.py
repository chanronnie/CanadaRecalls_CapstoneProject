# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 16:45:46 2023

@author: Ronnie Chan
"""

# import libraries
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from dash import Dash, Output, Input, dcc, html, ctx
import warnings
warnings.filterwarnings("ignore")

# import plots/graphs from the file "figures.py"
from figures import (all_items,
                     bar_allItems, pie_allItems, line_allItems, 
                     bar1_auto, bar2_auto, 
                     line_food, pie_food,
                     bar1_consumer, bar2_consumer, 
                     bar_medical, line_medical)

# *********************************** APP *************************************
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.SANDSTONE],
           suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])



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
    button_style = style={'font-size': '20px','border-radius': '5px', 'display':'inline-bloc'}
    return dbc.Button([dash_icon, button_name], 
                      id = id_button, 
                      n_clicks=0, 
                      outline = True, 
                      style = button_style,
                      color="secondary", className="mx-1")
    

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
app.layout = dbc.Container([
  
    dbc.Row([
             # Title 
             dbc.Col([html.H1(children = "Canada Recalls Dashboard", 
                                     style={"textAlign": "left", 'display':'inline-bloc', 'font-size':'40px'}, 
                                     className = 'text-white m-5 ms-2'),
                     html.Div("Author: Ronnie Chan\nUpdated: 2023-04-11", className = 'text-white m-5 ms-2')],style = {'background':'black'}, width = 2),
        
             # Line Plot 
             dbc.Col([dbc.Card(dbc.CardBody([
                 html.P(dcc.Graph(id = 'linechart', figure = line_allItems, 
                                   style={'display':'inline-bloc', 'height':'80%'}))]))], width = 7), 
            
            # Card
            dbc.Col([dbc.Card(dbc.CardBody([
                html.H4('Total Number of Recall Items', className = 'mt-4 ms-2'), 
                html.Div('From 2011 to 2022', className = 'ms-2'),
                html.Div(f"{all_items.shape[0]:,}", className = 'p-5 mt-5', 
                         style={"textAlign": "center", 'display':'inline-bloc', 'font-size':'80px', "font-weight": "bold", 'color':'grey'})], 
                
                style={'height':'57vh'}))], 
                width = 3)], 
            justify="center"),    
    
    html.Br(),
    
    # Buttons
    dbc.Row([dbc.Col(style = {'background':'black'}, width = 2),
             dbc.Col(button_group, width = 10)]),
    
    html.Br(),
    
    # Graphs at the bottom
    dbc.Row([dbc.Col(style = {'background':'black'}, width = 2),
        
             dbc.Col([dbc.Card(dbc.CardBody([
                html.P(dcc.Graph(id = 'graphLeft', figure = {}, style={'display':'inline-bloc'}))]))], width = 5),
            
             dbc.Col([dbc.Card(dbc.CardBody([
                html.P(dcc.Graph(id = 'graphRight', figure = {}, style={'display':'inline-bloc'}))]))], width = 5)], justify="center"),
    
    html.Br()
    
], fluid=True)


@app.callback(
    [Output(component_id='graphLeft', component_property='figure'), 
    Output(component_id='graphRight', component_property='figure')],
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
    
    # display the graphs of all recalled items as default (if no button is clicked)
    if button_clicked is None:
        return bar_allItems, pie_allItems
    
    # display figures after clicking the button
    if button_clicked == 'button-overview':
        return bar_allItems, pie_allItems
    
    elif button_clicked=='button-vehicles': 
        return bar1_auto, bar2_auto
    
    elif button_clicked=='button-food': 
        return line_food, pie_food
    
    elif button_clicked=='button-consumer': 
        return bar1_consumer, bar2_consumer
    
    elif button_clicked=='button-medical': 
        return line_medical, bar_medical


if __name__ == '__main__':
    app.run_server(debug=True)