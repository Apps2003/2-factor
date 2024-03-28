import json
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from random import randint

app = Flask(__name__)

# Load email configuration from config.json
with open('config.json', 'r') as f:
    params = json.load(f)['params']

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['gmail-user']  # Correct the key name
app.config['MAIL_PASSWORD'] = params['gmail-password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initialize Flask-Mail
mail = Mail(app)

# Generate OTP
otp = randint(1000, 9999)  # Ensure OTP is 4 digits


@app.route("/")
def index():
    return render_template('email.html', msg="")


@app.route('/verify', methods=["POST"])
def verify():
    # Get email address from form
    gmail = request.form['email']

    # Create and send email message with OTP
    msg = Message('OTP', sender='add-email', recipients=[gmail])
    msg.body = str(otp)
    mail.send(msg)

    return render_template("verify.html")


@app.route('/validate', methods=["POST"])
def validate():
    userotp = request.form['otp']
    if otp == int(userotp):
        return "Email Verified successfully"
    return render_template('email.html', msg='Not verified!')


if __name__ == '__main__':
    app.run(debug=True)
