from flask import Flask
from flask_cors import CORS
from Routes.Interpreter import router

app = Flask(__name__)
CORS(app)

app.register_blueprint(router, url_prefix='/interpreter')

@app.route('/')
def hello_world():
    return 'Hola mundo'

if __name__ == '__main__':
    app.run(debug=True, port=3000)