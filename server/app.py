#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants')
def restaurants():

    restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

    response = make_response(
        games,
        200
    )

    return response

#class Restaurants(Resource):

    #def get(self):
        #restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()
        #restaurants = []
        #for restaurant in Restaurant.query.all():
            #restaurant_dict = restaurant.to_dict()
            #restaurants.append(restaurant_dict)

        #return restaurants, 200

#api.add_resource(Restaurants, '/restaurants')

class RestaurantsByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            response_dict = restaurant.to_dict()
            return jsonify(response_dict), 200
        else:
            return {"error": "Restaurant not found"}, 404

    def delete(self, id):

        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
           db.session.delete(restaurant)
           db.session.commit()

           return {}, 204
        else:
            return {"error": "Restaurant not found"}, 404

api.add_resource(RestaurantsByID, '/restaurants/<int:id>')

class Pizzas(Resource):

    def get(self):

        pizzas_list = [pizza.to_dict() for pizza in Pizza.query.all()]

        return pizzas_list, 200

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):

    def post(self):

        new_restaurant_pizza = RestaurantPizza(
            price=request.form['price'],
            pizza_id=request.form['pizza_id'],
            restaurant_id=request.form['restaurant_id'],
        )

        if (1 <= new_restaurant_pizza.price <= 30):
            db.session.add(new_restaurant_pizza)
            db.session.commit()

            response_dict = new_restaurant_pizza.to_dict()

            return jsonify(response_dict), 201

        else:
            return {"errors": ["validation errors"]}, 400

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
