import dash
from dash import Dash,html, dcc, Output, Input,callback
import dash_bootstrap_components as dbc
import Input_Data as ID
import Input_Function as IF


dash.register_page(__name__, path="/AS_Service_Center")


df=ID.AS_sc_df


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
                dcc.Dropdown(id='asc-eval-brand-dropdown', options=ID.Eval_Brand_DropDown_List, value=0, placeholder="Select Evaluation Brand")
            ]),
            dbc.Col([
                html.Label("Select City:"),
                dcc.Dropdown(id='asc-city-dropdown', options=ID.City_DropDown_List, value=0, placeholder="Select City")
            ])
        ])
    ]),
    html.H4(id="asc-base-display"),  # Updated dynamically in callback
    html.Div(id="asc-card-container", style={"margin-top": "20px"}),

    html.Hr(),  
    html.H2("Detailed Score", style={"text-align": "center", "margin-top": "20px"}), 
    dbc.Row([
        dbc.Col(dcc.Graph(id='asc-chart1'),width=6),
        dbc.Col(dcc.Graph(id='asc-chart2'),width=6),
        dbc.Col(dcc.Graph(id='asc-chart3'),width=6),
        dbc.Col(dcc.Graph(id='asc-chart4'),width=6),
        dbc.Col(dcc.Graph(id='asc-chart5'),width=6),
        dbc.Col(dcc.Graph(id='asc-chart6'),width=6),
        dbc.Col(dcc.Graph(id='asc-chart7'),width=6),
        dbc.Col(dcc.Graph(id='asc-chart8'),width=6),
        ], style={"margin-top": "20px"}),
        
], fluid=True)


@callback(
    [Output('asc-base-display', 'children'),  # For displaying Base
    Output('asc-card-container', 'children'),
    Output('asc-chart1', 'figure'),
    Output('asc-chart2', 'figure'),
    Output('asc-chart3', 'figure'),
    Output('asc-chart4', 'figure'),
    Output('asc-chart5', 'figure'),
    Output('asc-chart6', 'figure'),
    Output('asc-chart7', 'figure'),
    Output('asc-chart8', 'figure'),
        ],
    [Input('asc-eval-brand-dropdown', 'value'), Input('asc-city-dropdown', 'value')]
)
def update_asc_cards(eval_brand, city):
    # Filter data based on the selected brand and city
    df_filtered = df.copy()
    if eval_brand != 0:
        df_filtered = df_filtered[df_filtered['Eval_Brand'] == eval_brand]
    
    if city != 0:
        df_filtered = df_filtered[df_filtered['City'] == city]

    # List of columns we want to aggregate
    columns = [
        'wInitial',
        'wServiceAdvisor',
        'wSalesConsultant',
        'wServicingTime',
        'wVehicleDel',
        'wFacility',
        'wOverallImpression',
        'wOverallScore',

        ]
    # Use .agg() to calculate the mean of the relevant columns
    df_filtered_mean = df_filtered[columns].mean().round(1)

    # Handle NaN values (set them to 0 where necessary)
    df_filtered_mean = df_filtered_mean.fillna(0)

    
    # Calculate metrics (use round() for cleaner display)
    
    Initial = df_filtered_mean['wInitial']
    ServiceAdvisor = df_filtered_mean['wServiceAdvisor']
    SalesConsultant = df_filtered_mean['wSalesConsultant']
    ServicingTime = df_filtered_mean['wServicingTime']
    VehicleDel = df_filtered_mean['wVehicleDel']
    Facility = df_filtered_mean['wFacility']
    OverallImpression = df_filtered_mean['wOverallImpression']
    OverallScore = df_filtered_mean['wOverallScore']



    

    # Create cards with dynamic values and gradient background
    cards = [
        dbc.Col(IF.Create_Cards("INITIAL", Initial, IF.get_gradient_color(Initial          ))),
        dbc.Col(IF.Create_Cards("SERVICE ADVISOR", ServiceAdvisor, IF.get_gradient_color(ServiceAdvisor   ))),
        dbc.Col(IF.Create_Cards("SALES CONSULTANT", SalesConsultant, IF.get_gradient_color(SalesConsultant  ))),
        dbc.Col(IF.Create_Cards("SERVICING TIME", ServicingTime, IF.get_gradient_color(ServicingTime    ))),
        dbc.Col(IF.Create_Cards("VEHICLE DELIVERY", VehicleDel, IF.get_gradient_color(VehicleDel       ))),
        dbc.Col(IF.Create_Cards("FACILITY", Facility, IF.get_gradient_color(Facility       ))),
        dbc.Col(IF.Create_Cards("OVERALL IMPRESSION", OverallImpression, IF.get_gradient_color(OverallImpression))),
        dbc.Col(IF.Create_Cards("OVERALL SCORE", OverallScore, IF.get_gradient_color(OverallScore     ))),
        
    ]

    def get_chart_data(columns):
        values = df_filtered[columns].mean().round(1).fillna(0)
        return values.tolist()

    # Data for the horizontal bar charts
    categories_1 = ['iQ1a',	'iQ1b',	'iQ1c',	'iQ1d',	'iQ1d1',	'iQ1d2',	'iQ1e_1',	'iQ1f',]
    values_1 = get_chart_data(categories_1)
    categories_2 = ['iQ2a',	'iQ2b',	'iQ2c',	'iQ2d',	'iQ2e',	'iQ2f',	'iQ2g',]
    values_2 = get_chart_data(categories_2)
    categories_3 = ['iQ3c',	'iQ3d',	'iQ3e',]
    values_3 = get_chart_data(categories_3)
    categories_4 = ['iQ4b',	'iQ4c',	'iQ4d',	'iQ4g',	'iQ4h',]
    values_4 = get_chart_data(categories_4)
    categories_5 = ['iQ4b',	'iQ4c',	'iQ4d',	'iQ4g',	'iQ4h',]
    values_5 = get_chart_data(categories_5)
    categories_6 = ['iQ5_2',	'iQ5_3',	'iQ5_4',	'iQ5_5',	'iQ5_6',	'iQ5_7',	'iQ5_8',	'iQ5_9']
    values_6 = get_chart_data(categories_6)
    categories_7 = ['iQ6_1',	'iQ6_2',	'iQ6_3',	'iQ6_4',]
    values_7 = get_chart_data(categories_7)
    categories_8 = ['iQ7_1',	'iQ7_2',	'iQ7_3',	'iQ7_4',	'iQ7_5',]
    values_8 = get_chart_data(categories_8)



    # Update charts with filtered data
    chart1 = IF.create_horizontal_bar_chart(categories_1, values_1,title='INITIAL')
    chart2 = IF.create_horizontal_bar_chart(categories_2, values_2,title='SERVICE ADVISOR')
    chart3 = IF.create_horizontal_bar_chart(categories_3, values_3,title='SALES CONSULTANT')
    chart4 = IF.create_horizontal_bar_chart(categories_4, values_4,title='SERVICING TIME')
    chart5 = IF.create_horizontal_bar_chart(categories_5, values_5,title='VEHICLE DELIVERY')
    chart6 = IF.create_horizontal_bar_chart(categories_6, values_6,title='FACILITY')
    chart7 = IF.create_horizontal_bar_chart(categories_7, values_7,title='OVERALL IMPRESSION')
    chart8 = IF.create_horizontal_bar_chart(categories_8, values_8,title='OVERALL SCORE')
    
    Base = f"Base: {len(df_filtered)}"
    return Base,dbc.Row(cards), chart1,chart2,chart3,chart4,chart5,chart6,chart7,chart8
        
