from dash import html
import dash_bootstrap_components as dbc
import dash

_nav_dropdown = dbc.DropdownMenu(
    children = [dbc.DropdownMenuItem(page["name"], href=page["path"]) for page in dash.page_registry.values()],
    menu_variant="dark", nav=True, align_end=False, size="sm", label="Menu"
    )

_nav = dbc.Container([
	dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([html.I(className="fa-brands fa-angellist fa-3x")], width = 2),
        dbc.Col([], width = 6),
        dbc.Col([_nav_dropdown], width = 3)
        #dbc.Col([html.I(_nav_dropdown, className="fa fa-bars")], width = 3)        
    ], className="nav-row")
])