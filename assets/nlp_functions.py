import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

# Embed query sentences via API
def embed_api(sentences_):
    """sentences_ should be a list of str; one entry per sentence"""
    # Define Huggingface API parameters
    model_name = 'sentence-transformers/all-mpnet-base-v2'
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
    hf_token = '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'
    headers = {"Authorization": f"Bearer {hf_token}"}
    input_json = {"inputs": sentences_, "options":{"wait_for_model":True}}
    # Call to API
    response = requests.post(api_url, headers=headers, json=input_json)

    return response.json()

# Calculate cosine similarities at sentence level
def calculate_sentences_similarity(df_job_sent_emb, df_query_sent_emb):
    """Requires a job dataframe where each row correspond to a sentence, with embeddings on columns;
    Plust a query df with same structure"""
    job_matrix = np.array(df_job_sent_emb.iloc[:, 2:]) # each row is a job sentence
    query_matrix = np.array(df_query_sent_emb) # each row is a query sentence
    similarity_matrix = cosine_similarity(job_matrix, query_matrix) # job sent on rows; query sent on columns
    # Prepare new dataframe
    similarity_df = df_job_sent_emb.iloc[:, :2]
    for j in range(similarity_matrix.shape[1]):
        similarity_df['sim_query_'+str(j)] = list(similarity_matrix[:, j])
        #print("Query sentence {} - Similarities from {} to {}".format(j, min(list(similarity_matrix[:, j])), max(list(similarity_matrix[:, j]))))
    
    return similarity_df

# Group cosine similarity at job level
def calculate_job_similarity(df_job, df_job_sent_sim, df_query_sent_emb):
    # Initialize empty df
    col_names = ['Job ID', 'Job Title', 'Job URL', 'Main Location', 'Company Name']
    for j in range(len(df_query_sent_emb)):
        col_names.append('Max_sim_query_'+str(j))
        col_names.append('Best_Sentence_sim_query_'+str(j))
    Job_Ranks = pd.DataFrame(columns = col_names)
    # Fill dataframe
    df_job = df_job.loc[df_job['Job ID'].isin(list(df_job_sent_sim['Job ID'])), :] # Filter job info df
    for i, row in df_job.iterrows():
        _data = list(row[:5]) # initialise a new df row
        for j in range(len(df_query_sent_emb)): # append columns for each query sentence
            # Max similarity score
            max_score = max(list(df_job_sent_sim.loc[df_job_sent_sim['Job ID']==row['Job ID'], 'sim_query_'+str(j)]))
            # Sentence with that score
            best_sen = list(df_job_sent_sim.loc[(df_job_sent_sim['Job ID'] == row['Job ID'])&
                                                (df_job_sent_sim['sim_query_'+str(j)] == max_score), 'Sentence'])[0]
            _data.append(max_score)
            _data.append(best_sen)
        Job_Ranks.loc[len(Job_Ranks)] = _data # Attach to df
    
    return Job_Ranks

# Calculate final rankings for each job
def calculate_ranks(Job_Ranks, df_query_sent_emb):
    """The final ranks is a weighted average. The weights will depend on the max similarity found against each query
    sentence."""
    # Calculate weights for each query sentence
    weights_ = []
    for j in range(len(df_query_sent_emb)):
        j_max = max(list(Job_Ranks['Max_sim_query_'+str(j)])) + 1 # sum 1 to force positive values as cos sim [-1,+1]
        weights_.append(j_max)
    weights_ = [w/sum(weights_) for w in weights_]    
    # Create columns with relative rank for each query sentence (using ranks will avoid negative values that are in the cos similarity)
    for j in range(len(df_query_sent_emb)):
        Job_Ranks = Job_Ranks.sort_values(by = 'Max_sim_query_'+str(j), ascending=False, ignore_index=True)
        Job_Ranks['Rank_query_'+str(j)] = list(Job_Ranks.index)
    # Dot product to get final score
    ranks_ = np.array(Job_Ranks.iloc[:, -len(df_query_sent_emb):])
    weights_ = np.array(weights_)
    Job_Ranks['Rank_fin'] = list(ranks_ @ weights_)
    Job_Ranks = Job_Ranks.sort_values(by = 'Rank_fin', ascending=True, ignore_index=True)
    
    return Job_Ranks

# Generate list of dbc.Row, dbc.Col, dbc.Card to be displayed as search results
def generate_cards(Job_Ranks, input_embed, n_per_row):
    """The function creates a row component containing n_per_row columns. Each column contains a dbc.Card with job info"""
    ranked_job_results = []
    for i_row in range(0, len(Job_Ranks), n_per_row):
        new_Cols = []
        j_col = i_row
        while (j_col < len(Job_Ranks)) & (j_col < i_row+n_per_row):
            # Create card body
            card_body_content = ([html.P(["("+str(qs)+") "+
                                          Job_Ranks.loc[j_col, 'Best_Sentence_sim_query_'+str(qs)]],
                                          className='card-body-par') for qs in range(len(input_embed))])
            card_body_content.insert(0, html.H5([str(Job_Ranks.loc[j_col, 'Job Title']), " | ", str(Job_Ranks.loc[j_col, 'Company Name'])]))
            card_body_content.insert(0, html.H6([
                html.I(className="fa fa-location-dot", style={'display':'inline'})," ",
                str(Job_Ranks.loc[j_col, 'Main Location'])]))
            # Create card header
            card_header_content = [
                    html.I(className="fa fa-briefcase", style={'display':'inline'}),
                    html.P(["  #"+str(j_col+1)+" | "], style={'display':'inline'}),
                    html.A("View Job", href = str(Job_Ranks.loc[j_col, 'Job URL']), style={'display':'inline'})
                ]
            # Create card object
            card_ = dbc.Card([
                dbc.CardHeader(card_header_content),
                dbc.CardBody(card_body_content)
            ])
            # Append as new column
            new_Cols.append(dbc.Col(card_, width=int(12/n_per_row)))
            j_col += 1
        # Insert cols into Row
        ranked_job_results.append(dbc.Row(new_Cols))
    
    return ranked_job_results
