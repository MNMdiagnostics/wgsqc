import plotly.graph_objects as go
from database.queries import get_stats_for_plot, get_stats_for_one_sample
from database.base import Record
import pandas as pd
import numpy as np

components_color = '#080808'
font_color = '#7FDBFF'


def mean_cov_scatterplot(selected_transcript, selected_gene, selected_sample):
    # --------------------------- SCATTER PLOT ---------------------------
    mean_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov")
    x10_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10")
    n_samples = len(x10_cov_data)

    mean_cov_df = pd.DataFrame(mean_cov_data, columns=["val"])
    x10_df = pd.DataFrame(x10_cov_data, columns=["val"])

    mean_cov, _, _, _ = get_stats_for_one_sample(Record, selected_sample, selected_transcript, selected_gene)

    scat = go.Scatter(
        x=x10_df['val'],
        y=mean_cov_df['val'],
        mode="markers",
        name="Mean coverage against coverage X10",
        marker=dict(
            color=np.where(mean_cov_df['val'] == mean_cov, 'red', font_color),
            size=np.where(mean_cov_df['val'] == mean_cov, 18, 12)))

    data = [scat]

    layout = go.Layout(title=f"Mean coverage against coverage X10, number of samples: {n_samples}",
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