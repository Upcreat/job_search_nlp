from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

############################################################################################
# Import shared components

from assets.footer import _footer
from assets.nav import _nav

# Upload data
Loc_list = pd.read_csv('data/job_info_dash.csv', sep='|', usecols=['Main Location'])
Loc_list = list(Loc_list['Main Location'].unique())
Loc_list.sort()

############################################################################################

_search_nav = html.Div([
    dbc.Row([
        dbc.Col([_nav], width = 12)
    ]),
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([
            html.P([html.B(['Welcome!!! ']), 'This webapp enables semantic search on job posts, using a pre-trained model based on sBERT'], className='par')        
        ], width = 10),
        dbc.Col([], width = 1),
    ]),
    dbc.Row([
        dbc.Col([], width = 6),
        dbc.Col([
            dcc.Dropdown(options=Loc_list, value='', searchable=True, placeholder='Filter Location', persistence=True, 
                         persistence_type='session', id='loc-dropdown', multi=True)
        ], width = 5),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([
            dcc.Textarea(id = 'search-input', placeholder="Type sentencentes (one per line) describing what you're looking for",
                         className= "search-area", persistence = True, persistence_type = 'session')
        ], width = 10),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([], width = 9),
        dbc.Col([
            html.Button('Search', id='search-button', n_clicks=0, className='my-button'),
        ], width = 3)
    ]),
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([html.Hr([], className = 'hr-footer')], width = 10),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([_footer], width = 12)
    ])
], className = 'searchnav')