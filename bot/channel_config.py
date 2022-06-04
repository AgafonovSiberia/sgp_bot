from bot.config_reader import config

channel_id = config.channel_id

channel_join_not_link = True # разрешено ли подключаться в канал без ссылок-приглашений
channel_join_invite_from_admin = False  # принимать в канал по ссылкам, созданным админами (не ботом)
bot_approve_join_request = True  # бот сам подтверждает запросы по ссылкам, созданным админом
delete_request_after_join = True  # удаляем заявки из БД после вступления пользователя в канал


