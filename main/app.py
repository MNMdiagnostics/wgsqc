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
from main.empty_plot import empty_plot
from main.get_plots import get_boxplot, get_scatterplot, coverage_x10_scatterplot

# --------------------------- STYLESHEETS AND APP SETUP ---------------------------
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
external_stylesheets = [dbc.themes.CYBORG, FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

border_color = "#1a1a1a"
background_color = "#000000"
font_color = '#7FDBFF'
components_color = '#080808'


navbar = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
          'padding': '10px 10px 10px 10px',
          'backgroundColor': components_color,
          'border': f'2px {border_color} solid',
          'border-radius': 10}

graph = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
         'padding': '10px 10px 10px 10px',
         'backgroundColor': components_color,
         'height': '800px',
         'border': f'2px {border_color} solid',
         'border-radius': 10}

body_style = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
              'backgroundColor': background_color,
              'padding': '10px 10px 10px 10px'}

sidebar_style = {'marginLeft': 5, 'marginRight': 5, 'marginTop': 5, 'marginBottom': 5,
                 'padding': '10px 10px 10px 10px',
                 'border': f'2px {border_color} solid',
                 'backgroundColor': components_color,
                 'height': '800px',
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

    plots_dropdown = dbc.Col(
        dcc.Dropdown(
            id='plots-dropdown',
            options=[
                {"label": "Mean coverage boxplots", "value": "Mean coverage boxplots"},
                {"label": "X10 coverage boxplots", "value": "X10 coverage boxplots"},
                {"label": "X20 coverage boxplots", "value": "X20 coverage boxplots"},
                {"label": "X30 coverage boxplots", "value": "X30 coverage boxplots"},
            ],
            value='X10 coverage boxplots'
        )
    )

    # --------------------------- NAVBAR SETTINGS ---------------------------
    navbar = dbc.Navbar(
        [
            html.H3("WGSqc"),
            plots_dropdown,
            genes_dropdown,
            transcripts_dropdown,
        ],
        dark=True,
        color=background_color,
        style=navbar
    )

    # --------------------------- DEFAULT PLOT ---------------------------
    first_plot = dcc.Graph(
            figure={
                'data': [
                    {'y': []}
                ],
                'layout':{
                    "height": 800,
                    'plot_bgcolor': background_color,
                    'paper_bgcolor': background_color,
                    'font': {
                        'color': font_color
                    }
                }
            },
        id="first-plot",
        style=graph
    )

    second_plot = dcc.Graph(
        figure={
            'data': [
                {'x': [],
                 'y': [],
                 }
            ],
            'layout': {
                "height": 800,
                'plot_bgcolor': background_color,
                'paper_bgcolor': background_color,
                'font': {
                    'color': font_color
                }
            }
        },
        id="second-plot",
        style=graph
    )

    third_plot = dcc.Graph(
        figure={
            'data': [
                {'x': [],
                 'y': [],
                 }
            ],
            'layout': {
                "height": 800,
                'plot_bgcolor': background_color,
                'paper_bgcolor': background_color,
                'font': {
                    'color': font_color
                }
            }
        },
        id="third-plot",
        style=graph
    )

    # --------------------------- SIDEBAR SETTINGS ---------------------------
    sidebar_content = dcc.RadioItems(
        options=[{'label': k, 'value': k} for k in sorted(get_all_file_names(Record, "sample_id"))],
        id='radio-button')

    sidebar = dbc.Jumbotron(
        sidebar_content,
        fluid=False,
        style=sidebar_style)

    body = html.Div([
        dbc.Row([
            dbc.Col(html.Div(sidebar), width='25%'),
            dbc.Col(html.Div(first_plot)),
            dbc.Col(html.Div(second_plot)),
            dbc.Col(html.Div(third_plot)),
        ])
    ],
        style=body_style)

    # --------------------------- LAYOUT SETTINGS ---------------------------
    app.layout = html.Div([navbar, body])

    # -----------------------------------------------------------------------
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
        Output('first-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('radio-button', 'value'),
         Input('plots-dropdown', 'value')])
    def display_scatter(selected_gene, selected_transcript, selected_sample, view):
        if view == "Mean coverage boxplots":
            return get_scatterplot(selected_transcript, selected_gene, selected_sample, "mean_cov")
        elif view == "X10 coverage boxplots":
            return get_scatterplot(selected_transcript, selected_gene, selected_sample, "cov_10")
        elif view == "X20 coverage boxplots":
            return get_scatterplot(selected_transcript, selected_gene, selected_sample, "cov_20")
        elif view == "X30 coverage boxplots":
            return get_scatterplot(selected_transcript, selected_gene, selected_sample, "cov_30")

    @app.callback(
        Output('second-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('plots-dropdown', 'value')])
    def display_box(selected_gene, selected_transcript, view):
        if view == "Mean coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "mean_cov")
        elif view == "X10 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "cov_10")
        elif view == "X20 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "cov_20")
        elif view == "X30 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "cov_30")


    @app.callback(
        Output('third-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('radio-button', 'value')])
    def display_second_scatter(selected_gene, selected_transcript, selected_sample):
        return coverage_x10_scatterplot(selected_transcript, selected_gene, selected_sample)


    if __name__ == "__main__":
        app.run_server(debug=True)

# TODO: Add dropdown/left-side menu to highlight wanted sample.
# TODO: Try to edit style and informations on hoverlabel.
# TODO: Maybe number of samples showed on navbar.
