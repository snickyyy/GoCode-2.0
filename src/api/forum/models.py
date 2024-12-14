from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import BaseModel


class Post(BaseModel):
    title: Mapped[str] = mapped_column(String(50))
    user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(600))
    image: Mapped[str] = mapped_column(String(250))

    comments: Mapped[List["Comment"]] = relationship(
        "Comment", backref="post", passive_deletes=True
    )


class Comment(BaseModel):
    user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(440))
    image: Mapped[str] = mapped_column(String(250))
