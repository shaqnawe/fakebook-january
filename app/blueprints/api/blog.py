from flask import request , jsonify
from app.blueprints.blog.models import Post
from app import db

from .import bp as api

@api.route('/blog')
def all():
    '''
    [GET] /api/v1/blog
    '''
    return jsonify([p.to_dict() for p in Post.query.all()])

@api.route('/blog/<id>')
def retrieve(id):
    '''
    [GET] /api/v1/blog/<id>
    '''
    return jsonify(Post.query.get(id).to_dict())

@api.route('/blog', methods=['POST'])
def create():
    '''
    [POST] /api/v1/blog
    '''
    data = request.get_json()
    print(data)
    p = Post(
        body=data.get('body'),
        user_id=data.get('user_id')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict())


@api.route('/blog/<id>', methods=['PUT'])
def update(id):
    '''
    [PUT] /api/v1/blog/<id>
    '''
    data = request.get_json()

    p = Post.query.get(id)
    p.body = data.get('body')
    p.user_id = data.get('user_id')

    # only run .commit on pre-existing data
    db.session.commit()
    return jsonify(p.to_dict())

@api.route('/blog/<id>', methods=['DELETE'])
def delete(id):
    '''
    [DELETE] /api/v1/blog/<id>
    '''
    p = Post.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify([p.to_dict() for p in Post.query.all()])