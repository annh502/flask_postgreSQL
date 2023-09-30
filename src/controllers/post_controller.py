from flask import Blueprint, request

from auth_middleware import token_required
from src.services import post_service, comment_service
from src.share.api.ResponseEntityFactory import *

post_route = Blueprint("Posts", __name__)


@post_route.route("/", methods=["GET"])
def get_posts():
    try:
        posts = post_service.get_all()
        return ok(posts.data) \
            if posts.is_success() \
            else bad_request("Posts not found")
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@post_route.route("/<int:post_id>", methods=['GET'])
def get_post(post_id):
    try:
        post = post_service.get_post(post_id)
        return ok(post.data) \
            if post.is_success() \
            else bad_request(f"Post {post_id} not found")
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@post_route.route("/create", methods=['POST'])
@token_required
def create_post(current_user):
    try:
        author_id = current_user.data.id
        post = request.json
        create_result = post_service.create_post(post, author_id)
        return ok(create_result.data) \
            if create_result.is_success() \
            else bad_request("Cannot create post: " + str(create_result.data))
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@post_route.route("/<int:post_id>/update", methods=['PUT', 'POST'])
@token_required
def update_post(current_user, post_id):
    try:
        old_post = post_service.get_post(post_id)
        if old_post.data.author_id != current_user.data.id:
            return bad_request("You're not allowed to edit this post")
        post = request.json
        update_result = post_service.update_post(post, post_id, current_user.data.id)
        return ok(update_result.data) \
            if update_result.is_success() \
            else bad_request("Cannot update post: " + str(update_result.data))
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@post_route.route("/<int:post_id>/delete", methods=['DELETE', 'POST'])
@token_required
def delete_post(current_user, post_id):
    try:
        old_post = post_service.get_post(post_id)
        if not old_post.is_success():
            return bad_request(old_post.data, post_id)
<<<<<<< HEAD
        if int(old_post.data.author_id) != int(current_user.data.id) and not current_user.data.is_admin():
=======
        if old_post.data.author_id != current_user.data.id or not current_user.data.is_admin():
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc
            return bad_request("You're not allowed to delete this post")
        delete_result = post_service.delete_post(post_id)
        return ok(delete_result.data) \
            if delete_result.is_success() \
            else bad_request("Cannot update post: " + str(delete_result.data))
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@post_route.route("/<int:post_id>/comment", methods=['POST'])
@token_required
def comment_post(current_user, post_id):
    try:
        comment = request.json
        author_id = current_user.data.id
        comment_result = comment_service.create_comment(post_id, author_id, comment)
        return ok(comment_result.data) \
            if comment_result.is_success() \
            else bad_request("Cannot comment on post: " + str(comment_result.data))
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@post_route.route("/<int:post_id>/comments", methods=['GET'])
def get_comments(post_id):
    try:
        comments_result = comment_service.get_all_by_post_id(post_id)
        return ok(comments_result.data) \
            if comments_result.is_success() \
            else bad_request(comments_result.data)
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


<<<<<<< HEAD
@post_route.route("/<int:post_id>/likes", methods=['GET'])
def get_likes(post_id):
    try:
        likes_result = post_service.count_likes(post_id)
        return make_response(jsonify(likes_result, 200)) \
=======
@post_route.route("/<int:post:id>/likes", methods=['GET'])
def get_likes(post_id):
    try:
        likes_result = post_service.count_likes(post_id)
        return ok(likes_result.data) \
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc
            if likes_result.is_success() \
            else bad_request(likes_result.data)
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@post_route.route("/<int:post_id>/like", methods=['POST'])
@token_required
def like_post(current_user, post_id):
    try:
        author_id = current_user.data.id
        likes_result = post_service.like_post(author_id, post_id)
        return ok(likes_result.data) \
            if likes_result.is_success() \
            else bad_request(likes_result.data)
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")
