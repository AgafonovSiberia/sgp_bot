from aiogram import types
from pydantic import ValidationError
from bot.models.member import MemberPydantic
from bot.db.models import ChannelMember


async def update_to_member_pydantic(update: types.ChatMemberUpdated, request=None):
    try:
        member = MemberPydantic(
            user={
                "user_id": update.new_chat_member.user.id,
                "user_name": (str(update.new_chat_member.user.first_name) + ' ' + str(
                    update.new_chat_member.user.last_name)).replace("None", ""),
                "user_nickname": update.new_chat_member.user.username,
            },

            user_passport={
                "real_name": request.user_name if request else None,
                "position": request.user_position if request else None,
                "phone_number": request.user_phone_number if request else None
            },

            from_user={
                "user_id": update.invite_link.creator.id if update.invite_link else update.from_user.id,
                "user_name": str(update.invite_link.creator.first_name) + ' ' + str(update.invite_link.creator.last_name).replace("None", "") if update.invite_link else str(update.from_user.first_name) + ' ' + str(update.from_user.last_name).replace("None", ""),
                "user_nickname": update.invite_link.creator.username if update.invite_link else update.from_user.username
            },
            user_status=update.new_chat_member.status,
            invite_link=update.invite_link.invite_link if update.invite_link else None,
            update_date=update.date

        )
        return member

    except ValidationError as e:
        print(e.json)


async def channel_member_model_to_member_pydantic(channel_member: ChannelMember):
    try:
        member = MemberPydantic(
            user={
                "user_id": channel_member.user_id,
                "user_name": channel_member.user_tg_name,
                "user_nickname": channel_member.user_tg_nickname
            },

            user_passport={
                "real_name": channel_member.user_name,
                "position": channel_member.user_position,
                "phone_number": channel_member.user_phone_number
            },

            from_user={
                "user_id": channel_member.from_user_id,
                "user_name":channel_member.from_user_name,
                "user_nickname": channel_member.from_user_nickname
            },
            user_status=channel_member.user_status,
            invite_link=channel_member.invite_link,
            update_date=channel_member.update_date
        )
        return member

    except ValidationError as e:
        print(e.json)

