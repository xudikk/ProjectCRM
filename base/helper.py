import base64
import binascii
import os
from datetime import datetime, timezone

from dashboard.models.extra import Otp


def code_hashing(key:str, decode=False):
    if decode:
        return base64.b64decode(key.encode()).decode()
    else:
        return base64.b64encode(key.encode()).decode()


def generate_key(x: int):
    return binascii.hexlify(os.urandom(x)).decode()


def check_otp(otp, code):
    if otp.is_expired:
        return {
            "expired": True
        }
    if (datetime.now(timezone.utc) - otp.created).total_seconds() > 120:
        otp.is_expired = True
        otp.save()
        return {
            "time_out": True
        }

    if str(code_hashing(otp.key, decode=True)).split("$")[1] != str(code):
        otp.tries += 1
        otp.save()
        print(str(code_hashing(otp.key, decode=True)).split("$")[1])
        print(code)
        return {
            "cer": True
        }
    otp.step = "checked"
    otp.save()
    return {
        "status": True
    }


