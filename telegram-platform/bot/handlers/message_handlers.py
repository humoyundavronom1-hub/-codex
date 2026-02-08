from bot.services.moderation_service import get_or_create_group, get_or_create_user, log_message

def register_message_handlers(bot, session_factory):
    @bot.message_handler(content_types=['text'])
    def on_message(message):
        if message.text and message.text.startswith('/'):
            return
        db = session_factory()
        try:
            group = get_or_create_group(db, message.chat.id, message.chat.title or str(message.chat.id))
            user = get_or_create_user(db, message.from_user)
            log_message(db, group, user)
        finally:
            db.close()
