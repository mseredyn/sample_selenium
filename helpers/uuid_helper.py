from uuid import uuid4


def generate_uuid():
    rand = str(uuid4())
    rand = rand.replace("-", "")
    return rand[:16]
