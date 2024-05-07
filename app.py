from validate_email import validate_email
import smtplib
from flask import Flask, request, render_template,redirect,url_for,jsonify
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from database.database import  connect_to_mysql,insert_data_db,data_search_email,delete_expired_data

conn = connect_to_mysql(
    host='localhost',
    username='root',
    password='',
    database='test'
)


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
        delete_expired_data(connection=conn)
        if (data_search_email(connection=conn,data=email_from,table='message')) :
            return jsonify({
                'result':'anda telah mengirim pesan'
            })
        else:
            
            insert_data(email_from,msgTxt)

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

def insert_data(email_from,msgTxt):
    waktu_sekarang = datetime.now()
    data = [(
        email_from,
        waktu_sekarang,
        msgTxt
    )]
    insert_data_db(connection=conn, table='message', data=data)



if __name__ == '__main__':
    app.run(debug=True)