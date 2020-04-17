#!/bin/python3

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

external_stylesheets = [dbc.themes.CYBORG]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dropdown_options = {
    "LOC100996442": ["XR_001737583.2", "XR_002958519.1", "XR_001737579.2"],
    "OR4F16": ["NM_001005277.1", "XM_024449993.1", "XM_024449987.1"],
    "LOC112268260": ["XR_002958507.1", "XR_002958506.1", "XR_002958503.1"],
}

name = dbc.Badge("WGSqc", color="secondary",)

genes_dropdown = dbc.Col(
                    dcc.Dropdown(
                        id='genes-dropdown',
                        options=[{'label': k, 'value': k} for k in dropdown_options.keys()],
                        value='LOC100996442'
                    ))

transcripts_dropdown = dbc.Col(
            dcc.Dropdown(id='transcripts-dropdown')
        )

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

# LAYOUT
app.layout = html.Div([dashboard])


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
    return u'{}{}'.format(
        selected_gene, selected_transcript,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
