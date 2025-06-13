from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from sqlalchemy import Enum as SqlEnum


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True)
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Profile(db.Model):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), unique=True)
    user: Mapped["User"] = relationship(
        "User", back_populates="profile", uselist=False)


class Follow(db.Model):
    __tablename__ = "follow"
    id: Mapped[int] = mapped_column(primary_key=True)
    following_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)


class PostType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_type: Mapped[PostType] = mapped_column(
        SqlEnum(PostType), nullable=False)
    post_url: Mapped[str] = mapped_column(String(120), nullable=False)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"), nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id"), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(300), nullable=False)
