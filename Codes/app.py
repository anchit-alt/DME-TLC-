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
    return render_template("website.html")


@app.route("/<name>")
def say_bye(name):
    return f"hi {name}  "


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