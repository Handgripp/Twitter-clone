from models.post_model import Posts, db
from repositories.comment_repositories import CommentRepository
from repositories.user_repositories import UserRepository
from sqlalchemy import update


class PostRepository:

    @staticmethod
    def create(text, user_id):
        new_post = Posts(
            text=text,
            user_id=user_id,
            likes=[]
        )
        db.session.add(new_post)
        db.session.commit()

    @staticmethod
    def get_post_by_id(post_id, user_id):
        post = Posts.query.filter_by(id=post_id).first()

        if not post:
            return None

        user = UserRepository.get_one(post.user_id)

        comments = CommentRepository.get_many_by_post_id(post.id)

        post_data = {
            'id': post.id,
            'user_name': user['name'] if user else None,
            'text': post.text,
            'likes': len(post.likes),
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'comments': comments
        }

        user_liked = False
        if user_id in post.likes:
            user_liked = True

        post_data['is_liked'] = user_liked

        return post_data

    @staticmethod
    def get_post_by_id_without_comments(post_id):
        post = Posts.query.filter_by(id=post_id).first()

        if not post:
            return None

        user = UserRepository.get_one(post.user_id)

        post_data = {
            'id': post.id,
            'user_name': user['name'] if user else None,
            'text': post.text,
            'likes': post.likes,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
        }

        return post_data



    @staticmethod
    def update(post, data):
        post.text = data.get('text', post.text)
        db.session.commit()
        return post

    @staticmethod
    def delete(post_id):
        db.session.delete(post_id)
        db.session.commit()

    @staticmethod
    def like(post, user_id):
        likes = post['likes']
        likes.append(str(user_id))
        stmt = update(Posts).where(Posts.id == post["id"]).values(likes=likes)
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def unlike(post, user_id):
        likes = post['likes']
        likes.remove(str(user_id))
        stmt = update(Posts).where(Posts.id == post["id"]).values(likes=likes)

        db.session.execute(stmt)
        db.session.commit()


