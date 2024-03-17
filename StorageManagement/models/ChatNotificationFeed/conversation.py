from sqlalchemy import Column, String, DATETIME, ForeignKey
from datetime import datetime, timezone

from ..databases.basemodel_2 import Base, BaseModel

class Conversation(BaseModel, Base):
    __tablename__ = 'conversation'

    name = Column(String(300), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

class ConversationParticipants(BaseModel, Base):
    __tablename__ = 'conversation_participants'

    user_id = Column(String(150), nullable=False, primary_key=True)
    conversation_id_1 = Column(String(150), nullable=False, primary_key=True)
    conversation_id = Column(String(150), ForeignKey("conversation.id"), nullable=False)

    def __init__(self, user_id, conversation_id):
        super().__init__()

        self.user_id = user_id
        self.conversation_id = conversation_id
        self.conversation_id_1 = conversation_id
