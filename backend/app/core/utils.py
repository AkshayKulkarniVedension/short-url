# /app/core/utils.py
import shortuuid

def generate_short_url():
    return shortuuid.ShortUUID().random(length=6)
