from telebot import types
from bot.services.moderation_service import get_or_create_group, get_or_create_user, ensure_progress, increment_invite

def register_member_handlers(bot, session_factory):
    @bot.message_handler(content_types=['new_chat_members'])
    def on_new_members(message: types.Message):
        db = session_factory()
        try:
            group = get_or_create_group(db, message.chat.id, message.chat.title or str(message.chat.id))
            inviter = get_or_create_user(db, message.from_user)
            for m in message.new_chat_members:
                new_user = get_or_create_user(db, m)
                progress = ensure_progress(db, group, new_user)
                if not (m.is_bot and group.ignore_bots):
                    bot.restrict_chat_member(message.chat.id, m.id, can_send_messages=False)
                    bot.send_message(message.chat.id, f"Welcome 👋\nTo chat you must invite {progress.required_invites} users.\nProgress: 0 / {progress.required_invites}")
                p = increment_invite(db, group, inviter, new_user)
                if p:
                    remaining = max(p.required_invites - p.invites_count, 0)
                    bot.send_message(message.chat.id, f"✅ One user added\nRemaining: {remaining}")
                    if p.unlocked:
                        bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=True)
                        bot.send_message(message.chat.id, '🎉 You can now chat freely!')
        finally:
            db.close()
