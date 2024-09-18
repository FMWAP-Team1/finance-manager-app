from uuid import uuid4


def assemble_kwargs(**kwargs):
    return kwargs


def generate_id_by_login_type(login_type: str) -> str:
    unique_uuid = str(uuid4())
    unique_id = f"{login_type}_{unique_uuid}"

    return unique_id
