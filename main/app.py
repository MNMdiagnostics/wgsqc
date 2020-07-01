#!/bin/python3

import sys
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from sqlalchemy.exc import ProgrammingError
from dash.dependencies import Input, Output
sys.path.append("..")
from new_database.new_base import WGSqc
from new_database.new_queries import *
from main.get_plots import get_boxplot, get_scatterplot, get_small_scatter, empty_plot, get_genome_mean_coverage


# --------------------------- STYLESHEETS AND APP SETUP ---------------------------
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
external_stylesheets = [dbc.themes.CYBORG, FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
    genome_mean_coverage = dcc.Graph(
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
        id="genome-mean-coverage-plot",
        style=graph
    )

    qc_coverage_section = html.Div([
        dbc.Col(html.H3("QC Coverage")),
        dbc.Col(html.Div(genome_mean_coverage))
    ])

    # --------------------------- QC VARIANTS SECTION ---------------------------
    qc_variants_section = html.Div([
        dbc.Col(html.H3("QC Variants")),
        dbc.Col(html.Div("A tu warianty"))
    ])

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
        options=[{'label': k, 'value': k} for k in sorted(get_all_file_names(WGSqc, "sample_id"))],
        id='radio-buttons')

    sidebar = dbc.Jumbotron(
        sidebar_content,
        fluid=False,
        style=sidebar_style)

    body = html.Div([
        dbc.Row([
            dbc.Col(html.Div(sidebar), width="25%"),
            dbc.Col([
                # dbc.Row(
                #     dbc.Col(html.Div(big_scatter))
                # ),
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
                # dbc.Row([
                #     dbc.Col(html.Div(box_plot)),
                #     dbc.Col(html.Div(small_scatter))
                # ])
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
            return get_boxplot(selected_transcript, selected_gene, "mean_coverage")
        elif view == "X10 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "percentage_above_10")
        elif view == "X20 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "percentage_above_20")
        elif view == "X30 coverage boxplots":
            return get_boxplot(selected_transcript, selected_gene, "percentage_above_30")
        else:
            return empty_plot()

    @app.callback(
        Output('small-scatter-plot', 'figure'),
        [Input('genes-dropdown', 'value'),
         Input('transcripts-dropdown', 'value'),
         Input('radio-buttons', 'value')])
    def display_small_scatter(selected_gene, selected_transcript, selected_sample):
        return get_small_scatter(selected_transcript, selected_gene, selected_sample)


    @app.callback(
        Output('genome-mean-coverage-plot', 'figure'),
        [Input('radio-buttons', 'value')])
    def update_coverage_per_genome(selected_sample):
        return get_genome_mean_coverage(WGSqc)


    if __name__ == "__main__":
        app.run_server(debug=True)
