# import dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
import plotly.graph_objects as go
import random
from datetime import date


# create dash
app = dash.Dash(
    name='Youtube',
    external_stylesheets =[dbc.themes.SUPERHERO]
)
app.title = 'Top 50 Youtube Channel Trending'

# create navbar
navbar = dbc.NavbarSimple(
    brand = 'Top 50 Youtube Channel Trending',
    color= 'dark',
    dark=True,
    sticky='top'
)

# load dataset
yt = pd.read_csv('trending.csv')
top50 = yt['channel_name'].value_counts().head(50).index.to_list()
yt = yt[yt['channel_name'].isin(top50)]

# clean dataset

yt.loc[:,'publish_time'] = pd.to_datetime(yt.publish_time.str.replace('Z','').str.replace('T',' '))
yt.loc[:,'trending_time'] = pd.to_datetime(yt.trending_time.str.replace('.            ',''))

yt['trending_daterange'] = yt['trending_time'].dt.to_period('D')
yt['publish_daterange'] = yt['publish_time'].dt.to_period('D')


yt['publish_year'] = yt['publish_time'].dt.year
yt['publish_month'] = yt['publish_time'].dt.month
yt['publish_month_name'] = yt['publish_time'].dt.month_name()
yt['publish_day'] = yt['publish_time'].dt.day
yt['publish_day_name'] = yt['publish_time'].dt.day_name()
yt['trending_year'] = yt['trending_time'].dt.year
yt['trending_month'] = yt['trending_time'].dt.month
yt['trending_month_name'] = yt['trending_time'].dt.month_name()
yt['trending_day'] = yt['trending_time'].dt.day
yt['trending_day_name'] = yt['trending_time'].dt.day_name()

yt = yt.dropna(axis=0)

# visualization plot 1
plot1_scatter = px.scatter(
    yt,
    x="like",
    y="dislike", 
    animation_group="channel_name",
    color="trending_day_name",
    size="view",
    size_max=50,
    hover_name="channel_name",
    log_x=True,
    color_discrete_sequence = px.colors.qualitative.Pastel,
    labels = {
        'trending_day_name' : 'Day of Trending :',
        'publish_day_name' : 'Day of Publish',
        'like' : 'Sum of Like',
        'dislike' : 'Sum of Dislike'
    }
)

# visualization plot 2
plot2_bar = px.bar(
    yt,
    x="trending_month_name",
    y="view",
    color="trending_day_name",
    color_discrete_sequence = px.colors.qualitative.Pastel,
    labels = {
        'trending_day_name':'Day of Trending',
        'trending_month_name' : 'Month of Trending',
        'view' : 'Sum of Views',
        'publish_day_name' : 'Day of Publish'
    }
)

# visualization plot 3
plot3_box = px.box(
    yt,
    color='trending_day_name',
    x='trending_day_name',
    y='view',
    title='Distribution of Views in each Youtube Channel Trending',
    color_discrete_sequence = px.colors.qualitative.Pastel,
    labels={
        'trending_day_name': 'Day of Trending :',
        'view': 'Sum of Views' 
    }
).update_xaxes(visible=False)

# visualization plot4
yt_corr = yt[['like','dislike','view','comment']].corr()
plot4_corr = go.Figure().add_trace(
                go.Heatmap(
                x = yt_corr.columns,
                y = yt_corr.index,
                z = np.array(yt_corr),
                text=yt_corr.values,
                texttemplate='%{text:.2f}',
                colorscale='Blues'
    )
)

plot4_corr.update_layout(
    title={
        'text' : f'Correlation of Numeric Value in each Youtube Channel'
    }
)

# visualization plot5
plot5_line = px.line(
    yt,
    x ='trending_time',
    y = 'view',
    title = 'Trend of Views in Youtube Channel',
    labels={
        'view' : 'Sum of Views',
        'trending_time' : 'Date of Trending'
    }
)

# default date
default_min_date = date(yt['publish_daterange'].min().year,
                        yt['publish_daterange'].min().month,
                        yt['publish_daterange'].min().day)
default_max_date = date(yt['trending_daterange'].max().year,
                        yt['trending_daterange'].max().month,
                        yt['trending_daterange'].max().day)

# dashboard layout
app.layout =  html.Div([
    navbar,

    html.Div([
        dbc.Row([
            dbc.Col([
                html.Br(),
                dcc.Graph(
                    id = 'lineplot',
                    figure = plot5_line
                )
            ],
                width = 8,
                style = {
                    'backgroundColor':'white',
                },            
            ),
            dbc.Col([
                html.Br(),
                dbc.Card([
                    dbc.CardHeader('Select Channel Name'),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id = 'select_channel_name',
                            options = yt['channel_name'].unique(),
                            value='Nihongo Mantappu',
                            style = {"color":"black"}
                        ),
                    ]),
                ]),
                html.Br(),
                dbc.Card([
                    dbc.CardHeader('Select Date Range'),
                    dbc.CardBody([
                        dcc.DatePickerRange(
                            id = 'date_range',
                            min_date_allowed = default_min_date,
                            max_date_allowed = default_max_date,
                            start_date = default_min_date,
                            end_date = default_max_date,
                            start_date_placeholder_text='Start Date',
                            end_date_placeholder_text='End Date',
                        ),
                    ]),
                ]),
            ],
                width = 4,
                style = {
                    'backgroundColor':'white',
                },      
            ),
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                dcc.Graph(
                    id = 'barplot',
                    figure = plot2_bar
                )
            ],
                width = 7,
                style = {
                    'backgroundColor':'white',
                },            
            ),
            dbc.Col([
                html.Br(),
                dcc.Graph(
                    id = 'boxplot',
                    figure = plot3_box
                )
            ],
                width = 5,
                style = {
                    'backgroundColor':'white',
                },            
            ),
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                dcc.Graph(
                    id = 'scatterplot',
                    figure = plot1_scatter
                )
            ],
                width = 7,
                style = {
                    'backgroundColor':'white',
                },            
            ),
            dbc.Col([
                html.Br(),
                dcc.Graph(
                    id = 'corrplot',
                    figure = plot4_corr
                )
            ],
                width = 5,
                style = {
                    'backgroundColor':'white',
                },            
            ),
        ]),
        html.Br(),html.Br(),
        dbc.Row([
            html.P(['Copyright 2022'], style={'textAlign':'center', 'color':'#87bdd8'})
        ]),
    ],
        style = {
        'backgroundColor':'#daebe8',
        'paddingRight':'30px',
        'paddingLeft':'30px',
        'paddingBottom':'30px',
        'paddingTop':'30px',
        
    }),
])


# callback all plot
@app.callback(
    Output(component_id='scatterplot', component_property='figure'),
    Input(component_id='select_channel_name',component_property='value'),
    Input(component_id='date_range',component_property='start_date'),
    Input(component_id='date_range',component_property='end_date'),
)

def update_plot1(channelname, start_date, end_date):
    yt_plot1 = yt[yt['channel_name']==channelname]
    yt_plot1 = yt_plot1[yt_plot1['publish_daterange']>=start_date]
    yt_plot1 = yt_plot1[yt_plot1['trending_daterange']<=end_date]

    #plot1
    plot1_scatter = px.scatter(
        yt_plot1,
        x="like",
        y="dislike",
        animation_group="channel_name",
        color="trending_day_name",
        size="view",
        size_max=50,
        hover_name="channel_name",
        log_x=True,
        color_discrete_sequence = px.colors.qualitative.Pastel,
        labels = {
            'trending_day_name' : 'Day of Trending :',
            'publish_day_name' : 'Day of Publish',
            'like' : 'Sum of Like',
            'dislike' : 'Sum of Dislike'
            },
        title=f'Comparison of Number Likes and Dislikes {str(channelname)} Youtube Channel'
        )

    return plot1_scatter

@app.callback(
    Output(component_id='barplot', component_property='figure'),
    Input(component_id='select_channel_name',component_property='value'),
    Input(component_id='date_range',component_property='start_date'),
    Input(component_id='date_range',component_property='end_date'),
)
def update_plot2(channelname, start_date, end_date):
    yt_plot2 = yt[yt['channel_name']==channelname]
    yt_plot2 = yt_plot2[yt_plot2['publish_daterange']>=start_date]
    yt_plot2 = yt_plot2[yt_plot2['trending_daterange']<=end_date]

    #plot2
    plot2_bar = px.bar(
        yt_plot2,
        x="trending_month_name",
        y="view",
        color="trending_day_name",
        color_discrete_sequence = px.colors.qualitative.Pastel,
        labels = {
            'trending_day_name':'Day of Trending',
            'trending_month_name' : 'Month of Trending',
            'view' : 'Sum of Views',
            'publish_day_name' : 'Day of Publish'
            },
        title=f'Total of Viewers in {str(channelname)} Youtube Channel'
        )

    return plot2_bar

@app.callback(
    Output(component_id='boxplot', component_property='figure'),
    Input(component_id='select_channel_name',component_property='value'),
    Input(component_id='date_range',component_property='start_date'),
    Input(component_id='date_range',component_property='end_date'),
)

def update_plot3(channelname, start_date, end_date):
    yt_plot3 = yt[yt['channel_name']==channelname]
    yt_plot3 = yt_plot3[yt_plot3['publish_daterange']>=start_date]
    yt_plot3 = yt_plot3[yt_plot3['trending_daterange']<=end_date]
    
    #plot3
    plot3_box = px.box(
        yt_plot3,
        color='trending_day_name',
        x='trending_day_name',
        y='view',
        title=f'Distribution of Views in {str(channelname)} Youtube Channel',
        color_discrete_sequence = px.colors.qualitative.Pastel,
        labels={
            'trending_day_name': 'Day of Trending :',
            'view': 'Sum of Views' 
            },
        ).update_xaxes(visible=False)

    return plot3_box

@app.callback(
    Output(component_id='corrplot', component_property='figure'),
    Input(component_id='select_channel_name',component_property='value'),
    Input(component_id='date_range',component_property='start_date'),
    Input(component_id='date_range',component_property='end_date'),
)

def update_plot4(channelname, start_date, end_date):
    yt_plot4 = yt[yt['channel_name']==channelname]
    yt_plot4 = yt_plot4[yt_plot4['publish_daterange']>=start_date]
    yt_plot4 = yt_plot4[yt_plot4['trending_daterange']<=end_date]

    yt_corr = yt_plot4[['like','dislike','view','comment']].corr()
    plot4_corr = go.Figure().add_trace(
                go.Heatmap(
                x = yt_corr.columns,
                y = yt_corr.index,
                z = np.array(yt_corr),
                text=yt_corr.values,
                texttemplate='%{text:.2f}',
                colorscale='Blues'
                )
    )
    plot4_corr.update_layout(
        title={
            'text' : f'Correlation of Numeric Value {str(channelname)} Youtube Channel'
        }
    )
    return plot4_corr

@app.callback(
    Output(component_id='lineplot', component_property='figure'),
    Input(component_id='select_channel_name',component_property='value'),
    Input(component_id='date_range',component_property='start_date'),
    Input(component_id='date_range',component_property='end_date'),
)

def update_plot5(channelname,start_date,end_date):
    yt_plot5 = yt[yt['channel_name']==channelname]
    yt_plot5 = yt_plot5[yt_plot5['publish_daterange']>=start_date]
    yt_plot5 = yt_plot5[yt_plot5['trending_daterange']<=end_date]

    #plot5
    plot5_line = px.line(
    yt_plot5,
    x ='trending_time',
    y = 'view',
    title = f'Trend of Views in {str(channelname)} Youtube Channel',
    labels={
        'view' : 'Sum of Views',
        'trending_time': 'Date of Trending'
        }
    )
    return plot5_line


#start the dash server
if __name__ == "__main__":
    app.run_server()
