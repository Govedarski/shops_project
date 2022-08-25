import os

from sqlalchemy.exc import InvalidRequestError
from werkzeug.exceptions import NotFound, Forbidden

from constants.Image_suffix import IMAGE_SUFFIX_IN_DB, IMAGE_SUFFIX_IN_SCHEMA, EXTENSION_SUFFIX_IN_SCHEMA
from constants.roots import TEMP_DIR
from db import db
from models import AdminRoles
from services.s3 import s3
from utils import helpers
from utils.decorators import handle_unique_constrain_violation
from utils.helpers import save_file, create_photo, has_photo, get_photo_name_by_url


class BaseManager:
    MODEL = None
    UNIQUE = False
    UNIQUE_CONSTRAINT_MESSAGE = "Unique constraint: Object already exist!"
    PERMISSION_DENIED_MESSAGE = "Permission denied!"
    _INSTANCE = None

    @handle_unique_constrain_violation
    def create(self, data, user, **kwargs):
        if self._uniqueness_required():
            self._check_uniqueness(user)

        data["holder_id"] = None
        if hasattr(self.get_model(), "holder_id") and user:
            data["holder_id"] = user.id

        if not hasattr(self.get_model(), "get_all_image_field_names"):
            return self._create_in_db(self.get_model(), data)

        return self._processed_with_photos(self.get_model(), data)

    def get(self, pk, **kwargs):
        self._check_access(pk, **kwargs)
        return self._get_instance(pk)

    def get_list(self, filter_by, **kwargs):
        try:
            return self.get_model().query.filter_by(**filter_by).all()
        except InvalidRequestError:
            # Invalid query string
            return []

    @handle_unique_constrain_violation
    def edit(self, data, pk, **kwargs):
        self._check_access(pk, **kwargs)
        instance = self._get_instance(pk)
        if not hasattr(self.get_model(), "get_all_image_field_names"):
            self.get_model().query.filter_by(id=instance.id).update(data)
            return instance

        return self._processed_with_photos(self.get_model(), data, instance)

    def delete(self, pk, **kwargs):
        self._check_access(pk, **kwargs)
        instance = self._get_instance(pk)
        if not hasattr(self.get_model(), "get_all_image_field_names"):
            self.get_model().query.filter_by(id=instance.id).delete()
            return None

        return self._delete_with_photos(self.get_model(), instance)

    def delete_image(self, pk, image_field_name, **kwargs):
        self._check_access(pk, **kwargs)
        instance = self._get_instance(pk)
        image_field_name_with_suffix = image_field_name + IMAGE_SUFFIX_IN_DB
        photo_url = getattr(instance, image_field_name_with_suffix)
        photo = get_photo_name_by_url(photo_url)
        if not photo:
            raise NotFound('Picture not found!')

        self.get_model().query.filter_by(id=instance.id).update({image_field_name_with_suffix: None})
        s3.delete_photo(photo)
        return instance

    def _get_instance(self, pk):
        if not self._INSTANCE:
            self._INSTANCE = helpers.get_or_404(self.get_model(), pk)
        return self._INSTANCE

    @staticmethod
    def _create_in_db(model, data):
        instance = model(**data)
        db.session.add(instance)
        db.session.flush()
        return instance

    def _processed_with_photos(self, model, data, instance=None):
        is_edit = bool(instance)
        image_field_names = model.get_all_image_field_names()
        photo_names = []
        paths = []
        previous_pictures = []
        try:
            for image_field_name in image_field_names:
                photo_str = data.pop(image_field_name + IMAGE_SUFFIX_IN_SCHEMA) \
                    if data.get(image_field_name + IMAGE_SUFFIX_IN_SCHEMA) else None
                extension = data.pop(image_field_name + EXTENSION_SUFFIX_IN_SCHEMA) \
                    if data.get(image_field_name + EXTENSION_SUFFIX_IN_SCHEMA) else None
                if not has_photo(photo_str, extension):
                    continue

                if is_edit:
                    photo_url = getattr(instance, image_field_name + IMAGE_SUFFIX_IN_DB)
                    previous_picture = get_photo_name_by_url(photo_url)
                    previous_pictures.append(previous_picture)

                photo_name, photo = create_photo(photo_str, extension)
                photo_names.append(photo_name)
                path = os.path.join(TEMP_DIR, photo_name)
                paths.append(path)
                save_file(path, photo)

                photo_url = s3.upload_photo(path, photo_name)
                data[image_field_name + IMAGE_SUFFIX_IN_DB] = photo_url

            if is_edit:
                model.query.filter_by(id=instance.id).update(data)
                [s3.delete_photo(previous_picture) for previous_picture in previous_pictures if previous_picture]
            else:
                instance = self._create_in_db(model, data)

        except Exception as ex:
            [s3.delete_photo(photo_name) for photo_name in photo_names]
            raise ex
        finally:
            [os.remove(path) for path in paths]

        return instance

    def get_model(self):
        return self.MODEL

    @staticmethod
    def _delete_with_photos(model, instance, **kwargs):
        image_field_names = model.get_all_image_field_names()
        photo_to_delete = []

        for image_field_name in image_field_names:
            photo_name = get_photo_name_by_url(getattr(instance, image_field_name + IMAGE_SUFFIX_IN_DB))
            photo_to_delete.append(photo_name)

        model.query.filter_by(id=instance.id).delete()
        [s3.delete_photo(photo) for photo in photo_to_delete if photo]

    def _check_uniqueness(self, user):
        if self.get_model().query.filter_by(holder_id=user.id).first():
            raise Forbidden(self.UNIQUE_CONSTRAINT_MESSAGE)

    def _is_holder(self, instance, user):
        if user.role in AdminRoles:
            return

        if not user or not instance.holder_id == user.id:
            raise Forbidden(self.PERMISSION_DENIED_MESSAGE)

    def _check_access(self, pk, **kwargs):
        if self._INSTANCE:
            return
        instance = self._get_instance(pk)
        if kwargs.get("holder_required"):
            user = kwargs.get("user")
            self._is_holder(instance, user)
        self._INSTANCE = instance

    def _uniqueness_required(self):
        return self.UNIQUE
