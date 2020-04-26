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

plots_dropdown = dbc.Col(
    dcc.Dropdown(
        id='plots-dropdown',
        options=[
            {"label": "Mean coverage boxplots", "value": "Mean coverage boxplots"},
            {"label": "Mean coverage - coverage X10", "value": "Mean coverage - coverage X10"},
        ],
        value='Mean coverage - coverage X10'
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
default_plot = dcc.Graph(id="default-plot")

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
    return available_options[0]['value']


@app.callback(
    Output('default-plot', 'figure'),
    [Input('genes-dropdown', 'value'),
     Input('transcripts-dropdown', 'value'),
     Input('plots-dropdown', 'value')])
def set_display_children(selected_gene, selected_transcript, view_type):
    if view_type == "Mean coverage boxplots":
        # --------------------------- BOXPLOTS ---------------------------
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
    elif view_type == "Mean coverage - coverage X10":
        mean_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov")
        x10_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10")
        scat = go.Scatter(
            x = x10_cov_data,
            y = mean_cov_data,
            mode = "markers",
            name = "Mean coverage against coverage X10",
            marker=dict(
                color='#7fdbff'),
            line=dict(
                color='#7fdbff',
                width=60))
        data = [scat]
        layout = go.Layout(title="Mean coverage against coverage X10",
                           height=800,
                           paper_bgcolor='#010608',
                           plot_bgcolor='#010608',
                           font={
                               "size": 18,
                               "color": '#7fdbff'
                           }

                           )
        fig = go.Figure(data=data, layout=layout)
        return fig



if __name__ == "__main__":
    app.run_server(debug=True)


# TODO: xlab and ylab description, dot size, net width
# TODO: Style default loading empty plot.
# TODO: Default first transcript in database. Now transcript is hardcoded.
# TODO: Maybe dropdown colors?