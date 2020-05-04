import plotly.graph_objects as go
from database.queries import get_stats_for_plot, get_stats_for_one_sample
from database.base import Record
import numpy as np
import pandas as pd

components_color = '#080808'
font_color = '#7FDBFF'


def mean_cov_boxplots(selected_transcript, selected_gene, selected_sample):
    # --------------------------- BOXPLOTS ---------------------------
    mean_cov_data, mean_cov_sample_ids = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov",
                                                            sample_ids=True)
    x10_cov_data, x10_cov_sample_ids = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10",
                                                          sample_ids=True)
    x20_cov_data, x20_cov_sample_ids = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_20",
                                                          sample_ids=True)
    x30_cov_data, x30_cov_sample_ids = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_30",
                                                          sample_ids=True)

    n_samples = len(mean_cov_sample_ids)

    mean_cov_boxplot = go.Box(
        y=mean_cov_data,
        name="Mean coverage",
        text=mean_cov_sample_ids,
        marker=dict(
            color=font_color,
        ),
        showlegend=False)

    x10_box = go.Box(
        y=x10_cov_data,
        name="Coverage X10",
        text=x10_cov_sample_ids,
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color=font_color),
        line=dict(
            color=font_color),
        showlegend=False)

    x20_box = go.Box(
        y=x20_cov_data,
        name="Coverage X20",
        text=x20_cov_sample_ids,
        marker=dict(
            color=font_color),
        showlegend=False)

    x30_box = go.Box(
        y=x30_cov_data,
        name="Coverage X30",
        text=x30_cov_sample_ids,
        marker=dict(
            color=font_color),
        showlegend=False)

    data = [mean_cov_boxplot, x10_box, x20_box, x30_box]

    layout = go.Layout(title=f"Coverage boxplots, number of samples: {n_samples}",
                       height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       font={
                           "size": 18,
                           "color": font_color
                       })
    fig = go.Figure(data=data, layout=layout)
    return fig
