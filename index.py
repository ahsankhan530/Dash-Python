import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import csv


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

@app.route('/e',methods=['POST'])
def index():
    data=request.get_json()
    a=dreamer(Ref=data["Ref"],Month=data['Month'],Date=data["Date"],Amount=data["Amount"],Detailed_Category=data['Detailed_Category'],
    subcategory=data['subcategory'], Ad=data['Ad'],Paid=data['Paid'],Settled=data['Settled'],FIELD2=data['FIELD2'])
    db.session.add(a)
    db.session.commit()
   
    return 'ok'
@app.route('/reports',methods=['POST','GET'])
def add():
   
    global a
    add.a= dreamer.query.filter_by().all()
    db.session.commit() 
    # for i in a:
    #     global df
    #     add.df=pd.Series([i.Amount,i.Month])
       
    return 'df'
add()
# print(add.df)
# df=add.df
dash_app2 = Dash(__name__, server = app)

# print(add.a)
li=[]
ai=[]
for i in add.a:
    # df=pd.Series([i.Amount,i.Month])
    # a=df
    li.append(i.Month)
    ai.append(i.Amount)
ap={'a':li,'pi':ai}
df=pd.DataFrame(ap)
y=df['a']
x=df['pi']



dash_app2.layout= html.Div(children=[
    html.H1(children='Data '),
    dcc.Graph(
    id='example',animate=True,
    figure={
        
            'data': [
                
                {'x':y,'y':x,'type':'bar'}
            ],
            'layout': {
                'title': 'Month and Amount'
            }
        }
    )
])   

app = DispatcherMiddleware(app, {
    '/dash2': dash_app2.server
})

run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=True)
