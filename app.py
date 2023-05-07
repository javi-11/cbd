from flask import Flask, redirect
from views import views


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

@app.route("/")
def red():
    return redirect("/views")


if __name__=='__main__':
    app.run(debug=True)
