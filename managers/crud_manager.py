import os

from werkzeug.exceptions import NotFound

from constants.Image_suffix import IMAGE_SUFFIX_IN_DB, IMAGE_SUFFIX_IN_SCHEMA, EXTENSION_SUFFIX_IN_SCHEMA
from constants.roots import TEMP_DIR
from db import db
from services.s3 import s3
from utils.helpers import save_file, create_photo_from_json, has_photo, get_photo_name_by_url


class CRUDManager:
    @classmethod
    def create(cls, data, user, model):
        data["holder_id"] = user.id

        if not hasattr(model, "get_all_image_field_names"):
            return cls._create_in_db(data, model)

        return cls._processed_with_photos(model, data)

    @staticmethod
    def get(pk, model):
        return model.query.filter_by(id=pk).first()

    @classmethod
    def edit(cls, data, pk, model):
        instance = cls.get(pk, model)
        if not hasattr(model, "get_all_image_field_names"):
            model.query.filter_by(id=instance.id).update(data)
            return instance

        return cls._processed_with_photos(model, data, instance)

    @classmethod
    def delete_image(cls, pk, model, image_field_name):
        instance = cls.get(pk, model)
        image_field_name_with_suffix = image_field_name + IMAGE_SUFFIX_IN_DB
        photo = get_photo_name_by_url(getattr(instance, image_field_name_with_suffix))
        if not photo:
            raise NotFound('Picture not found!')

        model.query.filter_by(id=instance.id).update({image_field_name_with_suffix: None})
        s3.delete_photo(photo)
        return instance

    @staticmethod
    def _create_in_db(data, model):
        instance = model(**data)
        db.session.add(instance)
        db.session.flush()
        return instance

    @classmethod
    def _processed_with_photos(cls, model, data, instance=None):
        is_edit = bool(instance)
        image_field_names = model.get_all_image_field_names()
        photo_names = []
        paths = []
        previous_pictures = []

        for image_field_name in image_field_names:
            photo_str = data.pop(image_field_name + IMAGE_SUFFIX_IN_SCHEMA) \
                if data.get(image_field_name + IMAGE_SUFFIX_IN_SCHEMA) else None
            extension = data.pop(image_field_name + EXTENSION_SUFFIX_IN_SCHEMA) \
                if data.get(image_field_name + EXTENSION_SUFFIX_IN_SCHEMA) else None
            if not has_photo(photo_str, extension):
                continue

            if is_edit:
                previous_picture = get_photo_name_by_url(getattr(instance, image_field_name + IMAGE_SUFFIX_IN_DB))
                previous_pictures.append(previous_picture)

            photo_name, photo = create_photo_from_json(photo_str, extension)
            photo_names.append(photo_name)
            path = os.path.join(TEMP_DIR, photo_name)
            paths.append(path)
            save_file(path, photo)

            photo_url = s3.upload_photo(path, photo_name)
            data[image_field_name + IMAGE_SUFFIX_IN_DB] = photo_url

        try:
            if is_edit:
                model.query.filter_by(id=instance.id).update(data)
                [s3.delete_photo(previous_picture) for previous_picture in previous_pictures if previous_picture]
                return instance
            return cls._create_in_db(data, model)

        except Exception:
            [s3.delete_photo(photo_name) for photo_name in photo_names]
        finally:
            [os.remove(path) for path in paths]
