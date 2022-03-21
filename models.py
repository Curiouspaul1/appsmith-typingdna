from app import db
from werkzeug.security import generate_password_hash
import uuid

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String())
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String())
    typing_id = db.Column(db.String(), default=str(uuid.uuid4()))

    def __init__(self, *args) -> None:
        super().__init__()
        if args:
            params = args[0]
            for key, val in params.items():
                if key.lower() == 'password':
                    setattr(self, key, str(generate_password_hash(str(val))))
                else:
                    setattr(self, key, val)
