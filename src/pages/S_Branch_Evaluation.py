import dash
from dash import Dash,html, dcc, Output, Input,callback
import dash_bootstrap_components as dbc
import Input_Data as ID
import Input_Function as IF


dash.register_page(__name__, path="/S_Branch_Evaluation")


df=ID.S_br_df


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
                dcc.Dropdown(id='sbr-eval-brand-dropdown', options=ID.Eval_Brand_DropDown_List, value=0, placeholder="Select Evaluation Brand")
            ]),
            dbc.Col([
                html.Label("Select City:"),
                dcc.Dropdown(id='sbr-city-dropdown', options=ID.City_DropDown_List, value=0, placeholder="Select City")
            ])
        ])
    ]),
    html.H4(id="sbr-base-display"),  # Updated dynamically in callback
    html.Div(id="sbr-card-container", style={"margin-top": "20px"}),

    html.Hr(),  
    html.H2("Detailed Score", style={"text-align": "center", "margin-top": "20px"}), 
    dbc.Row([
        dbc.Col(dcc.Graph(id='sbr-chart1'),width=4),
        dbc.Col(dcc.Graph(id='sbr-chart2'),width=4),
        dbc.Col(dcc.Graph(id='sbr-chart3'),width=4),
        ], style={"margin-top": "20px"}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='sbr-chart4'),width=4),
        dbc.Col(dcc.Graph(id='sbr-chart5'),width=4),
        dbc.Col(dcc.Graph(id='sbr-chart6'),width=4),
        ], style={"margin-top": "20px"})    
        
    
], fluid=True)


@callback(
    [Output('sbr-base-display', 'children'),
    Output('sbr-card-container', 'children'),
    Output('sbr-chart1', 'figure'),
    Output('sbr-chart2', 'figure'),
    Output('sbr-chart3', 'figure'),
    Output('sbr-chart4', 'figure'),
    Output('sbr-chart5', 'figure'),
    Output('sbr-chart6', 'figure'),
    ],
    [Input('sbr-eval-brand-dropdown', 'value'), Input('sbr-city-dropdown', 'value')]
)
def update_sbr_cards(eval_brand, city):
    # Filter data based on the selected brand and city
    df_filtered = df.copy()
    if eval_brand != 0:
        df_filtered = df_filtered[df_filtered['Eval_Brand'] == eval_brand]
    
    if city != 0:
        df_filtered = df_filtered[df_filtered['City'] == city]

    # List of columns we want to aggregate
    columns = [
        'wFacility', 'wInitialgreet', 'wCONSULTANTINTERACTION', 
        'wCONSULTANTKNOWLEDGE', 'wClosing', 'wFacilityEnvironment', 
        'wOverallImpression'
        ]
    # Use .agg() to calculate the mean of the relevant columns
    df_filtered_mean = df_filtered[columns].mean().round(1)

    # Handle NaN values (set them to 0 where necessary)
    df_filtered_mean = df_filtered_mean.fillna(0)

    
    # Calculate metrics (use round() for cleaner display)
    
    Facility = df_filtered_mean['wFacility']
    Initialgreet = df_filtered_mean['wInitialgreet']
    CONSULTANTINTERACTION = df_filtered_mean['wCONSULTANTINTERACTION']
    CONSULTANTKNOWLEDGE = df_filtered_mean['wCONSULTANTKNOWLEDGE']
    Closing = df_filtered_mean['wClosing']
    FacilityEnvironment = df_filtered_mean['wFacilityEnvironment']
    OverallImpression = df_filtered_mean['wOverallImpression']

    # Create cards with dynamic values and gradient background
    cards = [
        dbc.Col(IF.Create_Cards("FACILITY", Facility, IF.get_gradient_color(Facility))),
        dbc.Col(IF.Create_Cards("INITIAL GREET", Initialgreet, IF.get_gradient_color(Initialgreet))),
        dbc.Col(IF.Create_Cards("CONSULTANT INTERACTION", CONSULTANTINTERACTION, IF.get_gradient_color(CONSULTANTINTERACTION))),
        dbc.Col(IF.Create_Cards("CONSULTANT KNOWLEDGE", CONSULTANTKNOWLEDGE, IF.get_gradient_color(CONSULTANTKNOWLEDGE))),
        dbc.Col(IF.Create_Cards("CLOSING", Closing, IF.get_gradient_color(Closing))),
        dbc.Col(IF.Create_Cards("FACILITY ENVIRONMENT", FacilityEnvironment, IF.get_gradient_color(FacilityEnvironment))),
        dbc.Col(IF.Create_Cards("OVERALL IMPRESSION", OverallImpression, IF.get_gradient_color(OverallImpression))),
    ]

    def get_chart_data(columns):
        values = df_filtered[columns].mean().round(1).fillna(0)
        return values.tolist()

    # Data for the horizontal bar charts
    categories_1 = ['Parking availability', 'Valet parking facility', 'Guided with parking']
    values_1 = get_chart_data(['iQ1a', 'iQ1b', 'iQ1c'])

    categories_2 = ['Time before greeted','Who provided greeting','Greeting description','Appearance','Handshake']
    values_2 = get_chart_data(['iQ2a', 'iQ2c', 'iQ2d', 'iQ2e'])

    categories_3 = ['Manners','Recheck personal info','Asked personal info','Asked any Questions','Offer Tea/Coffee','Level of attentiveness','Level of recommendation']
    values_3 = get_chart_data(['iQ3a', 'iQ3b', 'iQ3c', 'iQ3d', 'iQ3e', 'iQ3f', 'iQ3g'])

    categories_4 = ['Model Advantages','Response','Test drive','Booking ','Booking assistance','Summary of impression ']
    values_4 = get_chart_data(['iQ4a', 'iQ4b', 'iQ4c', 'iQ4d', 'iQ4e', 'iQ4f'])

    categories_5 = ['Promotion','Pricing','Lease eligibility','Lease information','Lease explanation','Alternate Finance','Response to Objection','End of Interaction']
    values_5 = get_chart_data(['iQ5a', 'iQ5b', 'iQ5c', 'iQ5d', 'iQ5e', 'iQ5f', 'iQ5g'])

    categories_6 = ['Appearance','Visible amenities','Seating area','Toilet facility','Car display','Vehicle inventory']
    values_6 = get_chart_data(['iQ6a', 'iQ6c', 'iQ6d', 'iQ6e', 'iQ6f', 'iQ6g'])

    
    

    
    # Update charts with filtered data
    chart1 = IF.create_horizontal_bar_chart(categories_1, values_1,title='FACILITY')
    chart2 = IF.create_horizontal_bar_chart(categories_2, values_2,title='GREETING')
    chart3 = IF.create_horizontal_bar_chart(categories_3, values_3,title='INTERACTION')
    chart4 = IF.create_horizontal_bar_chart(categories_4, values_4,title='KNOWLEDGE')
    chart5 = IF.create_horizontal_bar_chart(categories_5, values_5,title='CLOSING')
    chart6 = IF.create_horizontal_bar_chart(categories_6, values_6,title='FACILITY ENVIRONMENT')


    Base = f"Base: {len(df_filtered)}"

    return Base,dbc.Row(cards), chart1, chart2, chart3, chart4, chart5, chart6
        
