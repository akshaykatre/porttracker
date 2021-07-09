import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from datetime import date
import sqlite3
import random 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

fields = { 
    "Symbol": "text",
    "Stockname": "text",
    "Price": "number",
    "Units": "number"
}

app.layout = html.Div(style={'width':'10%', 'height':'100%','float':'left'},
    children =
    # [
    #     dcc.Input(id="input_{}".format(k), type=v, placeholder="input {}".format(k))
    #     for k,v in zip(fields.keys(), fields.values())
    # ]
    [ dcc.Input(id='input_Symbol', type='text', placeholder='input Symbol'),
      dcc.Input(id='input_Stockname', type='text', placeholder='input Stockname'),
      dcc.Input(id='input_Price', type='number', placeholder='input Price') ,
      dcc.Input(id='input_Units', type='number', placeholder='input Units') ,
    ]
    + [dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2075, 12, 31),
        initial_visible_month=date(2021, 1, 1)
    )]
    + [html.Button(id='submit-button',n_clicks=0, children='Submit')]
    + [html.Div(id="out-all-types")]
)


@app.callback(
    Output("out-all-types", "children"),
    Input('submit-button', 'n_clicks'),
    [State("input_{}".format(k), "value") for k in fields.keys()],
    State('my-date-picker-single', 'date')
)
def cb_render(n_clicks, input_Symbol, input_Stockname, input_Price, input_Units, date):
    try:
        conn = sqlite3.connect("portfolio.db")
        conn.execute('''INSERT INTO PORTFOLIO(ID, SYMBOL, STOCKNAME, UNITS, PRICE, DATE)
                    VALUES({id}, '{symbol}', '{stockname}', {units}, {price}, '{dates}')'''.format(id=random.randint(0, 1000000) , 
                            symbol=input_Symbol, stockname=input_Stockname, price=input_Price, units=input_Units, dates=date))
        conn.commit()
        conn.close()
        return "Value inserted"
    except Exception as e: 
        pass



if __name__ == "__main__":
    app.run_server(debug=True)