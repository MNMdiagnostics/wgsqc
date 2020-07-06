import plotly.graph_objects as go
from new_database.new_base import WGSqc
import numpy as np
from new_database.new_queries import get_stats_for_plot


components_color = '#080808'
font_color = '#7FDBFF'
fig_height = 570
marker_default_size = 10
marker_selected_size = 18


def get_small_boxplot(selected_transcript, selected_gene, statistics):
    """
    Graph object updating handler for coverage boxplot.

    :param selected_transcript: Transcript selected in dropdown.
    :param selected_gene: Gene selected in dropdown.
    :param statistics: Statistics to plot. One from following: "mean_coverage", "percentage_above_10", "percentage_above_20", "percentage_above_30".
    :return: Figure object to update graph.
    """

    stat_dataframe = get_stats_for_plot(WGSqc, selected_transcript, selected_gene, statistics,
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

    all_plots = [boxplot]

    layout = go.Layout(title=f"{statistics} boxplot",
                       height=fig_height,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       font={
                           "size": 18,
                           "color": font_color
                       })
    fig = go.Figure(data=all_plots, layout=layout)

    return fig


def get_small_scatter(selected_transcript, selected_gene, selected_sample):
    """
    Graph object updating handler for mean_coverage-coverageX10 plot.

    :param selected_transcript: Transcript selected in dropdown.
    :param selected_gene: Gene selected in dropdown.
    :param selected_sample: Selected sample to highlight.
    :return: Figure object to update graph.
    """
    mean_cov_data = get_stats_for_plot(WGSqc, selected_transcript, selected_gene, "mean_coverage", sample_ids=True)
    x10_cov_data = get_stats_for_plot(WGSqc, selected_transcript, selected_gene, "percentage_above_10", sample_ids=True)

    scatter = go.Scatter(
        x=x10_cov_data['value'],
        y=mean_cov_data['value'],
        mode="markers",
        hovertemplate=
        '<i>Sample: </i>%{text}' +
        '<br><i>Mean coverage: </i>%{y}' +
        '<br><i>X10 coverage: </i>%{x}<br>',
        text=mean_cov_data["id"],
        name="Mean coverage - coverage X10",
        marker=dict(
            color=np.where(mean_cov_data['id'] == selected_sample, 'red', font_color),
            size=np.where(mean_cov_data['id'] == selected_sample, marker_selected_size, marker_default_size))
    )

    all_plots = [scatter]

    layout = go.Layout(title=f"Mean coverage - coverage X10",
                       height=fig_height,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       hoverlabel=dict(
                           bgcolor='black',
                           font_size=16,
                           bordercolor=font_color,
                       ),
                       xaxis={"title": "Coverage X10"},
                       yaxis={"title": "Mean coverage"},
                       font={
                           "size": 18,
                           "color": font_color
                       }
                       )
    fig = go.Figure(data=all_plots, layout=layout)
    return fig


def empty_plot():
    scat = go.Scatter(
        x=[],
        y=[]
    )
    all_plots = [scat]
    layout = go.Layout(height=fig_height,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color
                       )
    fig = go.Figure(data=all_plots, layout=layout)

    return fig
