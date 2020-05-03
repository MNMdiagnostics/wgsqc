import plotly.graph_objects as go
from database.queries import get_stats_for_plot
from database.base import Record

components_color = '#080808'
font_color = '#7FDBFF'


def mean_cov_scatterplot(selected_transcript, selected_gene):
    # --------------------------- SCATTER PLOT ---------------------------
    mean_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "mean_cov")
    x10_cov_data = get_stats_for_plot(Record, selected_transcript, selected_gene, "cov_10")
    n_samples = len(x10_cov_data)

    scat = go.Scatter(
        x=x10_cov_data,
        y=mean_cov_data,
        mode="markers",
        name="Mean coverage against coverage X10",
        marker=dict(
            color=font_color,
            size=12),
        line=dict(
            color=font_color))
    data = [scat]
    layout = go.Layout(title=f"Mean coverage against coverage X10, number of samples: {n_samples}",
                       height=750,
                       paper_bgcolor=components_color,
                       plot_bgcolor=components_color,
                       xaxis={
                           "title": "Coverage X10"
                       },
                       yaxis={
                           "title": "Mean coverage"
                       },
                       font={
                           "size": 18,
                           "color": font_color
                       }
                       )
    fig = go.Figure(data=data, layout=layout)
    return fig