import os

from werkzeug.exceptions import Forbidden, NotFound

from constants.roots import TEMP_DIR
from db import db
from models import CustomerDetailsModel
from services.s3 import s3
from utils.helpers import save_file, create_photo_from_json, has_photo, get_photo_name_by_url


class CustomerDetailsManager:
    @staticmethod
    def create(data, user):
        if CustomerDetailsModel.query.filter_by(customer_id=user.id).first():
            raise Forbidden(f"User with id: {user.id} has already created details!")

        print(user.id)
        data["customer_id"] = user.id
        photo_str = data.pop("photo") if data.get("photo") else None
        extension = data.pop("extension") if data.get("extension") else None

        if not has_photo(photo_str, extension):
            return CustomerDetailsManager._create_customer_details_in_db(data)

        photo_name, photo = create_photo_from_json(photo_str, extension)
        path = os.path.join(TEMP_DIR, photo_name)
        save_file(path, photo)

        photo_url = s3.upload_photo(path, photo_name)

        try:
            data["profile_picture_url"] = photo_url
            return CustomerDetailsManager._create_customer_details_in_db(data)
        except Exception:
            s3.delete_photo(photo_name)
        finally:
            os.remove(path)

    @staticmethod
    def get_details(pk):
        customer_details = CustomerDetailsModel.query.filter_by(id=pk).first()
        if not customer_details:
            raise NotFound(f"Details with id: {pk} are not found!")
        return customer_details

    @staticmethod
    def edit(data, pk):
        customer_details = CustomerDetailsManager.get_details(pk)

        photo_str = data.pop("photo") if data.get("photo") else None
        extension = data.pop("extension") if data.get("extension") else None

        CustomerDetailsModel.query.filter_by(id=customer_details.id).update(data)
        if has_photo(photo_str, extension):
            CustomerDetailsManager.change_profile_picture(
                {"photo": photo_str, "extension": extension},
                customer_details.id)

        return customer_details

    @staticmethod
    def change_profile_picture(data, pk):
        customer_details = CustomerDetailsManager.get_details(pk)
        previous_picture = get_photo_name_by_url(customer_details.profile_picture_url)

        photo_name, photo = create_photo_from_json(data.pop('photo'), data.pop("extension"))
        path = os.path.join(TEMP_DIR, photo_name)
        save_file(path, photo)

        photo_url = s3.upload_photo(path, photo_name)

        try:
            data["profile_picture_url"] = photo_url
            CustomerDetailsModel.query.filter_by(id=customer_details.id).update(data)
            if previous_picture:
                s3.delete_photo(previous_picture)
            return customer_details
        except Exception:
            s3.delete_photo(photo_name)
        finally:
            os.remove(path)

    @staticmethod
    def delete_profile_picture(pk):
        customer_details = CustomerDetailsManager.get_details(pk)
        photo = get_photo_name_by_url(customer_details.profile_picture_url)
        if not photo:
            raise NotFound('Profile picture not found!')

        CustomerDetailsModel.query.filter_by(id=customer_details.id).update({"profile_picture_url": None})
        s3.delete_photo(photo)
        return customer_details

    @staticmethod
    def _create_customer_details_in_db(data):
        customer_details = CustomerDetailsModel(**data)
        db.session.add(customer_details)
        db.session.flush()
        return customer_details
