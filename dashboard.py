import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from datetime import date
import sqlite3
import random 
import dash_table
import pandas 
import dash_bootstrap_components as dbc 
import time
import json 
import pdb

stks = open('stk.json', 'r')
maps = json.load(stks)

queries = open('queries.txt', 'w+')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

fields = { 
    #"Symbol": "text",
    "Stock": "text",
    "Price": "number",
    "Units": "number"
}

app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(
            [dcc.RadioItems(id='checklist', 
                    options=[{"label": "Buy", "value": 'buy'}, {'label': 'Sell', 'value': 'sell'}], 
                    labelStyle={"display": "inline-block"}
                    )
    ], width=4 )
    ),
    dbc.Row( 
        dbc.Col(dcc.Dropdown(id='input_Stock', options=[{'label': i, 'value': i} for i in maps.values()]), width=2)
    ),
    # dbc.Row(
    #     dbc.Col(dcc.Input(id='input_Stockname', type='text', placeholder='input Stockname'), width=2)
    # ),
    dbc.Row(
        dbc.Col(dcc.Input(id='input_Price', type='number', placeholder='input Price') , width=2)
    ),
    dbc.Row(
        dbc.Col(dcc.Input(id='input_Units', type='number', placeholder='input Units'), width=2)
    ),
    dbc.Row(
        dbc.Col(
            [dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2075, 12, 31),
        initial_visible_month=date(2021, 1, 1)
    )]
    , width=2   )
    ),
    dbc.Row(
        dbc.Col(html.Button(id='submit-button',n_clicks=0, children='Submit'),width=2)
    ),
    dbc.Row(
        dbc.Col(html.Div(id="out-all-types"), width=2)
    ),
    dbc.Row(
        dbc.Col(html.Div(id='tableloc'))
    )


])


@app.callback(
    Output("out-all-types", "children"),
    Input('submit-button', 'n_clicks'),
    State('checklist', 'value'), 
    [State("input_{}".format(k), "value") for k in fields.keys()],
    State('my-date-picker-single', 'date')
)
def enterdata(n_clicks, buy_sell, input_Stock, input_Price, input_Units, date):
    '''
    Enter or remove data in the database based on the inputs
    '''
    print(buy_sell, input_Stock)
    connection = sqlite3.connect("portfolio.db")
    if buy_sell == None and n_clicks != 0:
        return 'Please select type of transaction'
    with connection as conn:  
        #if buy_sell == 'buy': 
        
        try:
#                print("Are we here?")
#                print("Connectionname: ", connection)
            ## Perform a check on the number of units being sold
            if buy_sell == 'sell':
                df = pandas.read_sql_query("SELECT * from PORTFOLIO", conn)
                if df.groupby(input_Stock).sum('UNITS') < input_Units:
                    return 'Check the number of units being sold'
            query = '''INSERT INTO PORTFOLIO(ID, STOCKNAME, UNITS, PRICE, DATE, TRANSACTIONTYPE)
                        VALUES({id}, '{stockname}', {units}, {price}, '{dates}', '{ttype}')'''.format(id=[y for y,z in maps.items() if z == input_Stock][0], 
                                stockname=input_Stock, price=input_Price, units=input_Units, dates=date, ttype=buy_sell) 
            conn.execute(query)
            conn.commit()
            queries.write(query)
            return "Value inserted"
        except Exception as e: 
            pdb.set_trace()
            print( "does it make exception? ", e )
            return
        #if buy_sell =='sell': 
        #    return 'We are still working on this'

@app.callback(
    Output('tableloc', 'children'),
    [Input('submit-button', 'n_clicks')]
)
def data_table(n_clicks):
    time.sleep(2)

    connection = sqlite3.connect("portfolio.db")
    with connection as conn2: 
        df = pandas.read_sql_query("SELECT * from PORTFOLIO", conn2)
        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict('records')
        #conn.close()
    return dash_table.DataTable(id='tables', columns=columns, data=data)


if __name__ == "__main__":
    app.run_server(debug=True)