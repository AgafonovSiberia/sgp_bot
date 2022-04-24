from sqlalchemy import Column, BigInteger, Text, DateTime

from bot.db.base import Base
from bot.models.member import MemberPydantic
from sqlalchemy.sql import func

class ChannelMember(Base):
    __tablename__ = "members"

    user_id = Column(BigInteger, primary_key=True, unique=True)
    user_tg_name = Column(Text, default="NotTgName")  # tg: user.first_name + user.last_name
    user_tg_nickname = Column(Text, default="NotNickname")  # tg: user.username
    user_name = Column(Text, default="unknown")  # real name from registration
    user_position = Column(Text, default="unknown")  # real position from registration
    user_phone_number = Column(Text, default="unknown")  # real phone number from registration
    user_status = Column(Text, default="member")  # update.new_member_status.status

    invite_link = Column(Text, default="unknown")  # update.invite_link
    from_user_id = Column(BigInteger)  # update.from_user.id
    from_user_name = Column(Text, default="unknown")  # update.from_user.username + ..first_name + ..last_name
    from_user_nickname = Column(Text, default="unknown")
    update_date = Column(DateTime(timezone=True), server_default=func.now())# update.date

    def __init__(self, data: MemberPydantic):
        self.user_id = data.user.user_id
        self.user_tg_name = data.user.user_name
        self.user_tg_nickname = data.user.user_nickname
        self.user_name = data.user_passport.real_name
        self.user_position = data.user_passport.position
        self.user_phone_number = data.user_passport.phone_number
        self.invite_link = data.invite_link
        self.user_status = data.user_status
        self.from_user_id = data.from_user.user_id
        self.from_user_name = data.from_user.user_name
        self.from_user_nickname = data.from_user.user_nickname
        self.update_date = data.update_date


class ChannelRequest(Base):
    __tablename__ = "requests"

    user_id = Column(BigInteger, primary_key=True, unique=True)
    user_name = Column(Text, default="NotName")
    user_position = Column(Text, default="NotPosition")
    user_phone_number = Column(Text, default="NotPhoneNumber")
    invite_link = Column(Text, default="NotInviteLink")

    def __init__(self, user_id: int, user_name: str, user_position: str,
                 user_phone_number: str, invite_link: str):
        self.user_id = user_id
        self.user_name = user_name
        self.user_position = user_position
        self.user_phone_number = user_phone_number
        self.invite_link = invite_link
