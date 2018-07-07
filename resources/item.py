from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )


    @jwt_required() #When the user makes a request, the jwt is sent with the request and jwt then uses identity() to try to confirm the user using the jwt. If successful, no login is required. if no jwt is sent, fails
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404



    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return {'name': item.name, 'price': item.price}, 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}


    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()