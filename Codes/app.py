from bs4 import BeautifulSoup
import lxml
import time
from flask import Flask , render_template

app = Flask(__name__)

def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
        function()
    return wrapper_function


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ball_bearing.html")
def say_bye():
    return render_template("ball_bearing.html")


if __name__ == "__main__":
    app.run(debug=True)


# class User:
#     def __init__(self, name):
#         self.name = name
#         self.is_logged_in = False

# def is_authenticated_decorator(function):
#     def wrapper(*args, **kwargs):
#         if args[0].is_logged_in == True:
#             function(args[0])
#     return wrapper

# @is_authenticated_decorator
# def create_blog_post(user):
#     print(f"This is {user.name}'s new blog post.")

# new_user = User("angela")
# new_user.is_logged_in = True
# create_blog_post(new_user)