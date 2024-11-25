import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import Input_Data as ID
import Input_Function as IF
import openai  # For generating insights

from config import box_shadow
from config import pill_style
from config import chart_bg_space_style


dash.register_page(__name__, path="/")

# Sales DataFrame
df_sales = ID.S_ovr_df

# After Sales DataFrame
df_aftersales = ID.AS_ovr_df

# Brand and City Dictionaries
Eval_Brand_Dict = {1: 'Hyundai', 2: 'Toyota', 3: 'Nissan', 4: 'Ford', 5: 'Lincoln', 6: 'MG', 7: 'Cherry', 8: 'KIA'}
df_sales['Eval_Brand_Text'] = df_sales['BRND_DASH'].map(Eval_Brand_Dict)
df_aftersales['Eval_Brand_Text'] = df_aftersales['BRND_DASH'].map(Eval_Brand_Dict)

City_Dict = {1: 'Riyadh', 2: 'Jeddah', 3: 'Dammam'}
df_sales['City_Text'] = df_sales['CITY'].map(City_Dict)
df_aftersales['City_Text'] = df_aftersales['CITY'].map(City_Dict)



# Function to generate insights using the updated OpenAI API
def generate_insights(sales_data, aftersales_data):
    '''prompt = f"""
    Sales data: {sales_data.to_dict()}
    After Sales data: {aftersales_data.to_dict()}
    
    Based on the above data, please provide key insights and recommendations about the performance of the sales and aftersales touchpoints.
    """
    
    # Using the new openai.ChatCompletion API for GPT-based models
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4", depending on your access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates insights from sales and aftersales data."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the generated insights from the response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating insights: {e}" '''
    return "Work in Progress"

# Layout (Base will be updated by callback)
layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Select Evaluation Brand:"),
                dcc.Dropdown(id='sales-eval-brand-dropdown', options=ID.Eval_Brand_DropDown_List, value=0, placeholder="Select Evaluation Brand")
            ]),
            dbc.Col([
                html.Label("Select City:"),
                dcc.Dropdown(id='sales-city-dropdown', options=ID.City_DropDown_List, value=0, placeholder="Select City")
            ])
        ])
    ]),

    # Sales Section
    html.H3("Sales Overall Score"),
    html.Div(html.H4(id="sales-base-display"),style=pill_style),
    html.Div(id="sales-card-container", style={"margin-top": "20px"}),  # Sales overall score cards

    html.Hr(),

    # After Sales Section
    html.H3("After Sales Overall Score"),
    html.Div(html.H4(id="aftersales-base-display"),style=pill_style),
    html.Div(id="aftersales-card-container", style={"margin-top": "20px"}),  # After sales overall score cards

    html.Hr(),

    # AI-Generated Insights Section
    html.H3("AI-Generated Insights"),
    html.P(id="ai-insights-display", style={"margin-top": "20px"}),  # Display AI-generated insights

], fluid=True)

# Callback to update Sales, After Sales, and AI insights
@callback(
    [Output('sales-base-display', 'children'),
     Output('sales-card-container', 'children'),
     Output('aftersales-base-display', 'children'),
     Output('aftersales-card-container', 'children'),
     Output('ai-insights-display', 'children')],
    [Input('sales-eval-brand-dropdown', 'value'),
     Input('sales-city-dropdown', 'value')]
)
def update_sales_and_aftersales_cards(eval_brand, city):
    # ---- Sales Data Filtering ----
    df_sales_filtered = df_sales.copy()
    if eval_brand != 0:
        df_sales_filtered = df_sales_filtered[df_sales_filtered['BRND_DASH'] == eval_brand]
    
    if city != 0:
        df_sales_filtered = df_sales_filtered[df_sales_filtered['CITY'] == city]

    # ---- After Sales Data Filtering ----
    df_aftersales_filtered = df_aftersales.copy()
    if eval_brand != 0:
        df_aftersales_filtered = df_aftersales_filtered[df_aftersales_filtered['BRND_DASH'] == eval_brand]
    
    if city != 0:
        df_aftersales_filtered = df_aftersales_filtered[df_aftersales_filtered['CITY'] == city]

    # ---- Sales Data ----
    df_sales_filtered['Touchpoint_Text'] = df_sales_filtered['TOUCHPOINT'].map({1: 'Branch', 2: 'Call Center', 3: 'Online', 4: 'SM', 5: 'Website'})
    df_sales_mean = df_sales_filtered.groupby('Touchpoint_Text')['OVERALL_SCORE'].mean().round(1).fillna(0)

    # Extract Sales Scores
    Branch_Score = df_sales_mean.get('Branch', 0)
    CallCenter_Score = df_sales_mean.get('Call Center', 0)
    Online_Score = df_sales_mean.get('Online', 0)
    SM_Score = df_sales_mean.get('SM', 0)
    Website_Score = df_sales_mean.get('Website', 0)

    # Create Sales cards
    sales_cards = [
        dbc.Col(IF.Create_Cards("BRANCH", Branch_Score, IF.get_gradient_color(Branch_Score))),
        dbc.Col(IF.Create_Cards("CALL CENTER", CallCenter_Score, IF.get_gradient_color(CallCenter_Score))),
        dbc.Col(IF.Create_Cards("ONLINE", Online_Score, IF.get_gradient_color(Online_Score))),
        dbc.Col(IF.Create_Cards("SM", SM_Score, IF.get_gradient_color(SM_Score))),
        dbc.Col(IF.Create_Cards("WEBSITE", Website_Score, IF.get_gradient_color(Website_Score)))
    ]
    sales_base = f"Base : {len(df_sales_filtered)}"

    # ---- After Sales Data ----
    df_aftersales_filtered['Touchpoint_Text'] = df_aftersales_filtered['TOUCHPOINT'].map({1: 'Service Center', 2: 'Call Center', 3: 'Online', 4: 'SM', 5: 'Website'})
    df_aftersales_mean = df_aftersales_filtered.groupby('Touchpoint_Text')['OVERALL_SCORE'].mean().round(1).fillna(0)

    # Extract After Sales Scores
    ServiceCenter_Score = df_aftersales_mean.get('Service Center', 0)
    AfterSalesCallCenter_Score = df_aftersales_mean.get('Call Center', 0)
    AfterSalesOnline_Score = df_aftersales_mean.get('Online', 0)
    AfterSalesSM_Score = df_aftersales_mean.get('SM', 0)
    AfterSalesWebsite_Score = df_aftersales_mean.get('Website', 0)

    # Create After Sales cards
    aftersales_cards = [
        dbc.Col(IF.Create_Cards("SERVICE CENTER", ServiceCenter_Score, IF.get_gradient_color(ServiceCenter_Score))),
        dbc.Col(IF.Create_Cards("CALL CENTER", AfterSalesCallCenter_Score, IF.get_gradient_color(AfterSalesCallCenter_Score))),
        dbc.Col(IF.Create_Cards("ONLINE", AfterSalesOnline_Score, IF.get_gradient_color(AfterSalesOnline_Score))),
        dbc.Col(IF.Create_Cards("SM", AfterSalesSM_Score, IF.get_gradient_color(AfterSalesSM_Score))),
        dbc.Col(IF.Create_Cards("WEBSITE", AfterSalesWebsite_Score, IF.get_gradient_color(AfterSalesWebsite_Score)))
    ]
    aftersales_base = f"Base : {len(df_aftersales_filtered)}"

    # ---- AI-Generated Insights ----
    ai_insights = generate_insights(df_sales_filtered, df_aftersales_filtered)

    # Return values for both Sales and After Sales, plus AI insights
    return [sales_base, dbc.Row(sales_cards), aftersales_base, dbc.Row(aftersales_cards), ai_insights]
