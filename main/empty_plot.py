import plotly.graph_objs as go

components_color = '#080808'


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