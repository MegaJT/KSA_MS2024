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
    card = dbc.Card(
        [
            dbc.CardHeader(
                [Header],
                style={
                    "font-size": "20px",
                    "height": "100px",
                    "background-color": "#f8f9fa",  # Light background for header
                    "border-bottom": "1px solid #dee2e6"  # Border for separation
                },
            ),
            dbc.CardBody(
                [Body],
                style={
                    "font-size": "60px",
                    "font-weight": "bold",
                    "background-color": bgcolor,
                },
            ),
        ],
        style={
            "text-align": "center",
            "height": "200px",
            "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.5)",  # Shadow effect
            "border-radius": "10px",  # Rounded corners
            "margin": "5px",  # Space between cards
            "overflow": "hidden",  # Clean edges for rounded corners
        },
    )
    return card




def create_horizontal_bar_chart(categories, values, title):
    # Reverse categories and values to maintain the correct order
    categories = categories[::-1]
    values = values[::-1]

    # Create the bar chart
    fig = go.Figure(
        data=go.Bar(
            x=values,
            y=categories,
            text=[f"{v}" for v in values],  # Display percentage values
            textposition='auto',  # Automatically position the text
            orientation='h',  # Horizontal orientation
            hoverinfo='x+y',  # Show category and value on hover
            marker=dict(
                color='#6c757d',  # Secondary color (Bootstrap)
                line=dict(width=2, color='#5a6268'),  # Border color
                opacity=0.9  # Transparency for smoother visuals
            ),
        )
    )

    # Update layout with all relevant styling and shadow effect
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family='Arial, sans-serif'),
            x=0.5,  # Center the title
            xanchor='center'
        ),
        xaxis=dict(
            title='Score',
            showgrid=True,
            gridcolor='#e9ecef',  # Light grid lines
            zeroline=False  # Hide the zero line
        ),
        yaxis=dict(
            #title='Category',
            showgrid=False  # No grid lines on the y-axis
        ),
        paper_bgcolor='#f8f9fa',  # Light Bootstrap background
        plot_bgcolor='#ffffff',  # White plot area background
        margin=dict(l=100, r=20, t=50, b=50),  # Adjust layout margins
        barmode='group',  # Prevent bar overlap
        shapes=[
            dict(
                type="rect",  # Shadow rectangle
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="rgba(0, 0, 0, 0)", width=0),
                fillcolor="rgba(0, 0, 0, 0.05)"  # Subtle shadow effect
            )
        ],
        autosize=True  # Ensure responsiveness
    )

    return fig

















'''
# Horizontal bar chart function
def create_horizontal_bar_chart(categories, values,title):
    categories = categories[::-1]
    values = values[::-1]
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
