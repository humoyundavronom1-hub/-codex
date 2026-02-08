from sqlalchemy import func
from backend.models.models import Group, User, UserProgress, InviteLog, MessagesLog

def register_command_handlers(bot, session_factory):
    @bot.message_handler(commands=['my_status'])
    def my_status(message):
        db = session_factory()
        try:
            user = db.query(User).filter(User.telegram_user_id == str(message.from_user.id)).first()
            group = db.query(Group).filter(Group.telegram_group_id == str(message.chat.id)).first()
            if not user or not group:
                bot.reply_to(message, 'Ma’lumot topilmadi')
                return
            p = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.group_id == group.id).first()
            if not p:
                bot.reply_to(message, 'Progress yo‘q')
                return
            bot.reply_to(message, f"Progress: {p.invites_count} / {p.required_invites}. Unlocked: {p.unlocked}")
        finally:
            db.close()

    @bot.message_handler(commands=['my_invites'])
    def my_invites(message):
        db = session_factory()
        try:
            user = db.query(User).filter(User.telegram_user_id == str(message.from_user.id)).first()
            group = db.query(Group).filter(Group.telegram_group_id == str(message.chat.id)).first()
            if not user or not group:
                bot.reply_to(message, 'Ma’lumot topilmadi'); return
            count = db.query(func.count(InviteLog.id)).filter(InviteLog.group_id == group.id, InviteLog.inviter_user_id == user.id).scalar() or 0
            bot.reply_to(message, f"Sizning takliflaringiz: {count}")
        finally:
            db.close()

    @bot.message_handler(commands=['rules'])
    def rules(message):
        db = session_factory()
        try:
            group = db.query(Group).filter(Group.telegram_group_id == str(message.chat.id)).first()
            if not group:
                bot.reply_to(message, 'Qoidalar topilmadi'); return
            bot.reply_to(message, f"invite_required={group.invite_required}, reset_on_leave={group.reset_on_leave}, ignore_bots={group.ignore_bots}, admins_bypass={group.admins_bypass}, auto_kick_timeout={group.auto_kick_timeout}, risk_threshold={group.risk_threshold}")
        finally:
            db.close()

    @bot.message_handler(commands=['my_stats'])
    def my_stats(message):
        db = session_factory()
        try:
            user = db.query(User).filter(User.telegram_user_id == str(message.from_user.id)).first()
            group = db.query(Group).filter(Group.telegram_group_id == str(message.chat.id)).first()
            if not user or not group:
                bot.reply_to(message, 'Ma’lumot topilmadi'); return
            msg_count = db.query(func.count(MessagesLog.id)).filter(MessagesLog.group_id == group.id, MessagesLog.user_id == user.id).scalar() or 0
            inv_count = db.query(func.count(InviteLog.id)).filter(InviteLog.group_id == group.id, InviteLog.inviter_user_id == user.id).scalar() or 0
            bot.reply_to(message, f"Xabarlar: {msg_count}\nTakliflar: {inv_count}")
        finally:
            db.close()
