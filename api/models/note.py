from api import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class NoteModel(db.Model):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="cascade"))
    author: Mapped['UserModel'] = relationship(back_populates='notes')
    text: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    private: Mapped[bool] = mapped_column(default=True, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"(id: {self.id}, {self.text = }, author:{self.author.username})"