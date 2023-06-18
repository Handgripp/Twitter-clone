from models.post_model import Posts, db
from repositories.comment_repositories import CommentRepository
from repositories.user_repositories import UserRepository


class PostRepository:

    @staticmethod
    def create_post(text, user_id):
        new_post = Posts(
            text=text,
            user_id=user_id
        )
        db.session.add(new_post)
        db.session.commit()

    @staticmethod
    def get_post_by_id(post_id):
        post = Posts.query.filter_by(id=post_id).first()

        if not post:
            return None

        user = UserRepository.get_one_user(post.user_id)

        comments = CommentRepository.get_comments_by_post_id(post.id)

        post_data = {
            'id': post.id,
            'user_name': user['name'] if user else None,
            'text': post.text,
            'likes': post.likes,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'comments': comments
        }

        return post_data

    @staticmethod
    def update_post(post, data):
        post.text = data.get('text', post.text)
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id):
        db.session.delete(post_id)
        db.session.commit()

