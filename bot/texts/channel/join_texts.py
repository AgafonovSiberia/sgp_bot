async def not_join_request(text_error) -> str:
    return f"\U0001F6AB К сожалению, Вам отказано в подписке на канал\n\n" \
           f"<i>{text_error}</i>\n\n" \
           f"Обратитесь за помощью к HR компании"


async def admin_not_approve_join() -> str:
    return f"\U0001F6AB к сожалению, администратор отменил ваш запрос.\n\n" \
           f"Обратитесь за помощью к HR компании"
