import uuid
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.models.photo_tag import PhotoTag


def get_or_create_tag(db: Session, tag_name: str):
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if tag:
        return tag
    tag = Tag(id=uuid.uuid4(), name=tag_name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def attach_tags_to_photo(db: Session, photo_id, tag_names):
    tags = []
    for name in tag_names:
        tag = get_or_create_tag(db, name)
        photo_tag = PhotoTag(
            id=uuid.uuid4(), photo_id=photo_id, tag_id=tag.id
        )
        db.add(photo_tag)
        tags.append(tag)
    db.commit()
    return tags
