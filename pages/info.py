import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Info', title='NLP Job Search | Info')

############################################################################################
# Page layout

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.P([html.B(['App Overview'])], className='search-res-title')
        ], width=12)
    ]),
    # Part 1
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([html.H4(["Using the app"])], width = 10),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            html.P(["1) ", html.B("Type input sentences", className="info-text-b"), ": The app can work with up to 10 query sentences, one per line. There's a native limitation of 384 words per sentence in the sBERT model."], className='info-text'),
            html.P(["2) Optionally filter by available ", html.B("locations", className="info-text-b"),"."], className='info-text'),
            html.P(["3) Press ", html.B("Search", className="info-text-b"), " to generate embeddings and calculate similarity scores and job rankings."], className='info-text'),
            html.P(["4) ", html.B("Empedding Input", className="info-text-b"),": To get a local version of the app, insert your API token in the 'embed_api' function located in '.assets/nlp_functions.py' (further information ", html.A(["here"], href="https://huggingface.co/settings/tokens"), ")."], className='info-text')
            ], width = 9),
        dbc.Col([], width = 1)
    ]),
    # Part 2
    dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([html.H4(["Interpret results"])], width = 10),
        dbc.Col([], width = 1)
    ]),
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            html.P(["5) ", "The app will display a ", html.B("Box-Plot", className="info-text-b")," for each query sentence. This should allow to understand how strong the similarities are."], className='info-text'),
            html.P(["6) A ", html.B("Card", className="info-text-b"), " for each job is generated. All jobs are ranked based on their weighted similarities scores."], className='info-text'),
            html.P(["7) ", "Each card includes the most similar sentence found in each job description, against the corresponding input query."], className='info-text')
            ], width = 9),
        dbc.Col([], width = 1)
    ]),    
])
