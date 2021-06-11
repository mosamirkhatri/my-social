from flask import Blueprint, request
from datetime import datetime
from app.utils.helpers import query_database
from app.database.queries import Query
from app.utils.decorators.login_required import login_required


post = Blueprint('post', __name__)


@post.route('/all', methods=['GET'])
def get_all_posts():
    try:
        all_posts = query_database(Query.GET_ALL_POSTS)
        return {"success": True, "data": all_posts}, 200
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500


@post.route('/user-post', methods=['POST'])
def get_user_posts():
    try:
        request_data = request.get_json()
        user_id = request_data.get('id')
        posts = query_database(Query.GET_USER_POSTS, (user_id))
        if not posts:
            return {"success": False, "message": "Not Found"}, 404
        if isinstance(posts, dict):
            posts = [posts]
        return {"success": True, "data": posts}, 200
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500


@post.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = query_database(Query.GET_POST, (post_id))
        if not post:
            return {"success": False, "message": "Not Found"}, 404
        return {"success": True, "data": post}, 200
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500


@post.route('/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(current_user, post_id):
    try:
        post = query_database(Query.GET_POST, (post_id))
        if not post:
            return {"success": False, "message": "Not Found"}, 404
        if current_user.get('id') == post.get('author'):
            query_database(Query.DELETE_POST, (post_id))
            return {"success": True, "data": post, "message": "Post deleted successfully"}, 200
        else:
            return {"success": False, "message": "You are not the owner of the post"}, 409
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500


@post.route('/create', methods=['POST'])
@login_required
def create_post(current_user):
    try:
        request_data = request.get_json()
        description = request_data.get('description')
        format = '%Y-%m-%d %H:%M:%S'
        created_at = datetime.utcnow().strftime(format)
        id = current_user.get('id')
        query_database(Query.CREATE_NEW_POST, (description, created_at, id))
        return {"success": True, "message": "Post successfully created"}, 200
    except Exception as e:
        return {"success": False, "message": "Internal Server Error"}, 500
