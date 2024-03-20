from sqlalchemy import Column, String, ForeignKey, Enum

from ..databases.basemodel_1 import Base, BaseModel


class Friend(BaseModel, Base):
    __tablename__ = 'friends'

    friend_id = Column(String(150), ForeignKey('users.id'), nullable=False)
    user_id = Column(String(150), ForeignKey('users.id'), nullable=False)
    status = Column(Enum("pending", "friends", "blocked"), nullable=False)

    def __init__(self, friend_id, user_id, status):
        super().__init__()

        self.friend_id = friend_id
        self.user_id = user_id
        self.status = status