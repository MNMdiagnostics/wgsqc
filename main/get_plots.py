import plotly.graph_objects as go
from database.queries import get_stats_for_plot, get_stats_for_one_sample
from database.base import Record
import numpy as np


components_color = '#080808'
font_color = '#7FDBFF'


def get_boxplot(selected_transcript, selected_gene, statistics):
    """
    Graph object updating handler for coverage boxplot.

    :param selected_transcript: Transcript selected in dropdown.
    :param selected_gene: Gene selected in dropdown.
    :param statistics: Statistics to plot. One from following: "mean_cov", "cov_10", "cov_20", "cov_30".
    :return: Figure object to update graph.
    """

    # GET PANDAS DATAFRAME OF CHOSEN STATISTICS VALUES FOR MATCHING GENE AND TRANSCRIPT
    stat_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, statistics,
                                                            sample_ids=True)
    boxplot = go.Box(
        y=stat_dataframe['value'],
        name=f"{statistics}",
        boxpoints=False,
        text=stat_dataframe['id'],
        marker=dict(
            color=font_color,
        ),
        showlegend=False)

    data = [boxplot]

    layout = go.Layout(title=f"{statistics} boxplot",
                       height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       font={
                           "size": 18,
                           "color": font_color
                       })
    fig = go.Figure(data=data, layout=layout)
    return fig


def get_scatterplot(selected_transcript, selected_gene, selected_sample, statistics):
    """
    Graph object updating handler for coverage scatterlot.

    :param selected_transcript: Transcript selected in dropdown.
    :param selected_gene: Gene selected in dropdown.
    :param selected_sample: Sample to highlight selected in radiobox.
    :param statistics: Statistics to plot. One from following: "mean_cov", "cov_10", "cov_20", "cov_30".
    :return: Figure object to update graph.
    """

    # GET PANDAS DATAFRAME OF CHOSEN STATISTICS VALUES FOR MATCHING GENE AND TRANSCRIPT
    stat_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, statistics,
                                                            sample_ids=True)
    # GET VALUE OF SAMPLE TO HIGHLIGHT
    statistics_value = get_stats_for_one_sample(Record, selected_sample, selected_transcript, selected_gene, statistics)

    scatter = go.Scatter(
        y=stat_dataframe['value'],
        x=[1 for x in range(len(stat_dataframe['value']))],
        name=f"{statistics}",
        mode='markers',
        text=stat_dataframe['id'],
        marker=dict(
            color=np.where(stat_dataframe['value'] == statistics_value, 'red', font_color),
            size=np.where(stat_dataframe['value'] == statistics_value, 18, 12)
        ),
        showlegend=False)

    data = [scatter]

    layout = go.Layout(title=f"{statistics} scatterplot",
                       height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       xaxis={'title': '',
                              'showgrid': False,
                              'ticks': '',
                              'showticklabels': False},
                       font={
                           "size": 18,
                           "color": font_color
                       })
    fig = go.Figure(data=data, layout=layout)
    return fig


def coverage_x10_scatterplot(selected_transcript, selected_gene, selected_sample):
    """
    Graph object updating handler for mean_coverage-coverageX10 plot.

    :param selected_transcript: Transcript selected in dropdown.
    :param selected_gene: Gene selected in dropdown.
    :param selected_sample: Selected sample to highlight.
    :return: Figure object to update graph.
    """
    mean_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov", sample_ids=True)
    x10_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10", sample_ids=True)
    statistics_value = get_stats_for_one_sample(Record, selected_sample, selected_transcript, selected_gene, "mean_cov")

    scatter = go.Scatter(
        x=x10_cov_data['value'],
        y=mean_cov_data['value'],
        mode="markers",
        text=mean_cov_data["id"],
        name="Mean coverage - coverage X10",
        marker=dict(
            color=np.where(mean_cov_data['value'] == statistics_value, 'red', font_color),
            size=np.where(mean_cov_data['value'] == statistics_value, 18, 12)))

    data = [scatter]

    layout = go.Layout(title=f"Mean coverage - coverage X10",
                       height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       xaxis={"title": "Coverage X10"},
                       yaxis={"title": "Mean coverage"},
                       font={
                           "size": 18,
                           "color": font_color
                       }
                       )
    fig = go.Figure(data=data, layout=layout)
    return fig


def empty_plot():
    scat = go.Scatter(
        x=[],
        y=[]
    )
    data = [scat]
    layout = go.Layout(height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color
                       )
    fig = go.Figure(data=data, layout=layout)
    return fig