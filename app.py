from matplotlib import pyplot as plt
import dash
from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app=Flask(__name__)
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
@app.route('/ss',methods=['POST'])
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
@app.route('/',methods=['POST','GET'])
def add():
    i= dreamer.query.filter_by(id=1).first()
    db.session.commit()
    df=pd.Series([i.Ref,i.Month,i.Date,i.Amount,i.category,i.subcategory,i.Detailed_Category,i.Ad,i.Paid,i.Settled,i.FIELD2])
    x=df[0]
    y=df[1]
    plt.plot(data=df)
    
    plt.show()
    print(x,y)
    
    return 'ok'
#     for i,v in g:
#          a=dd(text=i,complete=v)
#          db.session.add(a)
#          db.session.commit()

     
    # wks.append_row([a.text])
    # db.session.add(a)
    # db.session.commit()
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)