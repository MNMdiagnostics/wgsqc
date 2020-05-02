#!/bin/python3

import sys
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from sqlalchemy.exc import ProgrammingError
from dash.dependencies import Input, Output
sys.path.append("..")
from database.base import Record
from database.queries import *
from main.empty_plot import empty_plot
from main.mean_cov_scatterplot import mean_cov_scatterplot
from main.mean_cov_boxplots import mean_cov_boxplots

# --------------------------- STYLESHEETS AND APP SETUP ---------------------------
external_stylesheets = [dbc.themes.CYBORG]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# --------------------------- DATA LOAD ---------------------------
try:
    dropdown_options = get_transcripts_by_gene(Record, type="object")
except ProgrammingError:
    print("Database do not exists")
else:
    # --------------------------- DROPDOWN MENUS SETTINGS ---------------------------
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
    name = dbc.Badge("WGSqc", color="secondary",)
    dashboard = dbc.Navbar(
        [
            dbc.Col(dbc.NavbarBrand(html.H3(name)), sm=3, md=2),
            plots_dropdown,
            genes_dropdown,
            transcripts_dropdown,
        ],
        dark=True,
        color="#1a1a1a",
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
                    'plot_bgcolor': '#010608',
                    'paper_bgcolor': '#010608',
                    'font': {
                        'color': '#7FDBFF'
                    }
                }
            },
        id="default-plot"
    )

    # --------------------------- LAYOUT SETTINGS ---------------------------
    app.layout = html.Div([dashboard, default_plot])

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
         Input('plots-dropdown', 'value')])
    def set_display_children(selected_gene, selected_transcript, view_type):

        if view_type == "Mean coverage boxplots":
            return mean_cov_boxplots(selected_transcript, selected_gene)

        elif view_type == "Mean coverage - coverage X10":
            return mean_cov_scatterplot(selected_transcript, selected_gene)

        else:
            return empty_plot()


    if __name__ == "__main__":
        app.run_server(debug=True)

# TODO: Add dropdown/left-side menu to highlight wanted sample.
# TODO: Try to edit style and informations on hoverlabel.
# TODO: Maybe number of samples showed on navbar.
