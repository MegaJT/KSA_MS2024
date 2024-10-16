import dash
from dash import Dash,html, dcc, Output, Input,callback
import dash_bootstrap_components as dbc
import Input_Data as ID
import Input_Function as IF

from config import box_shadow
from config import pill_style
from config import chart_bg_space_style



dash.register_page(__name__, path="/AS_Call_center")


df=ID.AS_cc_df


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
                dcc.Dropdown(id='acc-eval-brand-dropdown', options=ID.Eval_Brand_DropDown_List, value=0, placeholder="Select Evaluation Brand")
            ]),
            dbc.Col([
                html.Label("Select City:"),
                dcc.Dropdown(id='acc-city-dropdown', options=ID.City_DropDown_List, value=0, placeholder="Select City")
            ])
        ])
    ]),
    html.Div(html.H4(id="acc-base-display"),style=pill_style),
    html.Div(id="acc-card-container", style={"margin-top": "20px"}),

    html.Hr(),  
    html.Div([
        html.H2("Detailed Score", style={"text-align": "center", "margin-top": "20px"}), 
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='acc-chart1'),style={"box-shadow":box_shadow}),width=4),
            dbc.Col(html.Div(dcc.Graph(id='acc-chart2'),style={"box-shadow":box_shadow}),width=4),
            dbc.Col(html.Div(dcc.Graph(id='acc-chart3'),style={"box-shadow":box_shadow}),width=4),
            ], style={"margin-top": "20px"}),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='acc-chart4'),style={"box-shadow":box_shadow}),width=4),
            ], style={"margin-top": "20px"})    
    ],style=chart_bg_space_style)        
    
], fluid=True)


@callback(
    [Output('acc-base-display', 'children'),  # For displaying Base
    Output('acc-card-container', 'children'),
    Output('acc-chart1', 'figure'),
    Output('acc-chart2', 'figure'),
    Output('acc-chart3', 'figure'),
    Output('acc-chart4', 'figure'),
    ],
    [Input('acc-eval-brand-dropdown', 'value'), Input('acc-city-dropdown', 'value')]
)
def update_acc_cards(eval_brand, city):
    # Filter data based on the selected brand and city
    df_filtered = df.copy()
    if eval_brand != 0:
        df_filtered = df_filtered[df_filtered['Eval_Brand'] == eval_brand]
    
    if city != 0:
        df_filtered = df_filtered[df_filtered['City'] == city]

    # List of columns we want to aggregate
    columns = [
        'wInitial', 'wCallAgent', 'wCourtesy', 
        'wOverallImpression', 'wOverallScore',         
        ]
    # Use .agg() to calculate the mean of the relevant columns
    df_filtered_mean = df_filtered[columns].mean().round(1)

    # Handle NaN values (set them to 0 where necessary)
    df_filtered_mean = df_filtered_mean.fillna(0)

    
    # Calculate metrics (use round() for cleaner display)
    
    Initial = df_filtered_mean['wInitial']
    CallAgent = df_filtered_mean['wCallAgent']
    Courtesy = df_filtered_mean['wCourtesy']
    OverallImp = df_filtered_mean['wOverallImpression']
    OverallScore = df_filtered_mean['wOverallScore']
    

    # Create cards with dynamic values and gradient background
    cards = [
        dbc.Col(IF.Create_Cards("INITIAL", Initial, IF.get_gradient_color(Initial))),
        dbc.Col(IF.Create_Cards("CALL AGENT", CallAgent, IF.get_gradient_color(CallAgent))),
        dbc.Col(IF.Create_Cards("COURTESY", Courtesy, IF.get_gradient_color(Courtesy))),
        dbc.Col(IF.Create_Cards("OVERALL IMPRESSION", OverallImp, IF.get_gradient_color(OverallImp))),
        dbc.Col(IF.Create_Cards("OVERALL SCORE", OverallScore, IF.get_gradient_color(OverallScore))),
        
    ]

    def get_chart_data(columns):
        values = df_filtered[columns].mean().round(1).fillna(0)
        return values.tolist()

    # Data for the horizontal bar charts
    categories_1 = list_1 = [
    'Attempts before answer',
    'Rings before answer',
    'Prompts before person',
    'Time to reach person'
    ]
    values_1 = get_chart_data(['iQ1a','iQ1b','iQ1d','iQ1e'])

    categories_2 = [
    'Background noise level',
    'How you were greeted',
    'Agent attentiveness level',
    'Personalized service actions',
    'Agent’s manner throughout',
    'Clarity of agent’s communication'
    ]
    values_2 = get_chart_data(['iQ2b','iQ2c','iQ2d','iQ2e','iQ2f','iQ2g'])

    categories_3 = [
    'Agent actions during interaction',
    'Advisor actions during interaction'
    ]
    values_3 = get_chart_data(['iQ3a','iQ3_2',])

    categories_4 = [
    'Likelihood to visit for service',
    'Overall call center experience'
    ]
    values_4 = get_chart_data(['iQ4_1','iQ4_1b',])

        
        
    
    # Update charts with filtered data
    chart1 = IF.create_horizontal_bar_chart(categories_1, values_1,title='INITIAL')
    chart2 = IF.create_horizontal_bar_chart(categories_2, values_2,title='CALL AGENT')
    chart3 = IF.create_horizontal_bar_chart(categories_3, values_3,title='COURTESY')
    chart4 = IF.create_horizontal_bar_chart(categories_4, values_4,title='OVERALL IMPRESSION')
    
    
    Base = f"Base: {df_filtered['Eval_Brand'].nunique()}"
    return Base,dbc.Row(cards), chart1, chart2, chart3, chart4
        
