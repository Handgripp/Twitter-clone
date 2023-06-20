from sqlalchemy import update
from models.comment_model import Comments, db
from models.user_model import Users


class CommentRepository:
    @staticmethod
    def create(text, post_id):
        new_comment = Comments(text=text, post_id=post_id, likes=[])
        db.session.add(new_comment)
        db.session.commit()

    @staticmethod
    def get_one_by_id(comment_id, user_id):
        comment = Comments.query.filter_by(id=comment_id).first()
        user = Users.query.filter_by(id=user_id).first()
        if not comment:
            return None

        user_liked = str(user_id) in comment.likes
        comment_data = {
            'id': comment.id,
            'text': comment.text,
            'name': user.name,
            'likes': comment.likes,
            'likes_count': len(comment.likes),
            'created_at': comment.created_at,
            'updated_at': comment.updated_at,
            'is_liked': user_liked
        }

        return comment_data

    @staticmethod
    def get_many_by_post_id(post_id):
        comments = Comments.query.filter_by(post_id=post_id).all()

        comments_data = []
        for comment in comments:
            comment_data = {
                'id': comment.id,
                'post_id': comment.post_id,
                'text': comment.text,
                'likes': comment.likes,
                'created_at': comment.created_at,
                'updated_at': comment.updated_at
            }
            comments_data.append(comment_data)
        return comments_data

    @staticmethod
    def update(comment_id, data):
        comment = Comments.query.get(comment_id)
        comment.text = data.get('text', comment.text)
        db.session.commit()
        return comment

    @staticmethod
    def delete(comment_id):
        db.session.delete(comment_id)
        db.session.commit()

    @staticmethod
    def like(comment, user_id):
        likes = comment['likes']
        likes.append(str(user_id))
        stmt = update(Comments).where(Comments.id == comment["id"]).values(likes=likes)
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def unlike(comment, user_id):
        likes = comment['likes']
        likes.remove(str(user_id))
        stmt = update(Comments).where(Comments.id == comment["id"]).values(likes=likes)
        db.session.execute(stmt)
        db.session.commit()


