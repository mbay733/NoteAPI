from api import db, Config
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeSerializer, BadSignature
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from api.models.note import NoteModel


class UserModel(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    notes: WriteOnlyMapped['NoteModel'] = relationship(lambda: NoteModel, back_populates='author', cascade="all, delete-orphan",passive_deletes=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False, server_default="simple_user", default="simple_user")

    def __init__(self, username, password, role="simple_user"):
        self.username = username
        self.role = role
        self.hash_password(password)

    def get_roles(self):
        return self.role

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        s = URLSafeSerializer(Config.SECRET_KEY)
        return s.dumps({'id': self.id})

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:  # Обработка ошибки "создание пользователя с НЕ уникальным именем"
            db.session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        s = URLSafeSerializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user