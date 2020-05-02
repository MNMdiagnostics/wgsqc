import plotly.graph_objects as go
from database.queries import get_stats_for_plot
from database.base import Record


def mean_cov_boxplots(selected_transcript, selected_gene):
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
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff',
        ),
        line=dict(
            color='#7fdbff'),
        showlegend=False)

    x10 = go.Box(
        y=x10_cov_data,
        name="Coverage X10",
        text=x10_cov_sample_ids,
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff'),
        line=dict(
            color='#7fdbff'),
        showlegend=False)

    x20 = go.Box(
        y=x20_cov_data,
        name="Coverage X20",
        text=x20_cov_sample_ids,
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff'),
        line=dict(
            color='#7fdbff'),
        showlegend=False)

    x30 = go.Box(
        y=x30_cov_data,
        name="Coverage X30",
        text=x30_cov_sample_ids,
        jitter=0.3,
        boxpoints='all',
        marker=dict(
            color='#7fdbff'),
        line=dict(
            color='#7fdbff'),
        showlegend=False)

    data = [mean_cov_boxplot, x10, x20, x30]

    layout = go.Layout(title=f"Coverage boxplots, number of samples: {n_samples}",
                       height=800,
                       paper_bgcolor='#010608',
                       plot_bgcolor='#010608',
                       font={
                           "size": 18,
                           "color": '#7fdbff'
                       })
    fig = go.Figure(data=data, layout=layout)
    return fig
