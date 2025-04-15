from uuid import UUID


def to_uuid(val):
    return val if isinstance(val, UUID) else UUID(val)