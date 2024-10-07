import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
# Function to get gradient color
def get_gradient_color(value):
    if value <= 10:
        return '#FA9372'
    elif value <= 20:
        return '#F29D75'
    elif value <= 30:
        return '#EAA779'
    elif value <= 40:
        return '#E2B27C'
    elif value <= 50:
        return '#DABC80'
    elif value <= 60:
        return '#D2C683'
    elif value <= 70:
        return '#CAD087'
    elif value <= 80:
        return '#C2DB8A'
    elif value <= 90:
        return '#BAE58E'
    else:
        return '#B2EF91'

# Function to create cards
def Create_Cards(Header, Body, bgcolor):
    card = dbc.Card([
        dbc.CardHeader([Header], style={"font-size": "20px", "height": "100px"}),
        dbc.CardBody([Body], style={"font-size": "60px", "font-weight": "bold", "background-color": bgcolor}),
    ], style={"text-align": "center", "height": "200px"})
    return card


# Horizontal bar chart function
def create_horizontal_bar_chart(categories, values,title):
    data = [
        go.Bar(
            x=values,  # X-axis values (horizontal bars)
            text=values,  # Show values on the bars
            textposition='auto',  # Position text automatically
            y=categories,  # Y-axis values
            orientation='h'  # Set horizontal orientation
        )
    ]
    
    layout = go.Layout(
        title=title,
        xaxis=dict(title='Score'),
        yaxis=dict(title='Category')
    )
    
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(marker_color='#6c757d')  # Primary color

    return fig

'''
def create_horizontal_bar_chart(categories, values, title):
    # Create a bar chart using Plotly Express
    fig = px.bar(
        x=values,  # X-axis values (horizontal bars)
        y=categories,  # Y-axis values
        orientation='h',  # Set horizontal orientation
        labels={'x': 'Score', 'y': 'Category'}  # Axis labels
    )

    # Update layout to center and bold the title
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Anchor to the center
            'font': {'size': 20, 'color': 'black', 'family': 'Arial', 'bold': True}
        },
        xaxis_title="Score",
        yaxis_title="Category"
    )
    
    return fig
'''
