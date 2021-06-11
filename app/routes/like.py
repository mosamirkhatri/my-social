from app.database.queries import Query
from flask import Blueprint, request
from app.utils.decorators.login_required import login_required
from app.utils.helpers import query_database


like = Blueprint('like', __name__)


@like.route('/toggle', methods=['POST'])
@login_required
def add_like(current_user):
    try:
        request_data = request.get_json()
        user_id = current_user.get('id')
        post_id = request_data.get('post_id')
        post = query_database(Query.GET_POST_FOR_CHECK, (post_id))
        if not post:
            return {"success": False, "message": "Post not found"}, 404
        like_entry = query_database(Query.GET_LIKE_ENTRY, (post_id, user_id))
        print(like_entry)
        if not like_entry:
            query_database(Query.INSERT_LIKE, (post_id, user_id, 1))
            new_like_entry = query_database(
                Query.GET_LIKE_ENTRY, (post_id, user_id))
            return {"success": True, "data": new_like_entry}, 200
        new_status = int(not bool(like_entry.get('status')))
        query_database(Query.UPDATE_LIKE, (new_status, post_id, user_id))
        new_like_entry = query_database(
            Query.GET_LIKE_ENTRY, (post_id, user_id))
        return {"success": True, "data": new_like_entry}, 200
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500
