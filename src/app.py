#!/usr/bin/env python
# coding: utf-8

# Importación de los módulos necesarios:

from jupyter_dash import JupyterDash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np


# Importación del conjunto de datos de GapMinder


df = px.data.gapminder()


# Definición de la aplicación:

app = JupyterDash(__name__)

server = app.server

app.layout = html.Div(children = [dcc.Dropdown(id="year", value=2007, clearable=False, placeholder="Select a year",
                                               options=[{"label": y, "value": y} for y in df['year'].unique()]),
                                  dcc.Graph(id="main_graph", figure={}),
                                  dcc.Graph(id="deri_graph", figure={}),
                                  ])

@app.callback(Output('main_graph','figure'), Input('year', 'value'))
def cb(year):
  df_year=df.query("year == @year")
  fig = px.scatter(df_year,x="gdpPercap",y="lifeExp",hover_name="country",color="continent",log_x=True,
           title="World Life Expectancy vs. GDP/Capita for %d" % year, 
##           trendline='lowess',
           labels=dict(
              continent="Continent",
              gdpPercap="GDP per capita (USD price-adjusted)",
              lifeExp="Life Expectancy (years)"))
    
##  html_data = fig.to_html(full_html=False, include_plotlyjs='cdn')
##  html_plot = html.IFrame(srcDoc=html_data)
  return fig
  
@app.callback(Output('deri_graph','figure'), Input('main_graph','clickData'))
def display_selected_data(clickData):
  selected_country = 'Colombia'
  df_country = df.loc[df['country'] == selected_country]
  if clickData:
    selected_country = clickData['points'][0]['hovertext']
    try:
      df_country = df.loc[df['country'] == selected_country]
    except:
      pass
  fig = px.line(df_country,x="year",y="lifeExp",hover_name="lifeExp",color="continent",title="Life Expectancy evolution for %s" % selected_country, markers=True,
                    labels=dict(
                        year="Year",
                        lifeExp="Life Expectancy (years)",
                        continent="Continent"))
##  htlm_data = fig.to_html(full_html=False, include_plotlyjs='cdn')
##  htlm_plot = html.IFrame(srcDoc=html_data)
  
  return fig #html_plot 

if __name__ == "__main__":
    app.run_server(debug=True)





