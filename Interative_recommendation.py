import dash
from dash import html
from dash import dcc
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
data = pd.read_csv('property_evaluation.csv')
app = dash.Dash(suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Define your preference"),

    html.H3(
        id='Desciption_text_similarity',
        children=[
            'Weight for text similarity '
        ]
    ),
    dcc.Input(
        id='text_similarity_weight',
        placeholder='text_similarity_weight',
        type='number',
        value=1.0,
    ),
    html.Br(),
    html.H3(
        id='crime_per_1000_residents',
        children=[
            'Weight for crime_per_1000_residents '
        ]
    ),
    dcc.Input(
        id='crime_per_1000_residents_weight',
        placeholder='crime_per_1000_residents_weight',
        type='number',
        value=1.0,
    ),
    html.Br(),
    html.Br(),
    html.Div(id='result')
    ])


@app.callback(
    Output('result', 'children'),
    [Input('text_similarity_weight', 'value'),
     Input('crime_per_1000_residents_weight', 'value')]
)
def update_result(text_similarity_weight, crime_per_1000_residents_weight):
    data['property_score'] = data['text_similarity']*text_similarity_weight\
                             - data['crime_per_1000_residents']*crime_per_1000_residents_weight
    top_indices = data['property_score'].argsort()[::-1][0:5]
    recommended_homes_1 = list(data.iloc[top_indices]['link'])[0]
    address_1 = list(data.iloc[top_indices]['address'])[0]
    recommended_homes_2 = list(data.iloc[top_indices]['link'])[1]
    address_2 = list(data.iloc[top_indices]['address'])[1]
    recommended_homes_3 = list(data.iloc[top_indices]['link'])[2]
    address_3 = list(data.iloc[top_indices]['address'])[2]
    #html.A("Link to external site", href='https://plot.ly', target="_blank")
    return [html.A("Your 1st recommendation", href=recommended_homes_1, target="_blank"),
            html.H4(
                id='1st_Address',
                children=[
                    'Address: ' + address_1
                ]
            ),
            html.Br(),
            html.A("Your 2nd recommendation", href=recommended_homes_2, target="_blank"),
            html.H4(
                id='2nd_Address',
                children=[
                    'Address: ' + address_2
                ]
            ),
            html.Br(),
            html.A("Your 3rd recommendation", href=recommended_homes_3, target="_blank"),
            html.H4(
                id='3rd_Address',
                children=[
                    'Address: ' + address_3
                ]
            )
            ]
    #"The links are: {}".format(recommended_homes)

#@app.callback(Output('location', 'href'),
#              Input('result', 'clickData'),
#              prevent_initial_call=True)
#def redirect_to_url(clickData):
    # do something with clickData
#    url = 'https:www.example.com'
#    return url

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug = False, dev_tools_ui = False, dev_tools_props_check = False)