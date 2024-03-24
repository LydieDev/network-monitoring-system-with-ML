from flask import Flask, render_template, url_for
from links import my_blueprint

app = Flask(__name__)

app.register_blueprint(my_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
