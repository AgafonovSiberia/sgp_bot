from aiogram import types


async def create_fake_message(fake_user: types.User):
	return types.Message(**{
    "message_id": 7777,
    "from": fake_user,

    "chat": {
            "id": fake_user.id,
            "first_name": fake_user.first_name,
            "last_name": fake_user.last_name,
            "username": fake_user.username,
            "type": "private",
            },

    "date": 1508709711,
    "text": "/start"
})



