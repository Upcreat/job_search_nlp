from dash import Dash, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

_font = "https://fonts.googleapis.com/css2?family=Lato&display=swap"
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, _font],
	   suppress_callback_exceptions=True, prevent_initial_callbacks=True)
server = app.server

############################################################################################
# Import shared components
from assets.search_nav import _search_nav

############################################################################################
# App Layout
app.layout = dbc.Container([
	dbc.Row([
        dbc.Col([
		    dbc.Row([_search_nav])
        ], className = 'search-nav-col', width = 4),
        dbc.Col([
            dbc.Row([dash.page_container])
	    ], className = 'page-content', width = 8),
    ]),
    dcc.Store(id='browser-memo', data=dict(), storage_type='session')
], fluid=True)

############################################################################################
# Save Search Imput into Store
@callback(Output('browser-memo', 'data'),
          Input('search-button', 'n_clicks'),
          Input('search-input', 'value'),
          Input('loc-dropdown', 'value'),
          State('browser-memo', 'data'))
def store_input(n_clicks, input_query, input_loc, store_data):
    if n_clicks is None or len(str(input_query))==0:
        raise PreventUpdate
    #Initialize
    if 'search_clicks' in store_data.keys():
         curr_clicks = store_data['search_clicks']
    else:
         curr_clicks = 0
    #Update
    if int(n_clicks) != int(curr_clicks):
         store_data['search_clicks'] = n_clicks
         store_data['search_query'] = str(input_query)
         store_data['input_loc'] = input_loc
    else:
         raise PreventUpdate
    #print(store_data)
    return store_data

############################################################################################
# Run App
if __name__ == '__main__':
	app.run_server(debug=False)