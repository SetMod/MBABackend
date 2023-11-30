from flask_mailman import EmailMessage
from marshmallow import ValidationError
from app.logger import logger
import secrets


def generate_reset_token():
    # Generate a random token (for example purposes)
    return secrets.token_urlsafe(32)


def send_reset_email(email, token):
    logger.info(f"Sending reset password email to '{email}'")

    msg = EmailMessage()
    msg.from_email = "your_email@example.com"
    msg.to = email
    msg.subject = "Password Reset"
    msg.body = f"Reset your password using this link: http://yourapp.com/reset_password?token={token}"
    msg.send()

    logger.info(f"Reset email sent to '{email}'")


def password_check(passwd: str):
    special_symbols = ["$", "@", "#", "%"]
    min_length = 6
    max_length = 20

    is_valid = True
    err_msgs = []
    if len(passwd) < min_length:
        err_msg = f"Length should be at least {min_length}"
        err_msgs.append(err_msg)
        is_valid = False

    if len(passwd) > max_length:
        err_msg = f"Length should be not be greater than {max_length}"
        err_msgs.append(err_msg)
        is_valid = False

    if not any(char.isdigit() for char in passwd):
        err_msg = "Must have at least one numeral"
        err_msgs.append(err_msg)
        is_valid = False

    if not any(char.isupper() for char in passwd):
        err_msg = "Must have at least one uppercase letter"
        err_msgs.append(err_msg)
        is_valid = False

    if not any(char.islower() for char in passwd):
        err_msg = "Must have at least one lowercase letter"
        err_msgs.append(err_msg)
        is_valid = False

    if not any(char in special_symbols for char in passwd):
        symbols = ", ".join([f"'{s}'" for s in special_symbols])
        err_msg = f"Must have at least one of the symbols: {symbols}"
        err_msgs.append(err_msg)
        is_valid = False

    if not is_valid and len(err_msgs) > 0:
        raise ValidationError(err_msgs)

    return is_valid
