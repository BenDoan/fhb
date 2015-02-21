from flask import *

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from htmlmin import minify
from flask.ext.login import LoginManager,login_user,logout_user
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
loginmanager = LoginManager()
loginmanager.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/fhb.db'

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

assets = Environment(app)
assets.url_expire = False

css = Bundle('css/main.css', 'css/bootstrap.css', 'css/bootstrap-theme.css', filters="cssmin", output='css/gen/packed.css')
assets.register('css_all', css)

js = Bundle("js/vendor/jquery-1.11.2.min.js", "js/vendor/modernizr-2.8.3.min.js", 'js/bootstrap.js', 'js/main.js', filters="jsmin", output='js/gen/packed.js')
assets.register('js_all', js)

db = SQLAlchemy(app)

class LoginForm(Form):
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean())

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.authenticated = False

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self) :
        print(self.email)
        return self.authenticated

    def is_active(self) :
        return self.is_authenticated()

    def is_anonymous(self) :
        return False

    def get_id(self) :
        return self.email

@loginmanager.user_loader
def load_user(userid):
    users =  User.query.filter_by(email=userid)
    return users.first()

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = User.query.filter_by(username = request.form["name"])
        user = users.first()
        if user != None :
            if pbkdf2_sha256.verify(request.form["password"],user.password) :
                user.authenticated = True
                db.session.commit()
                login_user(user)
    return redirect(request.form["redirect"])

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(request.args.get("redirect"))

@app.route('/makeuser', methods=['GET'])
def makeuser():
    admin = User('admin', 'admin@example.com')
    admin.password = pbkdf2_sha256.encrypt("password")
    db.session.add(admin)
    db.session.commit()
    return "True"

@app.route('/getuser', methods=['GET'])
def getuser():
    admin = User.query.filter_by(username='admin').first()
    return admin.username

@app.route('/', methods=['GET','POST'])
def hello():
    return render_template('index.html',form=LoginForm())

app.secret_key = "Secret"

if __name__ == "__main__":
    app.run(host="0.0.0")
