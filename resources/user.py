import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required

user =Blueprint('users', 'user', url_prefix='/user')

@user.route('/', methods=["GET"])
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.User.select()]
        print(users)
        return jsonify(data=users, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print('payload:', payload)
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user, ' this is user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or password incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or password incorrect"})

@user.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return jsonify(data={}, status={'code': 200, 'message': 'successful logout'})

@user.route('/builder/<builderid>', methods=["GET"])
@login_required
def get_one_builder(builderid):
    print(builderid, 'reserved word?')
    builder = models.User.get_by_id(builderid)
    print(builder.__dict__)
    return jsonify(data=model_to_dict(builder), status={"code": 200, "message": "Success"})

@user.route('/builder/<builderid>', methods=["PUT"])
# @login_required
def update_user(builderid):
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['password'] = generate_password_hash(payload['password'])
    query = models.User.update(**payload).where(models.User.id==builderid)
    query.execute()
    return jsonify(data=model_to_dict(models.User.get_by_id(builderid)), status={"code": 200, "message": "resource updated successfully"})

@user.route('/builer/<builderid>', methods=["DELETE"])
def delete_user(builderid):
    query = models.User.delete().where(models.User.id==builderid)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "messsage": "resource deleted successfully"})