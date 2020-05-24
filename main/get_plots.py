import plotly.graph_objects as go
from database.queries import get_stats_for_plot
from database.base import Record
import numpy as np


components_color = '#080808'
font_color = '#7FDBFF'
fig_height = 570
marker_default_size = 10
marker_selected_size = 18


def get_boxplot(selected_transcript, selected_gene, statistics):
    """
    Graph object updating handler for coverage boxplot.

    :param selected_transcript: Transcript selected in dropdown.
    :param selected_gene: Gene selected in dropdown.
    :param statistics: Statistics to plot. One from following: "mean_cov", "cov_10", "cov_20", "cov_30".
    :return: Figure object to update graph.
    """

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


def get_scatterplot(selected_transcript, selected_gene, selected_sample):
    """
    Graph object updating handler for coverage scatterlot.

    :param selected_transcript: Transcript selected in dropdown.
    :param selected_gene: Gene selected in dropdown.
    :param selected_sample: Sample to highlight selected in radiobox.
    :param statistics: Statistics to plot. One from following: "mean_cov", "cov_10", "cov_20", "cov_30".
    :return: Figure object to update graph.
    """

    mean_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov",
                                        sample_ids=True).sort_values(by=['id'])
    x10_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10",
                                        sample_ids=True).sort_values(by=['id'])
    x20_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_20",
                                       sample_ids=True).sort_values(by=['id'])
    x30_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_30",
                                       sample_ids=True).sort_values(by=['id'])

    n_samples = len(mean_dataframe['id'])

    scatter_mean = go.Scatter(
        y=mean_dataframe['value'],
        x=[x for x in range(len(mean_dataframe['value']))],
        name="mean coverage",
        mode='markers',
        hovertemplate=
        '<i>Sample: </i>%{text}' +
        '<br><i>Value: </i>%{y}<br>',
        text=mean_dataframe['id'],
        marker=dict(
            color=np.where(mean_dataframe['id'] == selected_sample, 'red', "#FCBF1E"),
            size=np.where(mean_dataframe['id'] == selected_sample, marker_selected_size, marker_default_size)
        ),
        showlegend=True)

    scatter_x10 = go.Scatter(
        y=x10_dataframe['value'],
        x=[x for x in range(len(x10_dataframe['value']))],
        name="X10 coverage",
        mode='markers',
        hovertemplate=
        '<i>Sample: </i>%{text}' +
        '<br><i>Value: </i>%{y}<br>',
        text=x10_dataframe['id'],
        marker=dict(
            color=np.where(x10_dataframe['id'] == selected_sample, 'red', font_color),
            size=np.where(x10_dataframe['id'] == selected_sample, marker_selected_size, marker_default_size)
        ),
        showlegend=True)

    scatter_x20 = go.Scatter(
        y=x20_dataframe['value'],
        x=[x for x in range(len(x20_dataframe['value']))],
        name="X20 coverage",
        mode='markers',
        hovertemplate=
        '<i>Sample: </i>%{text}' +
        '<br><i>Value: </i>%{y}<br>',
        text=x20_dataframe['id'],
        marker=dict(
            color=np.where(x20_dataframe['id'] == selected_sample, 'red', "#035AA6"),
            size=np.where(x20_dataframe['id'] == selected_sample, marker_selected_size, marker_default_size)
        ),
        showlegend=True)

    scatter_x30 = go.Scatter(
        y=x30_dataframe['value'],
        x=[x for x in range(len(x30_dataframe['value']))],
        name="X30 coverage",
        mode='markers',
        hovertemplate=
        '<i>Sample: </i>%{text}' +
        '<br><i>Value: </i>%{y}<br>',
        text=x30_dataframe['id'],
        marker=dict(
            color=np.where(x30_dataframe['id'] == selected_sample, 'red', "#120136"),
            size=np.where(x30_dataframe['id'] == selected_sample, marker_selected_size, marker_default_size)
        ),
        showlegend=True)

    all_plots = [scatter_mean, scatter_x10, scatter_x20, scatter_x30]

    layout = go.Layout(title=f"Coverages across samples, number of samples: {n_samples}",
                       height=fig_height,
                       hoverlabel=dict(
                           bgcolor='black',
                           font_size=16,
                           bordercolor=font_color,
                       ),
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       xaxis={'tickvals': [x for x in range(len(mean_dataframe['id']))],
                              'ticktext': mean_dataframe['id']
                              },
                       yaxis=dict(range=[0, 100.5]),
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
    mean_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov", sample_ids=True)
    x10_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10", sample_ids=True)

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
            size=np.where(mean_cov_data['id'] == selected_sample, marker_selected_size, marker_default_size)))

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