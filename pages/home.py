import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
import time

dash.register_page(__name__, path='/', name='Home', title='NLP Job Search | Home')

############################################################################################
# Import functions, settings
from assets.nlp_functions import embed_api, calculate_sentences_similarity, calculate_job_similarity, calculate_ranks, generate_cards
from assets.fig_layout import my_figlayout, my_colors

############################################################################################
# Upload data
Job_Info = pd.read_csv('data/job_info_dash.csv', sep='|')
#Job_Info = Job_Info.loc[Job_Info['Main Location'] == 'Zurich', :] # Filter by one location
#Job_Info = Job_Info.iloc[:75, :]
#print("Job Info: {} records loaded".format(len(Job_Info)))

df_embeddings = pd.read_csv('data/sentences_embeddings_dash.csv', sep='|')
#print("Sentence Embeddings: {} records loaded".format(len(df_embeddings)))

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.P([html.B(['Search Results'])], className='search-res-title')
        ], width=12)
    ]),
    dcc.Loading(id = 'loading-1', type = 'default', children = [
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([
                dbc.Row([
                    dbc.Col([], width = 3),
                    dbc.Col([html.Div(id = 'input-embed-res')], width = 6),
                    dbc.Col([], width = 3)
                ]),
                dbc.Row([dbc.Col([html.Div(id = 'box-plot')], width = 12)]),
            ], width=10),
            dbc.Col([], width=1)
        ]),
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col(id='job-ranks-results', width = 10),
            dbc.Col([], width=1),
        ])
    ])
])

############################################################################################
# Page Callbacks
@callback(Output('input-embed-res', 'children'),
          Output('box-plot', 'children'),
          Output('job-ranks-results', 'children'),
          Input('browser-memo', 'data'))
def store_input(store_data):
    box_plot = None; ranked_job_results = None
    Job_Info_local = Job_Info.copy()
    df_embeddings_local = df_embeddings.copy()
    # Filter by location
    try:
        if len(store_data['input_loc']) > 0:
            Job_Info_local = Job_Info_local.loc[Job_Info_local['Main Location'].isin(store_data['input_loc']), :]
            df_embeddings_local = df_embeddings_local.loc[df_embeddings_local['Job ID'].isin(Job_Info_local['Job ID']), :]
        else:
            pass
    except:
        print("Location filter raised an error")
        raise PreventUpdate
    # Get input queries
    try:
        if len(str(store_data['search_query'])) > 0:
             input_str = store_data['search_query']
             input_list = str(input_str).split('\n') # Result is a list
             input_list = input_list[:10] # limit up to 10 sentences in the query
    except:
        print("Input text area raised an error")
        raise PreventUpdate
    # Embed input
    try:
        input_embed = embed_api(input_list)
        embed_res = dbc.Alert(children=['Query sentences embedded via Huggingface API: ', str(len(input_embed))], color='success', class_name='alert-style')
        # Calculate similarities and ranks
        similarity_df = calculate_sentences_similarity(df_embeddings_local, input_embed)
        Job_Ranks = calculate_job_similarity(Job_Info_local, similarity_df, input_embed)
        Job_Ranks = calculate_ranks(Job_Ranks, input_embed)
        # Generate box plot
        box_plot_fig = go.Figure(layout=my_figlayout)
        for j in range(len(input_embed)):
            box_plot_fig.add_trace(go.Box(y = list(Job_Ranks['Max_sim_query_'+str(j)]), name="Query_"+str(j), marker_color=my_colors[j],
                                          jitter=0.3, boxpoints='all', pointpos=-1.8)) # represent all points with relative position
        box_plot_fig.update_layout(title_text="Box Plot of queries similarity scores")
        box_plot = dcc.Graph(id='sim-box', className='my-graph', figure=box_plot_fig)
        # Generate job Cards
        ranked_job_results = generate_cards(Job_Ranks, input_embed, 2)
    except:
        embed_res = dbc.Alert(children=['Error when calling the Huggingface API to embed input query. Try again!'], color='danger', class_name='alert-style')

    return embed_res, box_plot, ranked_job_results