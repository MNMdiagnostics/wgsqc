#!/bin/python3
import sys
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
sys.path.append("..")
from database.base import Record
from database.queries import get_transcripts_by_gene, get_stats_for_plot


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
    ],
    dark=True,
    color="#1a1a1a",
)


# --------------------------- DEFAULT BOXPLOT ---------------------------
default_boxplots = go.Box(y=[])
data = [default_boxplots]
layout = go.Layout(title = "Mean coverage box plot")
fig = go.Figure(data=data, layout=layout)
boxplots = dcc.Graph(figure=fig, id='box-plot')

# --------------------------- LAYOUT SETTINGS ---------------------------
app.layout = html.Div([dashboard, boxplots, html.Div(id="display-selected-values")])

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
    Output('box-plot', 'figure'),
    [Input('genes-dropdown', 'value'),
     Input('transcripts-dropdown', 'value')])
def set_display_children(selected_gene, selected_transcript):
    mean_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov")
    x10_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10")
    x20_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_20")
    x30_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_30")

    mean_cov_boxplot = go.Box(
        y=mean_cov_data,
        name="Mean coverage",
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff'),
        line=dict(
            color='#7fdbff'))

    x10 = go.Box(
        y=x10_cov_data,
        name="Coverage X10",
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff'),
        line=dict(
            color='#7fdbff'))

    x20 = go.Box(
        y=x20_cov_data,
        name="Coverage X20",
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff'),
        line=dict(
            color='#7fdbff'))

    x30 = go.Box(
        y=x30_cov_data,
        name="Coverage X30",
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff'),
        line=dict(
            color='#7fdbff'))

    data = [mean_cov_boxplot, x10, x20, x30]

    layout = go.Layout(title = "Coverage boxplots",
                       height=800,
                       paper_bgcolor='#010608',
                       plot_bgcolor='#010608',
                       font = {
                           "size": 18,
                           "color": '#7fdbff'
                       }

                       )
    fig = go.Figure(data=data, layout=layout)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
