from models.comment_model import Comments, db


class CommentRepository:
    @staticmethod
    def create_comment(text, post_id):
        new_comment = Comments(text=text, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()

    @staticmethod
    def get_comment_by_id(comment_id):
        return Comments.query.get(comment_id)

    @staticmethod
    def get_comments_by_post_id(post_id):
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
    def update_comment(comment_id, data):
        comment = Comments.query.get(comment_id)
        comment.text = data.get('text', comment.text)
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment_id):
        db.session.delete(comment_id)
        db.session.commit()


