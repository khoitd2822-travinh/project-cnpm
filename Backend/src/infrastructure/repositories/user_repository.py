from src.domain.user import User

class userrepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_email(self, email):
        
        user_data = self.db_session.execute(
            "SELECT user_id, username, password, role FROM users WHERE username = :email",
            {"email": email}
        ).fetchone()

        if user_data:
             return User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                password=user_data['password'], 
                role=user_data['role']
            )
        return None
    
    def create_user(self, email, password, full_name, role):
    
         query = "INSERT INTO users (email, password, full_name, role) VALUES (%s, %s, %s, %s) RETURNING user_id"
         values = (email, password, full_name, role)
         new_id = self.db.execute_and_return_id(query, values)
         return User(user_id=new_id, email=email, role=role)