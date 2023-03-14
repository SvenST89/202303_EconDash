# Standard libs for data manipulation
import pandas as pd
import numpy as np
# For Visualization
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
from IPython.core.pylabtools import figsize
#------------------------------------------#
# my functions
from assist.data import *
from assist.viz import *
from assist.fmp import *
from treemap import make_treemap
import logging
import json

#===============================#
# SET LOGGING
#===============================#

logger=logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)

# set logging handler in file
fileHandler=logging.FileHandler(filename="log/main.log", mode='w')
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

# set logging handler in console
consoleHandler=logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)

#===============================#
# YIELD CURVE
#===============================#
# Read in ECB SDW time series keys from 3-month residual maturity until 30-years residual maturity
# for all ratings and all issures
keys_list=pd.read_excel('data/keys.xlsx', sheet_name='Tabelle1')['keys'].tolist()
yieldCurve_df=get_ecb_data(keys_list) # format start string %Y-%m-%d

print(yieldCurve_df.head())

# Plot interactive Yield Curve figure with graph objects
import plotly.graph_objects as go

CHART_THEME = 'plotly_white' #'plotly_white'; different themes available: https://plotly.com/python/templates/

fig = go.Figure()
fig.add_trace(go.Scatter(x=yieldCurve_df["Maturity"], y=yieldCurve_df["Value"], mode="lines", hovertemplate="Maturity=%{x}years<br>Value=%{y}")) #line=go.scatter.Line(color="purple", width=4),
fig.layout.template=CHART_THEME
fig.layout.height=500
fig.update_layout(
    xaxis=dict(
        title="Residual Maturity in years",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    yaxis=dict(
        title="Yield in %",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        zeroline=False,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    margin=dict(
        b=50,
        l=25,
        r=25,
        t=50
    ),
    # plot_bgcolor='black',
    # paper_bgcolor='black',
    # font_color='grey',
    # autosize=True
)

# annotations = []

# # Title
# annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
#                               xanchor='left', yanchor='bottom',
#                               #text='ECB Yield Curve Term Structure',
#                               font=dict(family='Arial',
#                                         size=30,
#                                         color='rgb(129,129,135)'),
#                               showarrow=False))
# # Source
# annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
#                               xanchor='center', yanchor='top',
#                               text='0.25=3months, 0.50=6months, 0.75=9months',
#                               font=dict(family='Arial',
#                                         size=10,
#                                         color='rgb(150,150,150)'),
#                               showarrow=False))
# #fig.update_yaxes(range=[yieldCurve_df["Value"].min(), yieldCurve_df["Value"].max()], showticklabels=True, gridcolor='darkgrey', showgrid=False)
# fig.update_layout(annotations=annotations)
#fig.show()

#===============================#
# Stock Heatmap
#===============================#

treemap=make_treemap()

#===============================#
# Stock Carousel
#===============================#
tickers=pd.read_excel("data/ticker.xlsx", sheet_name="dax")

ticker_list=tickers['ticker'].tolist()

carousel_prices={}
# Get Sentiment of Stock
for ticker in ticker_list:
    carousel_prices[ticker]=stock_pctchange(ticker)/100

with open("carousel_prices.json", "w") as outfile_prices:
    json.dump(carousel_prices, outfile_prices)

# Load the json-file for carousel prices again for later use in dashboard
carousel_prices = json.load(open("carousel_prices.json", "r"))
#===============================#
# PMI Data
#===============================#
pmi_df=pd.read_excel('data/pmi.xlsx', sheet_name='PMI')

pmi_fig = go.Figure()
pmi_fig.add_trace(go.Scatter(x=pmi_df["Release Date"], y=pmi_df["USA"], mode="lines", hovertemplate="Country: USA<br>Release Date: %{x}<br>Value: %{y}", name='USA'))#line=go.scatter.Line(color="blue", width=4), 
pmi_fig.add_trace(go.Scatter(x=pmi_df["Release Date"], y=pmi_df["GER"], mode="lines", hovertemplate="Country: GER<br>Release Date: %{x}<br>Value: %{y}", name='Germany'))#line=go.scatter.Line(color="red", width=4), 
pmi_fig.add_trace(go.Scatter(x=pmi_df["Release Date"], y=pmi_df["FR"], mode="lines", hovertemplate="Country: FR<br>Release Date: %{x}<br>Value: %{y}", name='France'))#line=go.scatter.Line(color="green", width=4), 
pmi_fig.layout.template=CHART_THEME
pmi_fig.layout.height=300
pmi_fig.update_layout(
    xaxis=dict(
        title="Release Date",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    yaxis=dict(
        title="PMI Index Value",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        zeroline=False,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    margin=dict(
        b=50,
        l=25,
        r=25,
        t=50
    ),
    # plot_bgcolor='black',
    # paper_bgcolor='black',
    # font_color='grey',
    # autosize=True
)

# annotations_pmi = []
# # Title
# annotations_pmi.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
#                               xanchor='left', yanchor='bottom',
#                               #text='Composite PMI Data',
#                               font=dict(family='Arial',
#                                         size=30,
#                                         color='rgb(129,129,135)'),
#                               showarrow=False))
# pmi_fig.update_layout(annotations=annotations_pmi)
#pmi_fig.show()

#===============================#
# Euro Area Inflation Data
#===============================#
infkeys_list=pd.read_excel('data/keys.xlsx', sheet_name='inflation')['keys'].tolist()
inflation_df=get_other_data(infkeys_list, country_list=["DE", "FR", "I8"]) # format start string %Y-%m-%d
print(inflation_df)

inf_fig = go.Figure()
inf_fig.add_trace(go.Scatter(x=inflation_df.index, y=inflation_df["I8"], mode="lines", hovertemplate="Country: Euro Area<br>Date: %{x}<br>Value: %{y}", name='Euro Area'))#line=go.scatter.Line(color="blue", width=4),
inf_fig.add_trace(go.Scatter(x=inflation_df.index, y=inflation_df["DE"], mode="lines", hovertemplate="Country: GER<br>Date: %{x}<br>Value: %{y}", name='Germany'))#line=go.scatter.Line(color="red", width=4), 
inf_fig.add_trace(go.Scatter(x=inflation_df.index, y=inflation_df["FR"], mode="lines", hovertemplate="Country: FR<br>Date: %{x}<br>Value: %{y}", name='France'))#line=go.scatter.Line(color="green", width=4), 
inf_fig.layout.template=CHART_THEME
inf_fig.layout.height=300
inf_fig.update_layout(
    xaxis=dict(
        title="Date",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    yaxis=dict(
        title="Inflation (HICP, Overall Index)",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        zeroline=False,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    margin=dict(
        b=50,
        l=25,
        r=25,
        t=50
    ),
    # plot_bgcolor='black',
    # paper_bgcolor='black',
    # font_color='grey',
    # autosize=True
)

# annotations_inf = []
# # Title
# annotations_inf.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
#                               xanchor='left', yanchor='bottom',
#                               #text='HICP Inflation Data (p.a. in %)',
#                               font=dict(family='Arial',
#                                         size=30,
#                                         color='rgb(129,129,135)'),
#                               showarrow=False))
# inf_fig.update_layout(annotations=annotations_inf)
#inf_fig.show()

#===============================#
# Euro Area Debt Data
#===============================#
#--- Government Debt
govdebt_list=pd.read_excel('data/keys.xlsx', sheet_name='govdebt')['keys'].tolist()
govdebt_df=get_other_data(govdebt_list, country_list=["DE", "FR", "I8"]) # format start string %Y-%m-%d
#print(govdebt_df)
#--- Corporate Debt
corp_list=pd.read_excel('data/keys.xlsx', sheet_name='corpdebt')['keys'].tolist()
corp_df=get_other_data(corp_list, country_list=["DE", "FR", "I8"]) # format start string %Y-%m-%d
#print(corp_df)
#--- Household Debt
house_list=pd.read_excel('data/keys.xlsx', sheet_name='housedebt')['keys'].tolist()
house_df=get_other_data(house_list, country_list=["DE", "FR", "I8"]) # format start string %Y-%m-%d
#print(house_df)
#--- TOTAL DEBT DF
debt_df=govdebt_df + corp_df.values
debt_df=debt_df + house_df.values
debt_df=debt_df.round(1)
print(debt_df.head())

debt_fig = go.Figure(data=[
    go.Bar(x=debt_df.index, y=debt_df["I8"], hovertemplate="Country: Euro Area<br>Date: %{x}<br>Value: %{y}", name='Euro Area'),
    go.Bar(x=debt_df.index, y=debt_df["DE"], hovertemplate="Country: GER<br>Date: %{x}<br>Value: %{y}", name='Germany'),
    go.Bar(x=debt_df.index, y=debt_df["FR"], hovertemplate="Country: FR<br>Date: %{x}<br>Value: %{y}", name='France')
])
#debt_fig.add_trace(go.bar(x=debt_df.index, y=debt_df["I8"], hovertemplate="Country: Euro Area<br>Date: %{x}<br>Value: %{y}", name='Euro Area'))#line=go.scatter.Line(color="blue", width=4),
#debt_fig.add_trace(go.bar(x=debt_df.index, y=debt_df["DE"], hovertemplate="Country: GER<br>Date: %{x}<br>Value: %{y}", name='Germany'))#line=go.scatter.Line(color="red", width=4), 
#debt_fig.add_trace(go.bar(x=debt_df.index, y=debt_df["FR"], hovertemplate="Country: FR<br>Date: %{x}<br>Value: %{y}", name='France'))#line=go.scatter.Line(color="green", width=4), 
debt_fig.layout.template=CHART_THEME
debt_fig.layout.height=300
debt_fig.update_layout(barmode='group')
debt_fig.update_layout(
    xaxis=dict(
        title="Date",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    yaxis=dict(
        title="Aggregated Debt Level (in %)",
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        zeroline=False,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='rgb(136, 136, 138)',
        ),
    ),
    margin=dict(
        b=50,
        l=25,
        r=25,
        t=50
    ),
    # plot_bgcolor='black',
    # paper_bgcolor='black',
    # font_color='grey',
    # autosize=True
)



#===============================#
# APP LAYOUT
#===============================#
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_trich_components as dtc
from dash.dependencies import Output, Input

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container(
    [
        # row 0: offset, for styling purposes
        dbc.Row([
            dtc.Carousel([
                html.Div([
                    # Span showing name of the stock
                    html.Span(stock, style={'margin-left':'80px'}),
                    # Now, this span shows the variation of the stock
                    html.Span('{}{:.2%}'.format('+' if carousel_prices[stock] > 0 else '', carousel_prices[stock]), style={
                        'color': 'green' if carousel_prices[stock] > 0 else 'red', 'margin-left':'20px'})
                ]) for stock in sorted(carousel_prices.keys())
            ], id='main-carousel', autoplay=True, slides_to_show=5),
        ]),
        # row 1
        dbc.Row([
            # column 1
            dbc.Col([html.H2('ECONOMIC ASSISTANT DASHBOARD', style={'margin-top': '12px', 'margin-left': '48px', 'margin-bottom': '16px'}, className='text-center text-primary, mb-3')], width={'size': 10, 'offset': 0, 'order': 0}), # the max size of a screen is width=12!
            dbc.Col([html.Img(src="assets/logo_vertical_darkgrey.png", style={'height': '50%', 'width':'50%', 'margin-top':'12px', 'margin-left':'16px'})], width={'size': 2, 'offset': 0, 'order': 0})
        ], justify='start'),
        # row 2
        dbc.Row([
            # column 1
            dbc.Col([
                html.H5('Euro Area: Yield Curve Term Structure', className='text-center'),
                dcc.Graph(
                    id='yieldchart',
                    figure=fig,
                    style={'height': 550, 'margin-bottom': '14px', 'margin-left':'12px'}),
                html.Hr(),
            ], width={'size': 6, 'offset': 0, 'order': 0}),
            # column 2
            dbc.Col([
                html.H5('Dax: Performance Treemap (1-Day Pct. Change)', className='text-center'),
                dcc.Graph(
                    id='treemap',
                    figure=treemap,
                    style={'height': 550, 'margin-bottom': '14px', 'margin-left':'12px'}),
                html.Hr(),
            ], width={'size': 6, 'offset': 0, 'order': 0}),
        ]),
        # row 3
        dbc.Row([
            # column 1
            dbc.Col([
                html.H5('Monthly Annual Inflation Rate (%, Overall HICP)', className='text-center'),
                dcc.Graph(
                    id='infchart',
                    figure=inf_fig,
                    style={'height': 380, 'margin-bottom': '14px', 'margin-left':'12px'}),
            ], width={'size': 6, 'offset': 0, 'order': 0}),
            # column 2
            dbc.Col([
                html.H5('Monthly Composite PMI Data', className='text-center'),
                dcc.Graph(
                    id='pmichart',
                    figure=pmi_fig,
                    style={'height': 380, 'margin-bottom': '14px', 'margin-left': '12px'}),
            ], width={'size': 6, 'offset': 0, 'order': 0}),
        ]),
        # row 4
        dbc.Row([
            # column 1
            dbc.Col([
                html.H5('Quarterly Aggregated Debt Level (in % of GDP)', className='text-center'),
                dcc.Graph(
                    id='debtchart',
                    figure=debt_fig,
                    style={'height': 380, 'margin-bottom':'14px', 'margin-left':'12px'}),
            ], width={'size': 12, 'offset': 0, 'order': 0}),
        ]),
    ], fluid=True
)

#import plotly
#import plotly.io as pio
#plotly.offline.plot(app, filename="econ_test_app.html")

if __name__=="__main__":
    app.run_server(debug=True, port=56789)


# @app.callback(
#     [
#         Output("yieldchart", "figure"), ...
#     ]
# )