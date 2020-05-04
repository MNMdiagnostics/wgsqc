import plotly.graph_objects as go
from database.queries import get_stats_for_plot, get_stats_for_one_sample
from database.base import Record
import numpy as np


components_color = '#080808'
font_color = '#7FDBFF'


def get_boxplot(selected_transcript, selected_gene, statistics):
    mean_cov_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, statistics,
                                                            sample_ids=True)
    mean_cov_boxplot = go.Box(
        y=mean_cov_dataframe['value'],
        name="Mean coverage",
        text=mean_cov_dataframe['id'],
        marker=dict(
            color=font_color,
        ),
        showlegend=False)

    data = [mean_cov_boxplot]

    layout = go.Layout(title=f"Coverage boxplot",
                       height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       font={
                           "size": 18,
                           "color": font_color
                       })
    fig = go.Figure(data=data, layout=layout)
    return fig


def get_scatterplot(selected_transcript, selected_gene, selected_sample, stat):
    stat_dataframe = get_stats_for_plot(Record, selected_transcript, selected_gene, stat,
                                                            sample_ids=True)
    stat = get_stats_for_one_sample(Record, selected_sample, selected_transcript, selected_gene, stat)

    scatter = go.Scatter(
        y=stat_dataframe['value'],
        x=[1 for x in range(len(stat_dataframe['value']))],
        name="Mean coverage",
        mode='markers',
        text=stat_dataframe['id'],
        marker=dict(
            color=np.where(stat_dataframe['value'] == stat, 'red', font_color),
            size=np.where(stat_dataframe['value'] == stat, 18, 12)
        ),
        showlegend=False)

    data = [scatter]

    layout = go.Layout(title=f"Coverage scatterplot",
                       height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       xaxis={'title': '',
                              'showgrid': False},
                       font={
                           "size": 18,
                           "color": font_color
                       })
    fig = go.Figure(data=data, layout=layout)
    return fig


def coverage_x10_scatterplot(selected_transcript, selected_gene, selected_sample):
    mean_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov", sample_ids=True)
    x10_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10", sample_ids=True)
    stat = get_stats_for_one_sample(Record, selected_sample, selected_transcript, selected_gene, "mean_cov")

    scat = go.Scatter(
        x=x10_cov_data['value'],
        y=mean_cov_data['value'],
        mode="markers",
        text=mean_cov_data["id"],
        name="Mean coverage against coverage X10",
        marker=dict(
            color=np.where(mean_cov_data['value'] == stat, 'red', font_color),
            size=np.where(mean_cov_data['value'] == stat, 18, 12)))

    data = [scat]

    layout = go.Layout(title=f"Mean coverage against coverage X10",
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