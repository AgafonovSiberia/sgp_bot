from aiogram import types


async def create_fake_chat(fake_user: types.User) -> dict:
    return {"id": fake_user.id,
            "first_name": fake_user.first_name,
            "last_name": fake_user.last_name,
            "username": fake_user.username,
            "type": "private",
            }

async def create_fake_message(fake_user: types.User):
	return types.Message(**{
    "message_id": 7777,
    "from": fake_user,

    "chat": await create_fake_chat(fake_user=fake_user),

    "date": 1508709711,
    "text": "/start"
})

async def create_fake_callback(fake_user: types.User, callback_data:str):
    return types.CallbackQuery(**{
        "id": 99999,
        "from_user":fake_user,
        "chat_instance": "--",
        "chat": await create_fake_chat(fake_user=fake_user),
        "message": await create_fake_message(fake_user=fake_user),
        "data": callback_data
    })


