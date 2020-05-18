#!/bin/python3

import sys
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from sqlalchemy.exc import ProgrammingError
from dash.dependencies import Input, Output, State
sys.path.append("..")
from database.base import Record
from database.queries import *
from main.get_plots import get_boxplot, get_scatterplot, get_small_scatter, empty_plot

# --------------------------- STYLESHEETS AND APP SETUP ---------------------------
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
external_stylesheets = [dbc.themes.CYBORG, FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

border_color = "#1a1a1a"
background_color = "#000000"
font_color = '#7FDBFF'
components_color = '#080808'
graph_height = '600px'


navbar = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
          'padding': '10px 10px 10px 10px',
          'backgroundColor': components_color,
          'border': f'2px {border_color} solid',
          'border-radius': 10}

graph = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
         'padding': '10px 10px 10px 10px',
         'backgroundColor': components_color,
         'height': graph_height,
         'border': f'2px {border_color} solid',
         'border-radius': 10}

body_style = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
              'backgroundColor': background_color,
              'padding': '10px 10px 10px 10px'}

sidebar_style = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
                 'padding': '10px 10px 10px 10px',
                 'border': f'2px {border_color} solid',
                 'backgroundColor': components_color,
                 'height': '1210px',
                 'width': '160px',
                 'overflowY': 'scroll',
                 'border-radius': 10}


# --------------------------- DATA LOAD ---------------------------
try:
    dropdown_options = get_transcripts_by_gene(Record, type="object")
except ProgrammingError:
    print("Database do not exists")
else:
    # --------------------------- DROPDOWNS SETTINGS ---------------------------
    genes_dropdown = dbc.Col(
                        dcc.Dropdown(
                            id='genes-dropdown',
                            options=[{'label': k, 'value': k} for k in dropdown_options.keys()],
                            value=get_first_row_for_default(Record)
                        ))

    transcripts_dropdown = dbc.Col(dcc.Dropdown(id='transcripts-dropdown'))

    boxplot_dropdown = dbc.Col(
        dcc.Dropdown(
            id='boxplot-view-dropdown',
            options=[
                {"label": "Mean coverage boxplots", "value": "Mean coverage boxplots"},
                {"label": "X10 coverage boxplots", "value": "X10 coverage boxplots"},
                {"label": "X20 coverage boxplots", "value": "X20 coverage boxplots"},
                {"label": "X30 coverage boxplots", "value": "X30 coverage boxplots"},
            ],
            value='Mean coverage boxplots'
        )
    )

    # --------------------------- NAVBAR SETTINGS ---------------------------
    navbar = dbc.Navbar(
        [
            html.H3("WGSqc"),
            boxplot_dropdown,
            genes_dropdown,
            transcripts_dropdown,
        ],
        dark=True,
        color=background_color,
        style=navbar
    )

    # --------------------------- DEFAULT PLOT ---------------------------
    big_scatter = dcc.Graph(
            figure={
                'data': [
                    {'y': []}
                ],
                'layout':{
                    "height": graph_height,
                    'plot_bgcolor': background_color,
                    'paper_bgcolor': background_color,
                    'font': {
                        'color': font_color
                    }
                }
            },
        id="big-scatter-plot",
        style=graph
    )

    box_plot = dcc.Graph(
        figure={
            'data': [
                {'x': [],
                 'y': [],
                 }
            ],
            'layout': {
                "height": graph_height,
                'plot_bgcolor': background_color,
                'paper_bgcolor': background_color,
                'font': {
                    'color': font_color
                }
            }
        },
        id="box-plot",
        style=graph
    )

    small_scatter = dcc.Graph(
        figure={
            'data': [
                {'x': [],
                 'y': [],
                 }
            ],
            'layout': {
                "height": graph_height,
                'plot_bgcolor': background_color,
                'paper_bgcolor': background_color,
                'font': {
                    'color': font_color
                }
            }
        },
        id="small-scatter-plot",
        style=graph
    )

    # --------------------------- SIDEBAR SETTINGS ---------------------------
    sidebar_content = dcc.RadioItems(
        options=[{'label': k, 'value': k} for k in sorted(get_all_file_names(Record, "sample_id"))],
        id='radio-buttons')

    sidebar = dbc.Jumbotron(
        sidebar_content,
        fluid=False,
        style=sidebar_style)

    body = html.Div([
        dbc.Row([
            dbc.Col(html.Div(sidebar), width="25%"),
            dbc.Col([
                dbc.Row(
                    dbc.Col(html.Div(big_scatter))
                ),
                dbc.Row([
                    dbc.Col(html.Div(box_plot)),
                    dbc.Col(html.Div(small_scatter))
                ])
            ])
        ])
    ],
        style=body_style)

    # --------------------------- LAYOUT SETTINGS ---------------------------
    app.layout = html.Div([navbar, body])

    # --------------------------- DROPDOWNS CALLBACKS ---------------------------

    @app.callback(
        Output('transcripts-dropdown', 'options'),
        [Input('genes-dropdown', 'value')])
    def set_transcript_options(selected_gene):
        return [{'label': i, 'value': i} for i in dropdown_options[selected_gene]]

    @app.callback(
        Output('transcripts-dropdown', 'value'),
        [Input('transcripts-dropdown', 'options')])
    def set_gene_value(available_options):
        try:
            return available_options[0]['value']
        except IndexError:
            return []

    @app.callback(
        Output('big-scatter-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('radio-buttons', 'value')])
    def display_big_scatter(selected_gene, selected_transcript, selected_sample):
        return get_scatterplot(selected_transcript, selected_gene, selected_sample)

    @app.callback(
        Output('box-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('boxplot-view-dropdown', 'value')])
    def display_box(selected_gene, selected_transcript, view):
        if view == "Mean coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "mean_cov")
        elif view == "X10 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "cov_10")
        elif view == "X20 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "cov_20")
        elif view == "X30 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "cov_30")
        else:
            return empty_plot()

    @app.callback(
        Output('small-scatter-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('radio-buttons', 'value')])
    def display_small_scatter(selected_gene, selected_transcript, selected_sample):
        return get_small_scatter(selected_transcript, selected_gene, selected_sample)

    if __name__ == "__main__":
        app.run_server(debug=False)

# TODO: Fix boxplots range to 100.
# TODO: Maybe number of samples showed on navbar.
# TODO: Debug to false.
