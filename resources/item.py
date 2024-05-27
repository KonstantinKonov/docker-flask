import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

bp = Blueprint("items", __name__, description="Operations on item")

@bp.route('/item')
class ListItems(MethodView):
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @bp.arguments(ItemSchema)
    @bp.response(200, ItemSchema)
    def post(self, data):
        item = ItemModel(**data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")

        return item


@bp.route('/item/<id>')
class Item(MethodView):
    @bp.response(200, ItemSchema)
    def get(self, id):
        for item in items:
            if item["store_id"] == id:
                return item
        abort(404)
    
    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, id):
        data = request.get_json()
        for item in items:
            if item["store_id"] == id:
                item |= data
                return item
        abort(404)

    def delete(self, id):
        for item in items:
            if item["store_id"] == id:
                del item
                return {"message": "Item deleted"}
        abort(404)