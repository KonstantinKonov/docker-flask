import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

bp = Blueprint("stores", __name__, description="Operations on stores")

@bp.route('/store')
class StoreList(MethodView):
    @bp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @bp.arguments(StoreSchema)
    @bp.response(200, StoreSchema)
    def post(self, data):
        store = StoreModel(**data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500, message="db integrity error")

        return store
    

@bp.route('/store/<store_id>')
class Store(MethodView):
    @bp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def put(self, store_id):
        data = request.get_json()
        try:
            store = stores[store_id] 
            store |= data
        except:
            abort(400)
        return stores

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")