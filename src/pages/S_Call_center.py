import dash
from dash import Dash,html, dcc, Output, Input,callback
import dash_bootstrap_components as dbc
import Input_Data as ID
import Input_Function as IF


dash.register_page(__name__, path="/S_Call_center")


df=ID.S_cc_df


# Brand and City Dictionaries
Eval_Brand_Dict = {1: 'Hyundai', 2: 'Toyota', 3: 'Nissan', 4: 'Ford', 5: 'Lincoln', 6: 'MG', 7: 'Cherry', 8: 'KIA'}
df['Eval_Brand_Text'] = df['Eval_Brand'].map(Eval_Brand_Dict)

City_Dict = {1: 'Riyadh', 2: 'Jeddah', 3: 'Dammam'}
df['City_Text'] = df['City'].map(City_Dict)


# Layout
layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Select Evaluation Brand:"),
                dcc.Dropdown(id='scc-eval-brand-dropdown', options=ID.Eval_Brand_DropDown_List, value=0, placeholder="Select Evaluation Brand")
            ]),
            dbc.Col([
                html.Label("Select City:"),
                dcc.Dropdown(id='scc-city-dropdown', options=ID.City_DropDown_List, value=0, placeholder="Select City")
            ])
        ])
    ]),
    html.H4(id="scc-base-display"),  # Updated dynamically in callback
    html.Div(id="scc-card-container", style={"margin-top": "20px"}),

    html.Hr(),  
    html.H2("Detailed Score", style={"text-align": "center", "margin-top": "20px"}), 
    dbc.Row([
        dbc.Col(dcc.Graph(id='scc-chart1'),width=4),
        dbc.Col(dcc.Graph(id='scc-chart2'),width=4),
        dbc.Col(dcc.Graph(id='scc-chart3'),width=4),
        ], style={"margin-top": "20px"}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='scc-chart4'),width=4),
        dbc.Col(dcc.Graph(id='scc-chart5'),width=4),
        
        ], style={"margin-top": "20px"})    
        
    
], fluid=True)


@callback(
    [Output('scc-base-display', 'children'),
    Output('scc-card-container', 'children'),
    Output('scc-chart1', 'figure'),
    Output('scc-chart2', 'figure'),
    Output('scc-chart3', 'figure'),
    Output('scc-chart4', 'figure'),
    Output('scc-chart5', 'figure'),
    
    ],
    [Input('scc-eval-brand-dropdown', 'value'), Input('scc-city-dropdown', 'value')]
)
def update_scc_cards(eval_brand, city):
    # Filter data based on the selected brand and city
    df_filtered = df.copy()
    if eval_brand != 0:
        df_filtered = df_filtered[df_filtered['Eval_Brand'] == eval_brand]
    
    if city != 0:
        df_filtered = df_filtered[df_filtered['City'] == city]

    # List of columns we want to aggregate
    columns = [
        'wInitial', 'wCallAgent', 'wCONSULTANTINTERACTION', 
        'wCONSULTANTKNOWLEDGE', 'wClosing', 'wOverallScore',         
        ]
    # Use .agg() to calculate the mean of the relevant columns
    df_filtered_mean = df_filtered[columns].mean().round(1)

    # Handle NaN values (set them to 0 where necessary)
    df_filtered_mean = df_filtered_mean.fillna(0)

    
    # Calculate metrics (use round() for cleaner display)
    
    Initial = df_filtered_mean['wInitial']
    CallAgent = df_filtered_mean['wCallAgent']
    CONSULTANTINTERACTION = df_filtered_mean['wCONSULTANTINTERACTION']
    CONSULTANTKNOWLEDGE = df_filtered_mean['wCONSULTANTKNOWLEDGE']
    Closing = df_filtered_mean['wClosing']
    OverallScore = df_filtered_mean['wOverallScore']
    

    # Create cards with dynamic values and gradient background
    cards = [
        dbc.Col(IF.Create_Cards("INITIAL", Initial, IF.get_gradient_color(Initial))),
        dbc.Col(IF.Create_Cards("CALL AGENT", CallAgent, IF.get_gradient_color(CallAgent))),
        dbc.Col(IF.Create_Cards("CONSULTANT INTERACTION", CONSULTANTINTERACTION, IF.get_gradient_color(CONSULTANTINTERACTION))),
        dbc.Col(IF.Create_Cards("CONSULTANT KNOWLEDGE", CONSULTANTKNOWLEDGE, IF.get_gradient_color(CONSULTANTKNOWLEDGE))),
        dbc.Col(IF.Create_Cards("CLOSING", Closing, IF.get_gradient_color(Closing))),
        dbc.Col(IF.Create_Cards("OVERALL SCORE", OverallScore, IF.get_gradient_color(OverallScore))),
        
    ]

    def get_chart_data(columns):
        values = df_filtered[columns].mean().round(1).fillna(0)
        return values.tolist()

    # Data for the horizontal bar charts
    categories_1 = ['iQ1a', 'iQ1c', 'iQ1d']
    values_1 = get_chart_data(['iQ1a', 'iQ1c', 'iQ1d'])

    categories_2 = ['iQ2b','iQ2c','iQ2d','iQ2e','iQ2f','iQ2g','iQ2h','iQ2i','iQ2k']
    values_2 = get_chart_data(['iQ2b','iQ2c','iQ2d','iQ2e','iQ2f','iQ2g','iQ2h','iQ2i','iQ2k'])

    categories_3 = ['iQ3a','iQ3b','iQ3d','iQ3e','iQ3f','iQ3g','iQ3h','iQ3i']
    values_3 = get_chart_data(['iQ3a','iQ3b','iQ3d','iQ3e','iQ3f','iQ3g','iQ3h','iQ3i'])

    categories_4 = ['iQ4a','iQ4b','iQ4c','iQ4d']
    values_4 = get_chart_data(['iQ4a','iQ4b','iQ4c','iQ4d'])

    categories_5 = ['iQ5a','iQ5c']
    values_5 = get_chart_data(['iQ5a','iQ5c'])

    
    
    

    
    # Update charts with filtered data
    chart1 = IF.create_horizontal_bar_chart(categories_1, values_1,title='INITIAL')
    chart2 = IF.create_horizontal_bar_chart(categories_2, values_2,title='CALL AGENT')
    chart3 = IF.create_horizontal_bar_chart(categories_3, values_3,title='INTERACTION')
    chart4 = IF.create_horizontal_bar_chart(categories_4, values_4,title='KNOWLEDGE')
    chart5 = IF.create_horizontal_bar_chart(categories_5, values_5,title='CLOSING')
    
    Base = f"Base: {len(df_filtered)}"

    return Base,dbc.Row(cards), chart1, chart2, chart3, chart4, chart5
        
