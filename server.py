from flask import *


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0")
