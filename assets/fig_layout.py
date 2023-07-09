import plotly.graph_objects as go

###### FIG LAYOUT
my_colors = ['rgb(75, 41, 145)',
 'rgb(135, 44, 162)',
 'rgb(192, 54, 157)',
 'rgb(234, 79, 136)',
 'rgb(250, 120, 118)',
 'rgb(246, 169, 122)',
 'rgb(237, 217, 163)'] # Max 10, from px.colors.sequential.Agsunset
    
font_style = {
    'color' : '#f6f6f6'
}

margin_style = {
    'b': 10,
    'l': 50,
    'r': 8,
    't': 50,
    'pad': 0
}

xaxis_style = {
    'linewidth' : 1,
    'linecolor' : 'rgba(0, 0, 0, 0.35%)',
    'showgrid' : False,
    'zeroline' : False
}

yaxis_style = {
    'linewidth' : 1,
    'linecolor' : 'rgba(0, 0, 0, 0.35%)',
    'showgrid' : True,
    'gridwidth' : 1,
    'gridcolor' : 'rgba(0, 0, 0, 0.11%)',
    'zeroline' : False
}

my_figlayout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)', # Figure background is transparend and controll by css on dcc.Graph() components
    plot_bgcolor='rgba(0,0,0,0)',
    font = font_style,
    margin = margin_style,
    xaxis = xaxis_style,
    yaxis = yaxis_style,
    height = 250
)
