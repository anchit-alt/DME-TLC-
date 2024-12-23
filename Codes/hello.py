from bs4 import BeautifulSoup
import lxml
from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world():
    return "HELO"

hello_world()