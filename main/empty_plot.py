import plotly.graph_objs as go


def empty_plot():
    scat = go.Scatter(
        x=[],
        y=[]
    )
    data = [scat]
    layout = go.Layout(height=800,
                       paper_bgcolor='#010608',
                       plot_bgcolor='#010608'
                       )
    fig = go.Figure(data=data, layout=layout)
    return fig