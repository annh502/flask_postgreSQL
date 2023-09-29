from flask import request
from src.services import user_service
from src.share.api.ResponseEntityFactory import *
from src.repository import user_repo, comment_repo
from flask import Blueprint
from auth_middleware import token_required

auth = Blueprint("Users", __name__)


@auth.route("/", methods=["GET"])
@token_required
def test(current_user):
    return ok("You have an account!!!" + str(current_user.data.email))


@auth.route("/signup", methods=["POST"])
def signup():
    try:
        user = request.json
        validate_result = user_service.validate_email_and_password(user)
        if not validate_result.is_success():
            return bad_request("Invalid input", validate_result.data)
        signup_result = user_service.create_user(user["name"], user["email"], user["password"])
        if not signup_result.is_success():
            return bad_request("Create account failed!", signup_result.data)
        else:
            result = {"token": signup_result.data}
            return ok(result)
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@auth.route("/signin", methods=['POST'])
def signin():
    try:
        user = request.json
        validate_result = user_service.validate_email_and_password(user)
        if not validate_result.is_success():
            return bad_request("Invalid input", validate_result.data)
        signin_result = user_service.login(user['email'], user['password'])
        if not signin_result.is_success():
            return bad_request("sign in account failed!", signin_result.data)
        else:
            return ok("Sign in account success! " + signin_result.data)
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@auth.route("/signout", methods=['POST'])
@token_required
def sign_out(token):
    try:
        sign_out_result = user_service.log_out(token)
        if sign_out_result.is_success():
            return ok(sign_out_result.data)
        return bad_request(sign_out_result.data)
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@auth.route("/update", methods=['PUT'])
@token_required
def update(current_user):
    try:
        user_id = current_user.data.id
        user = request.json
        validate_result = user_service.validate_email(user['email'])
        if not validate_result.is_success():
            return bad_request("Invalid input", validate_result.data)

        update_result = user_service.update_user(user_id, user)
        if not update_result.is_success():
            return bad_request("Update account failed!", update_result.data)
        else:
            return ok("Update account success! " + str(update_result.data))
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@auth.route("/delete", methods=['DELETE'])
@token_required
def delete(current_user):
    try:
        user_id = current_user.data.id
        delete_result = user_service.delete_user(user_id)
        if not delete_result.is_success():
            return bad_request("Delete account failed!", delete_result.data)
        else:
            return ok("Delete account success! " + str(delete_result.data))
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@auth.route("/disable/<int:account_id>", methods=['DELETE'])
@token_required
def disable(current_user, account_id):
    try:
        user_id = current_user.data.id
        disable_result = user_service.disable_account(user_id, account_id)
        if not disable_result.is_success():
            return bad_request("Disable account failed!", disable_result.data)
        return ok("Disable account success! " + str(disable_result.data))
    except Unauthorized:
        return unauthorized("You're not authorized to delete this user!")
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


@auth.route("/comments", methods=['GET'])
@token_required
def get_comments(current_user):
    try:
        author_id = current_user.data.id
        comments_result = comment_repo.get_all_by_author_id(author_id)
        return ok(comments_result.data) \
            if comments_result.is_success() \
            else bad_request(comments_result.data)
    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")
