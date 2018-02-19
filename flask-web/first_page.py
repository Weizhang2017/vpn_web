from flask import Flask, send_file, render_template, request, session, flash, request, abort
#from flask_mail import Mail, Message
from email.message import EmailMessage
from email.headerregistry import Address
import smtplib
import os

app = Flask(__name__,template_folder='template')
'''
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'zdsangw1.2011@gmail.com'
app.config['MAIL_PASSWORD'] = 'w34874'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
'''

@app.route('/')
def vpn_intro():
	return render_template('main_page.html')

@app.route('/client102.ovpn')
def download_client_file():
	return send_file('/home/wei/vpn_web/download/client102.ovpn')

@app.route('/openvpn_client.apk')
def download_android_client():
	return send_file('/home/wei/vpn_web/download/openvpn_client.apk')

@app.route('/openvpn_windows.zip')
def download_windows_client():
	return send_file('/home/wei/vpn_web/download/openvpn_windows.zip')

@app.route('/Tunnelblick.dmg')
def download_macos_client():
	return send_file('/home/wei/vpn_web/download/Tunnelblick.dmg')

@app.route('/send_message',methods=['POST'])
def send_message():
	req = request.form
	content = 'Email:%s. Message:%s. Name:%s' %(req['Email'],req['Message'],req['Name'])
	msg = EmailMessage()
	msg['Subject'] = 'New Request'
	msg['From'] = Address('vpn request','vpn.req@gmail.com')
	msg['To'] = Address('vpn request','vpn.req@gmail.com')
	msg.set_content(content)
	with smtplib.SMTP('smtp.gmail.com:587') as s:
		s.ehlo()
		s.starttls()
		s.login('vpn.req@gmail.com','vpngroup')
		s.send_message(msg)
#	msg = Message('New Request',sender = 'vpn.req@gmail.com',recipients = ['vpn.req@gmail.com'])
#	msg.body = message
#	mail.send(msg)
	return 'We have received your request and will get back to you soon.'

@app.route('/login_main')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

'''
if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=5000, debug=True)
'''
