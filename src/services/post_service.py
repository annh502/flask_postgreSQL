from src.repository import post_repo, user_repo
from src.share.Result import Result


def get_all():
    return post_repo.get_all()


def get_post(post_id):
    return post_repo.get_by_id(post_id)


def create_post(post, author_id):
    try:
        author_result = user_repo.get_by_id(author_id)
        if not author_result.is_success():
            return author_result
        if post['title'] is None:
            return Result.failed("Title must not be null.")
        if post['body'] is None:
            return Result.failed("Body must not be null.")
        return post_repo.save(post, author_id)
    except Exception as e:
        return Result.failed("Error at post_service: " + str(e))


def update_post(post, post_id):
    try:
        old_post = post_repo.get_by_id(post_id)
        if not old_post.is_success():
            return old_post
        return post_repo.update(old_post.data, post)
    except Exception as e:
        return Result.failed("Error at post_service: " + str(e))


def delete_post(post_id):
    try:
        post = post_repo.get_by_id(post_id)
        if not post.is_success():
            return post
        return post_repo.delete(post.data)
    except Exception as e:
        return Result.failed("Error at post_service: " + str(e))
