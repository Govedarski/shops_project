from sqlalchemy.exc import InvalidRequestError
from werkzeug.exceptions import Forbidden, NotFound, BadRequest

from managers.base_manager import BaseManager
from models import UserRoles, ShopModel
from utils import helpers
from utils.helpers import is_admin


class ShopManager(BaseManager):
    MODEL = ShopModel
    DELETE_DENIED_MESSAGE = "Cannot delete verified shop!"
    NOT_FOUND_MESSAGE = "Page not found!"
    NAME_ERROR_MESSAGE = "Cannot change name of verified resource! Please contact admin!"
    BULSTAT_ERROR_MESSAGE = "Cannot change bulstat of verified resource! Please contact admin!"

    def get(self, pk, **kwargs):
        self._check_access(pk, **kwargs)

        user = kwargs.get('user')
        shop = self._get_instance(pk)
        if helpers.is_admin(user) or helpers.is_holder(shop, UserRoles.owner, user) or shop.active:
            return shop
        raise NotFound(self.NOT_FOUND_MESSAGE)

    def get_list(self, criteria, **kwargs):

        user = kwargs.get('user')
        try:
            return self._fetch_data(self.get_model(), criteria, user)
        except InvalidRequestError:
            # not sure empty list or BadRequest
            return []

    def edit(self, data, pk, **kwargs):
        self._check_access(pk, **kwargs)

        shop = self._get_instance(pk)
        user = kwargs.get('user')
        if is_admin(user):
            return super().edit(data, pk, **kwargs)

        if shop.verified and data.get("name") and not data["name"] == shop.name:
            raise BadRequest(self.NAME_ERROR_MESSAGE)
        if shop.verified and data.get("bulstat") and not data["bulstat"] == shop.bulstat:
            raise BadRequest(self.NAME_ERROR_MESSAGE)
        if shop.verified:
            fields = ("name", "bulstat", "verifying_documents_photo", "verifying_documents_extension")
            [data.pop(field) for field in fields if data.get(field) is not None]

        return super().edit(data, pk, **kwargs)

    def delete(self, pk, **kwargs):
        self._check_access(pk, **kwargs)

        shop = self._get_instance(pk)
        if shop.verified:
            raise Forbidden(self.DELETE_DENIED_MESSAGE)
        return super().delete(pk)

    def get_shops_by_ids(self, ids):
        return self.get_model().query.filter(ShopModel.id.in_(ids)).all()

    @staticmethod
    def _fetch_data(model, criteria, user):
        # if not auth user or customer return shops by criteria which are active
        if not user or user.role == UserRoles.customer:
            criteria = criteria | {"active": True}
            return model.query.filter_by(**criteria).all()

        # if admin return all shops by criteria
        if helpers.is_admin(user):
            return model.query.filter_by(**criteria).all()

        # if user want his own shop fetch his shops
        if criteria.get('holder_id') == user.id:
            return model.query.filter_by(**criteria).all()

        # if user want all shop fetch his shops and all the rest which are active
        if not criteria.get('holder_id'):
            user_shops = []
            if not criteria.get('active'):
                holder_criteria = criteria | {"holder_id": user.id, "active": False}
                user_shops = model.query.filter_by(**holder_criteria).all()

            foreign_criteria = criteria | {"active": True}
            foreign_shops = model.query.filter_by(**foreign_criteria).all()
            return user_shops + foreign_shops

        # if user do  want someone else shops fetch shops by criteria which are active
        if not criteria.get('holder_id') == user.id:
            foreign_criteria = criteria | {"active": True}
            return model.query.filter_by(**foreign_criteria).all()
