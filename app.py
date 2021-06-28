from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    savefile = db.Column(db.String(144), unique=False)

    def __init__(self, username, savefile):
        self.username = username
        self.savefile = savefile

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'savefile')



user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user', methods=["POST"])
def add_user():
    username = request.json["username"]
    savefile = request.json["savefile"]

    new_user = User(username, savefile)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)


@app.route('/users', methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user/<id>', methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route("/user/<id>", methods=["PUT"])
def guide_update(id):
    user = User.query.get(id)
    username = request.json['username']
    savefile = request.json['savefile']

    user.username = username
    user.savefile = savefile

    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/user/<id>', methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return "Your user was succesfully deleted"

if __name__ == '__main__':
    app.run(debug=True)

    