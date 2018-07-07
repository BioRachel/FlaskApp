from flask import Flask
from flask_restful import Api
from flask_jwt import JWT #jwt_required is a decorator

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__) # we know this from before
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rice'
api = Api(app) # wraps app in Api, giving different syntax and more functions


jwt = JWT(app, authenticate, identity) # jwt automatically generates a /auth endpoint
# when we call /auth we send a username and password, jwt library sends these data to authenticate() which attempts to authenticate the user. jwt sends back the user and a JSON WEB TOKEN (JWT). its a JSON object with the key "access_token" and a big long encoded string.

api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')
