import pandas as pd

Eval_Brand_DropDown_List = [
    {"label": "Overall NYNM", "value": 0},
    {"label": "Hyundai", "value": 1},
    {"label": "Ford", "value": 4},
    {"label": "Lincoln", "value": 5},
    {"label": "MG", "value": 6},
    {"label": "Cherry", "value": 7}
]

City_DropDown_List = [
    {"label": "Overall", "value": 0},
    {"label": "Riyadh", "value": 1},
    {"label": "Jeddah", "value": 2},
    {"label": "Dammam", "value": 3},
]


# Load CSV
S_ovr_df = pd.read_csv(r"SALES CSV.csv", index_col=False)
S_ovr_df = S_ovr_df.apply(pd.to_numeric, errors='coerce')

AS_ovr_df = pd.read_csv(r"AFTERSALES CSV.csv", index_col=False)
AS_ovr_df = AS_ovr_df.apply(pd.to_numeric, errors='coerce')


S_br_df = pd.read_csv(r"Sales_Branch_Evaluation CSV.csv", index_col=False)
S_br_df = S_br_df.apply(pd.to_numeric, errors='coerce')

S_cc_df = pd.read_csv(r"Sales_Call_Centre CSV.csv", index_col=False)
S_cc_df = S_cc_df.apply(pd.to_numeric, errors='coerce')

S_wb_df = pd.read_csv(r"Sales_Website CSV.csv", index_col=False)
S_wb_df = S_wb_df.apply(pd.to_numeric, errors='coerce')

S_on_df = pd.read_csv(r"Sales_Online_Search CSV.csv", index_col=False)
S_on_df = S_on_df.apply(pd.to_numeric, errors='coerce')

S_sm_df = pd.read_csv(r"Sales_SM CSV.csv", index_col=False)
S_sm_df = S_sm_df.apply(pd.to_numeric, errors='coerce')

AS_cc_df = pd.read_csv(r"AFTERSALES_CALL_CENTRE CSV.csv", index_col=False)
AS_cc_df = AS_cc_df.apply(pd.to_numeric, errors='coerce')

AS_on_df = pd.read_csv(r"AFTERSALES_ONLINE_SEARCH CSV.csv", index_col=False)
AS_on_df = AS_on_df.apply(pd.to_numeric, errors='coerce')

AS_sc_df = pd.read_csv(r"AFTERSALES_SERVICE_CENTRE CSV.csv", index_col=False)
AS_sc_df = AS_sc_df.apply(pd.to_numeric, errors='coerce')

AS_sm_df = pd.read_csv(r"AFTERSALES_SM CSV.csv", index_col=False)
AS_sm_df = AS_sm_df.apply(pd.to_numeric, errors='coerce')

AS_wb_df = pd.read_csv(r"AFTERSALES_WEBSITE CSV.csv", index_col=False)
AS_wb_df = AS_wb_df.apply(pd.to_numeric, errors='coerce')
