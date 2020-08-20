import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

car =Blueprint('cars', 'car', url_prefix='/cars')

@car.route('/', methods=["GET"])
# @login_required
def get_all_cars():
    try:
        cars = [model_to_dict(car) for car in models.Car.select()]
        print(cars)
        return jsonify(data=cars, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@car.route('/carsbybuilder/<ownerid>', methods=["GET"])
@login_required
def get_all_cars_by_owner(ownerid):
    try:
        cars = [model_to_dict(car) for car in models.Car.select().where(models.Car.builder_id==ownerid)]
        print(cars)
        return jsonify(data=cars, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data=[], status={"code": 401, "message": "Error getting the resources"})

@car.route('/<id>', methods=["GET"])
@login_required
def get_one_car(id):
    print(id, 'reserved word?')
    car = models.Car.get_by_id(id)
    print(car.__dict__)
    return jsonify(data=model_to_dict(car), status={"code": 200, "message": "Success"})

@car.route('/', methods=["POST"])
@login_required
def create_cars():
    payload = request.get_json()
    print(type(payload), 'payload')
    car = models.Car.create(name=payload['name'], builder=current_user.id, make=payload['make'], model=payload['model'], year=payload['year'], photo_url=payload['photo_url'])
    car = models.Car.create(**payload)
    print(car.__dict__)
    print(dir(car))
    print(model_to_dict(car), 'model to dict')
    car_dict = model_to_dict(car)
    return jsonify(data=car_dict, status={"code": 201, "message": "Success"})

@car.route('/<id>', methods=["Delete"])
@login_required
def delete_car(id):
    query = models.Car.delete().where(models.Car.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

@car.route('/<id>', methods=["PUT"])
@login_required
def update_car(id):
    payload = request.get_json()
    query = models.Car.update(**payload).where(models.Car.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Car.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})