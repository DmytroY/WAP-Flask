from flask import Flask, render_template, url_for, redirect, session
from flask_session import Session
from authlib.integrations.flask_client import OAuth
from secret_configs import Config


app = Flask(__name__)
oauth = OAuth(app)
app.secret_key = Config.SECRET_KEY

@app.route("/")
def index():
    name = session.get('user_name')
    return render_template('index.html', name=name)
    
@app.route("/google")
def google():

    # Google Oauth Config
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(name='google',
                client_id=Config.GOOGLE_CLIENT_ID,
                client_secret=Config.GOOGLE_CLIENT_SECRET,
                server_metadata_url=CONF_URL,
                client_kwargs={'scope': 'openid email profile'} )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    session['user_email'] = token['userinfo']['email']
    session['user_name'] = token['userinfo']['name']
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_name')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)