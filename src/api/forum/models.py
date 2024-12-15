from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import BaseModel


class Post(BaseModel):
    title: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(600))
    image: Mapped[str] = mapped_column(String(250))

    comments = relationship("Comment", back_populates="post", passive_deletes=True)
    user = relationship("User", back_populates="posts", passive_deletes=True, uselist=True)


class Comment(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(440))
    image: Mapped[str] = mapped_column(String(250))

    user = relationship("User", back_populates="comments", uselist=True, passive_deletes=True)
    post = relationship("Post", back_populates="comments", uselist=True, passive_deletes=True)
