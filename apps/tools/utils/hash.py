from datetime import datetime


def hash_filename(instance, filename):
    now = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
    return f"uploads/{now}_{filename}"
