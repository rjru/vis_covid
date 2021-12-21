import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

#df_vis = pd.read_pickle("D:/rjru/Google Drive (rjruos@gmail.com)/dataset/resultado_total_clustering2.pkl")
df_vis = pd.read_pickle("D:/rjru/Google Drive (rjruos@gmail.com)/dataset/clusterfinal4.pkl")
#df_vis = pd.read_pickle("D:/rjru/Google Drive (rjruos@gmail.com)/dataset/clusterfinal4SinDistancia.pkl")

cluster_colors = ["Cluster_Id", "cluster_spec_id", "cluster_gaussian_id", "cluster_hierarchical_complete", "cluster_hierarchical_average", "cluster_hierarchical_average_four", "Cluster_Id_four", "cluster_gaussian_id_four", "cluster_spec_id_four"]             

type_projection = ["PCA", "T-SNE"]

saludo = "NO"

df_vis['fecha_fallecimiento'] = df_vis['fecha_fallecimiento'].astype(str)
df_vis['fecha_dosis1'] = df_vis['fecha_dosis1'].astype(str)
df_vis['fecha_dosis2'] = df_vis['fecha_dosis2'].astype(str)
df_vis['fecha_ingreso_hosp'] = df_vis['fecha_ingreso_hosp'].astype(str)
df_vis['fecha_ingreso_uci'] = df_vis['fecha_ingreso_uci'].astype(str)
df_vis['fecha_ingreso_ucin'] = df_vis['fecha_ingreso_ucin'].astype(str)


pca_res_2d = np.load('D:/rjru/Google Drive (rjruos@gmail.com)/dataset/pca_2d_v2.npy')
tsne_res_2d = np.load('D:/rjru/Google Drive (rjruos@gmail.com)/dataset/tsne_2d_v2.npy')

pca_res_3d = np.load('D:/rjru/Google Drive (rjruos@gmail.com)/dataset/pca_3d_v2.npy')
tsne_res_3d = np.load('D:/rjru/Google Drive (rjruos@gmail.com)/dataset/tsne_3d_v2.npy')


print(saludo)
print("count: ", df_vis['Cluster_Id'].value_counts())



# TIME SERIES
df = px.data.stocks()
# BAR CHAR
dfx = px.data.tips()
days = dfx.day.unique()

token = "pk.eyJ1IjoicmpydSIsImEiOiJja3g5a2sxanQweDJqMm5xaHVoeGpteHM2In0.cMoR4NI3-mcBGCR7i1pXkQ"

dfm = px.data.election()
geojson = px.data.election_geojson()
candidates = dfm.winner.unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

fig = px.scatter_3d(
    pca_res_3d, x= 0, y= 1, z= 2,
    color=df_vis['Cluster_Id'], labels={'color': 'Cluster_Id'}, hover_name=df_vis["fallecido_id_persona"],
    width=800, height=800
)


app.layout = html.Div([
        
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Click Data**
                Click on points in the graph.
            """),
            html.Pre(id='click-data'),
        ], style={'width': '29%', 'display': 'inline-block', 'float': 'left'}),
                         
        html.Div([
            dcc.Dropdown(
                id='paint-cluster',
                options=[{'label': i, 'value': i} for i in cluster_colors],
                value='Cluster_Id'
            ),
            dcc.Dropdown(
                id='type-projection',
                options=[{'label': i, 'value': i} for i in type_projection],
                value='PCA'
            ),
            dcc.Graph(
                id='basic-interactions'
            ),
        ], style={'width': '69%', 'display': 'inline-block', 'float': 'right'} ),
    ]),
    
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Click Data**
                Click on points in the graph.
            """),
            html.Pre(id='click-data2'),
        ], style={'width': '29%', 'display': 'inline-block', 'float': 'left'}),
                         
        html.Div([
            dcc.Dropdown(
                id='paint-cluster2',
                options=[{'label': i, 'value': i} for i in cluster_colors],
                value='Cluster_Id'
            ),
            dcc.Dropdown(
                id='type-projection2',
                options=[{'label': i, 'value': i} for i in type_projection],
                value='PCA'
            ),
            dcc.Graph(
                id='basic-interactions2'
            ),
        ], style={'width': '69%', 'display': 'inline-block', 'float': 'right'} ),
    ]),
                         
    dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x} 
                  for x in df.columns[1:]],
        value=df.columns[1],
        clearable=False,
    ),
    dcc.Graph(id="time-series-chart"),
    
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in days],
        value=days[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-chart"),
    
    html.P("Candidate:"),
    dcc.RadioItems(
        id='candidate', 
        options=[{'value': x, 'label': x} 
                  for x in candidates],
        value=candidates[0],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
])

# https://community.plotly.com/t/duplicate-callback-outputs-solution-api-discussion/55909

@app.callback(
    Output('basic-interactions', 'figure'),
    Input('paint-cluster', 'value'),
    Input('type-projection', 'value'))
    #prevent_initial_call=True)

def update_graph(paint_cluster, type_projection):
    #fig.update_traces(marker=dict(color=df_vis[paint_cluster]))

    type_p = {"PCA":pca_res_3d, "T-SNE":tsne_res_3d}
    #config1 = {'toImageButtonOptions': {'filename': "3d " + type_projection + " " + paint_cluster}}
    saludo = "si"
    fig = px.scatter_3d(
        type_p[type_projection], x=0, y=1, z=2,
        color=df_vis[paint_cluster], labels={'color': 'Cluster_Id'}, hover_name=df_vis["fallecido_id_persona"], width=1000, height=700, title = "3d " + type_projection + " " + paint_cluster + " 4 grupos")
    #print("3d " + type_projection + " " + paint_cluster)
    fig.update_layout(clickmode='event+select')
    fig.update_traces(marker_size=2)
    return fig

@app.callback(
    Output('basic-interactions2', 'figure'),
    Input('paint-cluster2', 'value'),
    Input('type-projection2', 'value'))
    #prevent_initial_call=True)

def update_graph(paint_cluster, type_projection):
    #fig.update_traces(marker=dict(color=df_vis[paint_cluster]))

    type_p = {"PCA":pca_res_2d, "T-SNE":tsne_res_2d}
    fig = px.scatter(type_p[type_projection], x=0, y=1, color = df_vis[paint_cluster], title = "2d " + type_projection + " " + paint_cluster + " 4 grupos")
    #print("2d " + type_projection + " " + paint_cluster)
    fig.update_layout(clickmode='event+select')
    #fig.update_traces(marker_size=2)
    return fig    

@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))

def display_click_data(clickData):
    #res = json.dumps(clickData, indent=2)
    #aqui = clickData
    #print("aquiii: ", aqui)
    res = "Seleccionar"
    if clickData is not None:
        
        res = df_vis[df_vis["fallecido_id_persona"]==clickData["points"][0]["hovertext"]]
        res = res.to_dict(orient='records')
        res = {"result": res}
        res = json.dumps(res, indent=2)
    
    return res 

@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("ticker", "value")])
def display_time_series(ticker):
    fig = px.line(df, x='date', y=ticker)
    return fig

@app.callback(
    Output("bar-chart", "figure"), 
    [Input("dropdown", "value")])
def update_bar_chart(day):
    mask = dfx["day"] == day
    fig = px.bar(dfx[mask], x="sex", y="total_bill", 
                 color="smoker", barmode="group")
    return fig

@app.callback(
    Output("choropleth", "figure"), 
    [Input("candidate", "value")])
def display_choropleth(candidate):
    fig = px.choropleth_mapbox(
        dfm, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        center={"lat": -9.5105, "lon": -75.8604}, zoom=4.5,
        range_color=[0, 6500],
        width=600, height=700
        )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken=token)

    return fig

app.run_server(debug=False)




