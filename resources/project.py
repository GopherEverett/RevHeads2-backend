import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

project =Blueprint('projects', 'project', url_prefix='/projects')

@project.route('/', methods=["GET"])
def get_all_projects():
    try:
        projects = [model_to_dict(project) for project in models.Project.select()]
        print(projects)
        return jsonify(data=projects, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@project.route('/', methods=["POST"])
@login_required
def create_projects():
    payload = request.get_json()
    print(type(payload), 'payload')
    # project = models.Project.create(name=payload['name'], builder=current_user.id, make=payload['make'], model=payload['model'], year=payload['year'], photo_url=payload['photo_url'])
    project = models.Project.create(**payload)
    print(project.__dict__)
    print(dir(project))
    print(model_to_dict(project), 'model to dict')
    project_dict = model_to_dict(project)
    return jsonify(data=project_dict, status={"code": 201, "message": "Success"})

@project.route('/projectsbycar/<car_id>', methods=["GET"])
@login_required
def get_all_projects_by_owner(car_id):
    try:
        projects = [model_to_dict(project) for project in models.Project.select().where(models.Project.car_id==car_id)]
        print(projects)
        return jsonify(data=projects, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data=[], status={"code": 401, "message": "Error getting the resources"})

@project.route('/<id>', methods=["GET"])
@login_required
def get_one_project(id):
    print(id, 'reserved word?')
    project = models.Project.get_by_id(id)
    print(project.__dict__)
    return jsonify(data=model_to_dict(project), status={"code": 200, "message": "Success"})

@project.route('/<id>', methods=["Delete"])
@login_required
def delete_project(id):
    query = models.Project.delete().where(models.Project.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

@project.route('/<id>', methods=["PUT"])
@login_required
def update_project(id):
    payload = request.get_json()
    query = models.Project.update(**payload).where(models.Project.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Project.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})