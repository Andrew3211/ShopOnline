from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    seller = db.Column(db.String(35), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


@app.route("/")
def index():
    item = Item.query.order_by(Item.price).all()
    return render_template("index.html", item=item)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        price = request.form["price"]
        seller = request.form["seller"]

        item = Item(title=title, price=price, seller=seller)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении товара произошла ошибка!'
    else:
        return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
