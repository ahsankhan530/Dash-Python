import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import csv

# app =dash.Dash()

# if __name__ == '__main__':
#     app.run_server(debug=True)
from flask import Flask,redirect,url_for,request
import flask
from werkzeug.serving import run_simple
import dash_html_components as html
from dash import Dash
from werkzeug.wsgi import DispatcherMiddleware
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'dE\xad2g\x0c\x8d\xb9\x1cq\x86\x04:\xa8>\xc7\xc5\xc2Dr\xe7f\xf9\xeb'


dash_app1 = Dash(__name__, server = app)
df=pd.read_csv('a.csv')
df.columns=['a','b']
x=df['a']
y=df['b']
dash_app2 = Dash(__name__, server = app, url_base_pathname='/reports/')
dash_app1.layout = html.Div(
    children=[
        html.Div(
            className="container",
            children=[
                dcc.Location(id='url_login', refresh=True),
                html.Div('''Please log in to continue:''', id='h1'),
                html.Div(
                    # method='Post',
                    children=[
                        dcc.Input(
                            placeholder='Enter your username',
                            type='text',
                            id='uname-box'
                        ),
                        dcc.Input(
                            placeholder='Enter your password',
                            type='password',
                            id='pwd-box'
                        ),
                        html.Button(
                            children='Login',
                            n_clicks=0,
                            type='submit',
                            id='login-button'
                        ),
                        html.Div(children='', id='output-state')
                    ]
                ),
            ]
        )
    ]
)

dash_app2.layout= html.Div(children=[
    html.H1(children='Data visualization'),
    dcc.Graph(
    id='example',
    figure={
        
            'data': [
                
                {'x':x,'y':y,'type':'bar'}
            ],
            'layout': {
                'title': 'Dreamer'
            }
        }
    )
])
db = SQLAlchemy(app)

class dreamer(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     Ref = db.Column(db.String(200))
     Month = db.Column(db.String)
     Date = db.Column(db.String)
     Amount = db.Column(db.String)
     category = db.Column(db.String)
     subcategory = db.Column(db.String)
     Detailed_Category = db.Column(db.String)
     Ad= db.Column(db.String)
     Paid= db.Column(db.String)
     Settled = db.Column(db.String)
     FIELD2 = db.Column(db.String)
x=0
y=0
@app.route('/',methods=['POST'])
def index():
    data=request.get_json()
#     scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#     credationals=ServiceAccountCredentials.from_json_keyfile_name('placeapi-a3c5e000d8e2.json',scope)
#     gc=gspread.authorize(credationals)
#     wks=gc.open('ahsan').sheet1
#     g=wks.get_all_values()
    
    a=dreamer(Ref=data["Ref"],Month=data['Month'],Date=data["Date"],Amount=data["Amount"],Detailed_Category=data['Detailed_Category'],
    subcategory=data['subcategory'], Ad=data['Ad'],Paid=data['Paid'],Settled=data['Settled'],FIELD2=data['FIELD2'])
    db.session.add(a)
    db.session.commit()
    
    return 'ok'
@app.route('/aa',methods=['POST','GET'])
def add():
    f = open("a.csv", "w")
    f.truncate()
    f.close()
    a= dreamer.query.filter_by().all()
    
    db.session.commit() 
    for i in a:
        df=pd.Series([i.Date,i.Month])
        with open('a.csv','a')as f:
            writer = csv.writer(f)
            writer.writerow(df)
#     f.close()
        print(df)
        
        # df=pd.Series([i.Ref,i.Month,i.Date,i.Amount,i.category,i.subcategory,i.Detailed_Category,i.Ad,i.Paid,i.Settled,i.FIELD2])
    # x=df[0]
    # y=df[1]
    return 'ok'
    # return flask.redirect('/reports')
    # df=pd.Series([i.Ref,i.Month,i.Date,i.Amount,i.category,i.subcategory,i.Detailed_Category,i.Ad,i.Paid,i.Settled,i.FIELD2])
   
     
# @app.route('/reports')
# def render_reports():
#     return flask.redirect('/dash2')

app = DispatcherMiddleware(app, {
    '/dash1': dash_app1.server,
    '/dash2': dash_app2.server
})

db.create_all()
run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=True)