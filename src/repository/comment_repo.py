from database.database import db
from src.models.Comment import Comment
from src.models.PostComment import PostComment
from src.share.Result import Result


def save(post_id, author_id, comment):
    try:
        new_comment = Comment(comment['content'])
        db.session.add(new_comment)
        db.session.flush()
        db.session.refresh(new_comment)

        new_post_comment = PostComment(new_comment.id, post_id, author_id)
        db.session.add(new_post_comment)
        db.session.commit()
        return Result.success(new_comment)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_by_id(comment_id):
    try:
        comment = Comment.query.filter_by(id=comment_id).first()
        return Result.success(comment)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def _get_by_post_comment(post_comment):
    try:
        comment = Comment.query.filter_by(id=post_comment.comment_id).first()
        return comment
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all_by_post_id(post_id):
    try:
        comment_ids = PostComment.query.filter_by(post_id=post_id)
        comments = map(_get_by_post_comment, comment_ids)
        return Result.success(list(comments))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all_by_author_id(author_id):
    try:
        comment_ids = PostComment.query.filter_by(author_id=author_id)
        comments = map(get_by_id, comment_ids)
        return Result.success(list(comments))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all():
    try:
        comment_ids = PostComment.query.all()
        comments = map(get_by_id, comment_ids)
        return Result.success(list(comments))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))
