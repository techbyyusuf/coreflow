from models.models import User

class UserService:
    def __init__(self, session):
        self.session = session

    def create_user(self, name, email):
        new_user = User(name=name, email=email)
        self.session.add(new_user)
        self.session.commit()

    def get_all_users(self):
        return self.session.query(User).all()

    def update_user_email(self, user_id, new_email):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            user.email = new_email
            self.session.commit()

    def delete_user(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
