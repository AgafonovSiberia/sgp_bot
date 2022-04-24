from pydantic import BaseModel
from datetime import datetime
from typing import Union


class User(BaseModel):
    user_id: int
    user_name: Union[str, None]
    user_nickname: Union[str, None]


class UserPassport(BaseModel):
    real_name: Union[str, None]
    position: Union[str, None]
    phone_number: Union[str, None]


class MemberPydantic(BaseModel):
    user: User
    user_passport: UserPassport
    user_status: Union[str, None]
    invite_link: Union[str, None]
    from_user: User
    update_date: Union[datetime, None]


