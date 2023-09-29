from database.database import db
from src.models.Like import Like
from src.models.PostLike import PostLike
from src.share.Result import Result


def save(post_id, author_id):
    try:
        like = Like()
        db.session.add(like)
        db.session.flush()
        db.session.refresh(like)

        post_like = PostLike(like.id, post_id, author_id)
        db.session.add(post_like)
        db.session.commit()

        return Result.success(post_like)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_id_by_post_author(post_id, author_id):
    try:
        post_like = PostLike.query.filter_by(post_id=post_id, author_id=author_id).first()
        return Result.success(post_like) \
            if post_like \
            else Result.failed("Cannot found")
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def _get_by_post_like(post_like):
    try:
        like = Like.query.filter_by(id=post_like.like_id).first()
        return like if like else Result.failed("Cannot found: " + post_like)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all_by_post_id(post_id):
    try:
        like_ids = PostLike.query.filter_by(post_id=post_id)
        likes = map(_get_by_post_like, like_ids)
        return Result.success(list(likes))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def count_likes(post_id):
    try:
        likes = get_all_by_post_id(post_id)
        return Result.success(len(likes.data))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def delete(post_like):
    try:
        like = _get_by_post_like(post_like)
        if isinstance(like, Like):
            db.session.delete(like)
            db.session.commit()
            return Result.success(like.id)
        return like
    except Exception as e:
        return Result.failed("Cannot save" + str(e))
