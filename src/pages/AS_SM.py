import dash
from dash import Dash,html, dcc, Output, Input,callback
import dash_bootstrap_components as dbc
import Input_Data as ID
import Input_Function as IF


from config import box_shadow
from config import pill_style
from config import chart_bg_space_style



dash.register_page(__name__, path="/AS_SM")


df=ID.AS_sm_df


# Brand and City Dictionaries
Eval_Brand_Dict = {1: 'Hyundai', 2: 'Toyota', 3: 'Nissan', 4: 'Ford', 5: 'Lincoln', 6: 'MG', 7: 'Cherry', 8: 'KIA'}
df['Eval_Brand_Text'] = df['Eval_Brand'].map(Eval_Brand_Dict)

City_Dict = {1: 'Riyadh', 2: 'Jeddah', 3: 'Dammam'}
df['City_Text'] = df['City'].map(City_Dict)

box_shadow= "0px 4px 8px rgba(0, 0, 0, 0.5)"

# Layout
layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Select Evaluation Brand:"),
                dcc.Dropdown(id='asm-eval-brand-dropdown', options=ID.Eval_Brand_DropDown_List, value=0, placeholder="Select Evaluation Brand")
            ]),
            dbc.Col([
                html.Label("Select City:"),
                dcc.Dropdown(id='asm-city-dropdown', options=ID.City_DropDown_List, value=0, placeholder="Select City")
            ])
        ])
    ]),
    
    html.Div(html.H4(id="asm-base-display"),style=pill_style),
    html.Div(id="asm-card-container", style={"margin-top": "20px"}),

    html.Hr(),  
    html.Div([
        html.H2("Detailed Score", style={"text-align": "center", "margin-top": "20px"}), 
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='asm-chart1'),style={"box-shadow":box_shadow}),width=12),
            ], style={"margin-top": "20px"}),
    ]),    
], fluid=True)


@callback(
    [Output('asm-base-display', 'children'),  # For displaying Base
    Output('asm-card-container', 'children'),
    Output('asm-chart1', 'figure'),
        ],
    [Input('asm-eval-brand-dropdown', 'value'), Input('asm-city-dropdown', 'value')]
)
def update_aon_cards(eval_brand, city):
    # Filter data based on the selected brand and city
    df_filtered = df.copy()
    if eval_brand != 0:
        df_filtered = df_filtered[df_filtered['Eval_Brand'] == eval_brand]
    
    if city != 0:
        df_filtered = df_filtered[df_filtered['City'] == city]

    # List of columns we want to aggregate
    columns = [
        'wOverallScore'
        ]
    # Use .agg() to calculate the mean of the relevant columns
    df_filtered_mean = df_filtered[columns].mean().round(1)

    # Handle NaN values (set them to 0 where necessary)
    df_filtered_mean = df_filtered_mean.fillna(0)

    
    # Calculate metrics (use round() for cleaner display)
    
    OverallScore = df_filtered_mean['wOverallScore']
    

    # Create cards with dynamic values and gradient background
    cards = [
        dbc.Col(IF.Create_Cards("OVERALL SCORE", OverallScore, IF.get_gradient_color(OverallScore))),
        
    ]

    def get_chart_data(columns):
        values = df_filtered[columns].mean().round(1).fillna(0)
        return values.tolist()

    # Data for the horizontal bar charts
    categories_1 = [
    'Time to respond via DM', 
    'Time to respond publicly', 
    'First response description', 
    'Consultant’s response description', 
    'Clarity of consultant’s communication', 
    'Consultant actions during interaction', 
    'Information provided during interaction about service/spare parts', 
    'Usefulness of information provided', 
    'How consultant closed the conversation', 
    'Received call/response from service agent or spare parts consultant', 
    'Service centre visit date confirmed', 
    'Overall experience with social media interaction for service query', 
    'Likelihood of future vehicle purchase'
    ]

    values_1 = get_chart_data([
        'iQ2', 'iQ3', 'iQ4', 'iQ5', 'iQ6', 'iQ7', 'iQ8', 'iQ9', 
        'iQ10', 'iQ11', 'iQ12', 'iQ13'
    ])


    # Update charts with filtered data
    chart1 = IF.create_horizontal_bar_chart(categories_1, values_1,title='OVERALL')
    
    Base = f"Base: {len(df_filtered)}"
    return Base,dbc.Row(cards), chart1
        
