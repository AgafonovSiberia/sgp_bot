from sqlalchemy import Column, BigInteger, Text, DateTime, Integer, Boolean

from bot.database.base import Base
from bot.misc.pydantic_models import MemberPydantic
from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

class ChannelMember(Base):
    __tablename__ = "members"

    user_id = Column(BigInteger, primary_key=True, unique=True)
    user_tg_name = Column(Text, default="NotTgName")
    user_tg_nickname = Column(Text, default="NotNickname")
    user_name = Column(Text, default="unknown")
    user_position = Column(Text, default="unknown")
    user_phone_number = Column(Text, default="unknown")
    user_status = Column(Text, default="member")

    invite_link = Column(Text, default="unknown")
    from_user_id = Column(BigInteger)
    from_user_name = Column(Text, default="unknown")
    from_user_nickname = Column(Text, default="unknown")
    update_date = Column(DateTime(timezone=True), server_default=func.now())
    employment_date = Column(DateTime(timezone=True), default=None)

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


class CongratulationData(Base):
    __tablename__ = "congratulation"
    slot_id = Column(Integer,  primary_key=True, unique=True)
    caption = Column(Text, default="unknown")
    img_id = Column(Text, default="unknown")

    def __init__(self, slot_id: int, caption: str, img_id: str):
        self.slot_id = slot_id
        self.caption = caption
        self.img_id = img_id


class ModuleSettings(Base):
    __tablename__ = "modules_settings"

    module_id = Column(Integer, primary_key=True, unique=True)
    module_name = Column(Text, unique=True)
    is_active = Column(Boolean, default=False)
    config = Column(MutableDict.as_mutable(JSONB))

    def __init__(self, module_name: str, is_active: bool, module_config: dict):
        self.module_name = module_name
        self.is_active = is_active
        self.config = module_config

class Lottery(Base):
    __tablename__ = "lottery_list"
    user_id = Column(BigInteger, unique=True)
    code = Column(Integer, primary_key=True)
    ticket_file_id = Column(Text, default=None)



