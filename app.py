from validate_email import validate_email
import smtplib
from flask import Flask, request, render_template,redirect,url_for,jsonify
from email.mime.text import MIMEText
from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient('mongodb+srv://maulanasyakhiya:X6Tx5vkB5TZUiCMo@cluster0.zsgjrxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', serverSelectionTimeoutMS = 500)
db = client.portofolio

app = Flask(__name__)



@app.route('/')
def index():
    return redirect(url_for('home', lang='id'))

@app.route('/home')
def home():
    lang = request.args.get('lang')
    if (lang == 'id'):
        return render_template(f'index/index-{lang}.html')
    elif(lang == 'en'):
        return render_template(f'index/index-{lang}.html')
    else:
        return render_template('index/index-id.html')

@app.route('/sendMessage' , methods = ['POST'])
def sendMessage():
    receiver = 'maulana.syakhiya@gmail.com'
    email_from = request.form.get('email') 
    subject = request.form.get('subject') 
    msgTxt = request.form.get('msgTxt') 
    lang = request.form.get('lang') 

    text = f"""\
    From: {email_from}
    {msgTxt}
    """
    
    message = MIMEText(text, "plain")
    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = receiver

    if validate_email(email_from):
        delete_expired_data()
        if (db.emailMessage.find_one({'email' : email_from})) :
            return jsonify({
                'result':'anda telah mengirim pesan'
            })
        else:
            
            insert_data(email_from)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('maulana.syakhiya@gmail.com', 'pklrjwgablthpevu')
                server.sendmail(email_from, receiver, message.as_string())

            if (lang =='en'):
                return jsonify({
                    'result':'success',
                    'msg':f'Your massage from {email_from} has been send'
                })
            else:
                return jsonify({
                    'result':'berhasil',
                    'msg':f'Pesan dari {email_from} telah terkirim '
                })
            
    else:
        return jsonify({
                'result':'email invalid'
            })

def insert_data(email_from):
    waktu_sekarang = datetime.now()
    data = {
        "email": email_from,
        "date": waktu_sekarang
    }
    db.emailMessage.insert_one(data)

def delete_expired_data():
    waktu_sekarang = datetime.now()
    batas_waktu = waktu_sekarang - timedelta(hours=3)
    db.emailMessage.delete_many({'date': {'$lt': batas_waktu}})

if __name__ == '__main__':
    app.run(debug=True)