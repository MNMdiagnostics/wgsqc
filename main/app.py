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
from main.mean_cov_scatterplot import mean_cov_scatterplot
from main.mean_cov_boxplots import mean_cov_boxplots

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

    transcripts_dropdown = dbc.Col(
                dcc.Dropdown(id='transcripts-dropdown')
            )

    plots_dropdown = dbc.Col(
        dcc.Dropdown(
            id='plots-dropdown',
            options=[
                {"label": "Mean coverage boxplots", "value": "Mean coverage boxplots"},
                {"label": "Mean coverage - coverage X10", "value": "Mean coverage - coverage X10"},
            ],
            value='Mean coverage boxplots'
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
    default_plot = dcc.Graph(
            figure={
                'data': [
                    {'x': [],
                     'y': [],
                     }
                ],
                'layout':{
                    "height": 700,
                    'plot_bgcolor': background_color,
                    'paper_bgcolor': background_color,
                    'font': {
                        'color': font_color
                    }
                }
            },
        id="default-plot",
        style=graph
    )

    # --------------------------- SIDEBAR SETTINGS ---------------------------
    content = [html.Div(sample_id, id=f"{sample_id}-button") for sample_id in sorted(get_all_file_names(Record, "sample_id"))]
    radio = dcc.RadioItems(
        options=[{'label': k, 'value': k} for k in sorted(get_all_file_names(Record, "sample_id"))],
        id='radio-button'
    )
    sidebar = dbc.Jumbotron(
        radio,
        fluid=False,
        style=sidebar_style)

    body = html.Div([
        dbc.Row([
            dbc.Col(html.Div(sidebar), width='25%'),
            dbc.Col(html.Div(default_plot))])],
        style=body_style)

    # --------------------------- LAYOUT SETTINGS ---------------------------
    app.layout = html.Div([navbar, html.Div(id="output-radio"), body])

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
        Output('default-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('plots-dropdown', 'value'),
         Input('radio-button', 'value')])
    def set_display_children(selected_gene, selected_transcript, view_type, selected_sample):

        if view_type == "Mean coverage boxplots":
            return mean_cov_boxplots(selected_transcript, selected_gene, selected_sample)

        elif view_type == "Mean coverage - coverage X10":
            return mean_cov_scatterplot(selected_transcript, selected_gene, selected_sample)

        else:
            return empty_plot(selected_sample)


    if __name__ == "__main__":
        app.run_server(debug=True)

# TODO: Add dropdown/left-side menu to highlight wanted sample.
# TODO: Try to edit style and informations on hoverlabel.
# TODO: Maybe number of samples showed on navbar.
