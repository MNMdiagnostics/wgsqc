import plotly.graph_objects as go
from database.queries import get_stats_for_plot
from database.base import Record


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
            color='#7fdbff',
            size=12),
        line=dict(
            color='#7fdbff'))
    data = [scat]
    layout = go.Layout(title=f"Mean coverage against coverage X10, number of samples: {n_samples}",
                       height=800,
                       paper_bgcolor='#010608',
                       plot_bgcolor='#010608',
                       xaxis={
                           "title": "Coverage X10"
                       },
                       yaxis={
                           "title": "Mean coverage"
                       },
                       font={
                           "size": 18,
                           "color": '#7fdbff'
                       }
                       )
    fig = go.Figure(data=data, layout=layout)
    return fig