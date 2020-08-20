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