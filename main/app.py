#!/bin/python3

import sys
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
sys.path.append("..")
from database.base import Record
from database.queries import get_transcripts_by_gene
import time


# --------------------------- STYLESHEETS AND APP SETUP ---------------------------
external_stylesheets = [dbc.themes.CYBORG]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# --------------------------- DATA LOAD ---------------------------
dropdown_options = get_transcripts_by_gene(Record, type="object")


# --------------------------- DROPDOWN MENUS SETTINGS ---------------------------
genes_dropdown = dbc.Col(
                    dcc.Dropdown(
                        id='genes-dropdown',
                        options=[{'label': k, 'value': k} for k in dropdown_options.keys()],
                        value='LOC100996442'
                    ))

transcripts_dropdown = dbc.Col(
            dcc.Dropdown(id='transcripts-dropdown')
        )

# --------------------------- NAVBAR SETTINGS ---------------------------
name = dbc.Badge("WGSqc", color="secondary",)
dashboard = dbc.Navbar(
    [
        dbc.Col(dbc.NavbarBrand(html.H3(name)), sm=3, md=2),
        genes_dropdown,
        transcripts_dropdown,
        html.Div(id="display-selected-values")
    ],
    dark=True,
    color="#1a1a1a",
)

# --------------------------- LAYOUT SETTINGS ---------------------------
app.layout = html.Div([dashboard])

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
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('genes-dropdown', 'value'),
     Input('transcripts-dropdown', 'value')])
def set_display_children(selected_gene, selected_transcript):
    return u'{} {}'.format(
        selected_gene, selected_transcript,
    )


if __name__ == "__main__":
    app.run_server()
