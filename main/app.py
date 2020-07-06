#!/bin/python3

import sys
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
from sqlalchemy.exc import ProgrammingError
from dash.dependencies import Input, Output
sys.path.append("..")
from new_database.new_base import WGSqc
from new_database.new_queries import *
from main.get_plots import get_small_boxplot, get_small_scatter, empty_plot


# --------------------------- STYLESHEETS AND APP SETUP ---------------------------
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
external_stylesheets = [dbc.themes.CYBORG, FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig_height = 700
border_color = "#1a1a1a"
background_color = "#000000"
font_color = '#7FDBFF'
components_color = '#080808'
graph_height = '600px'
padding = '10px 10px 10px 10px'
border_radius = 10
margin = 5


navbar = {'marginLeft': margin, 'marginRight': margin, 'marginTop': margin, 'marginBottom': margin,
          'padding': padding,
          'backgroundColor': components_color,
          'border-radius': border_radius,
          'border': f'2px {border_color} solid'
          }

graph = {'marginLeft': margin, 'marginRight': margin, 'marginTop': margin, 'marginBottom': margin,
         'padding': padding,
         'backgroundColor': components_color,
         'height': graph_height,
         'border-radius': border_radius,
         'border': f'2px {border_color} solid'
         }

body_style = {'marginLeft': margin, 'marginRight': margin, 'marginTop': margin, 'marginBottom': margin,
              'backgroundColor': background_color,
              'padding': padding
              }

sidebar_style = {'marginLeft': margin, 'marginRight': margin, 'marginTop': margin, 'marginBottom': margin,
                 'padding': padding,
                 'border-radius': border_radius,
                 'backgroundColor': components_color,
                 'border': f'2px {border_color} solid',
                 'height': '1210px',
                 'width': '160px',
                 'overflowY': 'scroll',
                 }

section_style = {'marginLeft': margin, 'marginRight': margin, 'marginTop': margin, 'marginBottom': margin,
               'padding': padding,
               'border-radius': border_radius,
               'backgroundColor': components_color,
               'border': f'2px {border_color} solid',
                 }


# --------------------------- DATA LOAD ---------------------------
try:
    dropdown_options = get_transcripts_by_gene(WGSqc, type="object")
except ProgrammingError:
    print("Database does not exist")
else:
    # --------------------------- DROPDOWNS SETTINGS ---------------------------
    genes_dropdown = dbc.Col(
                        dcc.Dropdown(
                            id='genes-dropdown',
                            options=[{'label': k, 'value': k} for k in dropdown_options.keys()],
                            value=get_first_row_for_default(WGSqc)
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
    sample_dropdown = dbc.Col(
        dcc.Dropdown(
            id='sample-dropdown',
            options=[{"label": k, "value": k} for k in sorted(get_all_file_names(WGSqc, "sample_id"))],
            value=get_all_file_names(WGSqc, "sample_id")[0]
        )
    )

    navbar = dbc.Navbar(
        [
            dbc.Col(html.H3("WGSqc"), width=1),
            dbc.Col(sample_dropdown, width=5),
            dbc.Col(dbc.Button("Save to .csv", color="primary"), width=2)

        ],
        dark=True,
        color=background_color,
        style=navbar,
        sticky="top"
    )

    # --------------------------- DEFAULT PLOTS ---------------------------
    small_box_plot = dcc.Graph(
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

    # --------------------------- QC SUMMARY SECTION ---------------------------
    table_header = [
        html.Thead(html.Tr([
            html.Th("Measure"),
            html.Th("Value"),
        ]))
    ]

    values_for_summary = [0 for x in range(11)]

    row1 = html.Tr([html.Td("Total reads number"), html.Td(f"{values_for_summary[0]}")])
    row2 = html.Tr([html.Td("Total mapped reads number"), html.Td(f"{values_for_summary[1]}")])
    row3 = html.Tr([html.Td("Percentage of mapped"), html.Td(f"{values_for_summary[2]}")])
    row4 = html.Tr([html.Td("Duplicates number"), html.Td(f"{values_for_summary[3]}")])
    row5 = html.Tr([html.Td("Average depth"), html.Td(f"{values_for_summary[4]}")])
    row6 = html.Tr([html.Td("Percent covered >= 10 reads"), html.Td(f"{values_for_summary[5]}")])
    row7 = html.Tr([html.Td("Percent covered >= 20 reads"), html.Td(f"{values_for_summary[6]}")])
    row8 = html.Tr([html.Td("Percent covered >= 30 reads"), html.Td(f"{values_for_summary[7]}")])
    row9 = html.Tr([html.Td("Total detected variants number"), html.Td(f"{values_for_summary[8]}")])
    row10 = html.Tr([html.Td("Total heterozygous variants number"), html.Td(f"{values_for_summary[9]}")])
    row11 = html.Tr([html.Td("Total heterozygous number on X chromosome"), html.Td(f"{values_for_summary[10]}")])

    table_body = [html.Tbody([row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11])]

    qc_summary_table = dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        style={
            'backgroundColor': components_color,
            'color': font_color
        },
    )

    qc_summary_section = html.Div([
        dbc.Col(html.H3("QC Summary")),
        dbc.Col(html.Div(qc_summary_table))
    ])

    # --------------------------- QC REPORTS SECTION ---------------------------
    qc_reports_section = html.Div([
        dbc.Col(html.H3("QC Reports")),
        dbc.Col(html.Div("a tu będą reporty"))
    ])

    # --------------------------- QC COVERAGE SECTION ---------------------------
    samples = get_list_of_available_samples(WGSqc)

    sample_ids, mean_coverage_values, x10_coverage_values, \
    x20_coverage_values, x30_coverage_values = get_coverages_and_ids(WGSqc, samples)

    genome_mean_coverage = go.Scatter(
        y=mean_coverage_values,
        x=list(range(len(sample_ids))),
        name="Mean coverage percentage across whole genome",
        mode='markers',
        marker=dict(
            color=font_color,
            size=18
        ),
        showlegend=True)

    genome_x10_coverage = go.Scatter(
        y=x10_coverage_values,
        x=list(range(len(sample_ids))),
        name="X10 coverage percentage across whole genome",
        mode='markers',
        marker=dict(
            color="#FCBF1E",
            size=18
        ),
        showlegend=True)

    genome_x20_coverage = go.Scatter(
        y=x20_coverage_values,
        x=list(range(len(sample_ids))),
        name="X20 coverage percentage across whole genome",
        mode='markers',
        marker=dict(
            color="#035AA6",
            size=18
        ),
        showlegend=True)

    genome_x30_coverage = go.Scatter(
        y=x30_coverage_values,
        x=list(range(len(sample_ids))),
        name="X30 coverage percentage across whole genome",
        mode='markers',
        marker=dict(
            color="#6b26a3",
            size=18
        ),
        showlegend=True)

    subplots = [genome_mean_coverage,
                genome_x10_coverage,
                genome_x20_coverage,
                genome_x30_coverage
                ]

    layout = go.Layout(title="Mean coverage of whole genome across samples",
                       height=fig_height,
                       hoverlabel=dict(
                           bgcolor='black',
                           font_size=16,
                           bordercolor=font_color,
                       ),
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       xaxis={'tickvals': [x for x in range(len(sample_ids))],
                              'ticktext': sample_ids
                              },
                       yaxis=dict(range=[0, 100.5]),
                       font={
                           "size": 18,
                           "color": font_color
                       },)

    fig = go.Figure(data=subplots, layout=layout)

    genome_mean_coverage_plot = dcc.Graph(figure=fig)

    qc_coverage_section = html.Div([
        dbc.Row(dbc.Col(html.H3("QC Coverage"))),
        dbc.Row(dbc.Col(html.Div(genome_mean_coverage_plot))),
        dbc.Row([
            dbc.Col(boxplot_dropdown),
            dbc.Col(genes_dropdown),
            dbc.Col(transcripts_dropdown)
        ]),
        dbc.Row([
            dbc.Col(html.Div(small_scatter)),
            dbc.Col(html.Div(small_box_plot))
        ])
    ])

    # --------------------------- QC VARIANTS SECTION ---------------------------
    qc_variants_section = html.Div([
        dbc.Col(html.H3("QC Variants")),
        dbc.Col(html.Div("A tu beda warianty"))
    ])

    # --------------------------- SIDEBAR SETTINGS ---------------------------
    body = html.Div([
        dbc.Row([
            # dbc.Col(html.Div(sidebar), width="25%"),
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div(qc_summary_section, style=section_style)),
                    dbc.Col(html.Div(qc_reports_section, style=section_style))
                ]),
                dbc.Row(
                    dbc.Col(html.Div(qc_coverage_section, style=section_style))
                ),
                dbc.Row(
                    dbc.Col(html.Div(qc_variants_section, style=section_style))
                ),
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
        Output('box-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('boxplot-view-dropdown', 'value')])
    def display_small_box(selected_gene, selected_transcript, view):
        if view == "Mean coverage boxplots":
            return get_small_boxplot(selected_transcript, selected_gene, "mean_coverage")
        elif view == "X10 coverage boxplots":
            return get_small_boxplot(selected_transcript, selected_gene, "percentage_above_10")
        elif view == "X20 coverage boxplots":
            return get_small_boxplot(selected_transcript, selected_gene, "percentage_above_20")
        elif view == "X30 coverage boxplots":
            return get_small_boxplot(selected_transcript, selected_gene, "percentage_above_30")
        else:
            return empty_plot()

    @app.callback(
        Output('small-scatter-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('sample-dropdown', 'value')])
    def display_small_scatter(selected_gene, selected_transcript, selected_sample):
        return get_small_scatter(selected_transcript, selected_gene, selected_sample)


    if __name__ == "__main__":
        app.run_server(debug=True)
