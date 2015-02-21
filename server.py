from flask import *

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from htmlmin import minify

app = Flask(__name__)

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/makeuser', methods=['GET'])
def makeuser():
    admin = User('admin', 'admin@example.com')
    db.session.add(admin)
    db.session.commit()
    return "True"

@app.route('/getuser', methods=['GET'])
def getuser():
    admin = User.query.filter_by(username='admin').first()
    return admin.username

@app.route('/', methods=['GET'])
def hello():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(host="0.0.0")
