from src.repository import comment_repo, user_repo, post_repo
from src.share.Result import Result


def get_all():
    return comment_repo.get_all()


def create_comment(post_id, author_id, comment):
    try:
<<<<<<< HEAD
        if not post_repo.get_by_id(post_id).is_success():
            return Result.failed("Post doesn't exist: " + str(post_id))
        if not user_repo.get_by_id(author_id).is_success():
            return Result.failed("User doesn't exist: " + str(author_id))
=======
        if not post_repo.get_by_id(post_id):
            return Result.failed("Post doesn't exist: " + post_id)
        if not user_repo.get_by_id(author_id):
            return Result.failed("User doesn't exist: " + author_id)
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc
        if comment['content'] is None:
            return Result.failed("Content must not be null.")
        return comment_repo.save(post_id, author_id, comment)
    except Exception as e:
        return Result.failed("Error in comment services: " + str(e))


def get_all_by_user_id(author_id):
    try:
<<<<<<< HEAD
        if not user_repo.get_by_id(author_id).is_success():
            return Result.failed("User doesn't exist: " + str(author_id))
=======
        if not user_repo.get_by_id(author_id):
            return Result.failed("User doesn't exist: " + author_id)
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc
        return comment_repo.get_all_by_author_id(author_id)
    except Exception as e:
        return Result.failed("Error in comment services: " + str(e))


def get_all_by_post_id(post_id):
    try:
<<<<<<< HEAD
        if not post_repo.get_by_id(post_id).is_success():
            return Result.failed("Post doesn't exist: " + str(post_id))
=======
        if not post_repo.get_by_id(post_id):
            return Result.failed("Post doesn't exist: " + post_id)
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc
        return comment_repo.get_all_by_post_id(post_id)
    except Exception as e:
        return Result.failed("Error in comment services: " + str(e))
