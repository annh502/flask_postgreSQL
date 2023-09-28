from database.database import db
from src.models.Post import Post
from src.share.Result import Result
from src.repository.user_repo import get_by_id as get_author_by_id


def get_all():
    """Get all posts"""
    posts = Post.query.all()
    return posts


def get_by_id(post_id):
    """Get a post by id"""
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return Result.failed(post_id)
    return Result.success(post)


def save(data, author_id):
    """Create new post"""
    try:
        author = get_author_by_id(author_id)
        if not author.is_success():
            return Result.failed("Author not exist: " + str(author_id))
        new_post = Post(data['title'], data['short_description'], data['body'], author_id)
        db.session.add(new_post)
        db.session.commit()
        return Result.success(str(new_post.id))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def update(post_id, post):
    """Update a post"""
    try:
        post_result = get_by_id(post_id)
        if not post_result.is_success():
            return Result.failed(post_id)
        try:
            old_post = post_result.data
            if post['title']:
                old_post.title = post['title']
            if post['short_description']:
                old_post.short_description = post['short_description']
            if post['body']:
                old_post.body = post['body']
            db.session.commit()
            return Result.success(post_id)
        except Exception as e:
            return Result.failed("Cannot save" + str(e))
    except Exception as e2:
        return Result.failed(str(e2))


def delete(post_id):
    """Delete a post"""
    try:
        post_result = get_by_id(post_id)
        if not post_result.is_success():
            return Result.failed(post_id)
        try:
            db.session.delete(post_result.data)
            db.session.commit()
            return Result.success(post_id)

        except Exception as e:
            return Result.failed("Cannot save" + str(e))
    except Exception as e2:
        return Result.failed(str(e2))
