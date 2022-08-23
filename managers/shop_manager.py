import itertools

from sqlalchemy.exc import InvalidRequestError
from werkzeug.exceptions import Forbidden

from managers.crud_manager import CRUDManager
from models import UserRoles
from utils import helpers


class ShopManager(CRUDManager):
    PERMISSION_DENIED_MESSAGE = "Permission denied!"
    DELETE_DENIED_MESSAGE = "Cannot delete verified shop!"

    @classmethod
    def get(cls, model, pk, **kwargs):
        user = kwargs.get('user')
        shop = cls._get_instance(model, pk)
        if helpers.is_admin(user) or helpers.is_holder(shop, UserRoles.owner, user) or shop.active:
            return shop
        raise Forbidden(cls.PERMISSION_DENIED_MESSAGE)

    @classmethod
    def get_list(cls, model, criteria, **kwargs):
        user = kwargs.get('user')
        try:
            return cls._fetch_data(model, criteria, user)
        except InvalidRequestError:
            # not sure empty list or BadRequest
            return []

    @classmethod
    def delete(cls, model, pk, **kwargs):
        shop = cls._get_instance(model, pk)
        if shop.verified:
            raise Forbidden(cls.DELETE_DENIED_MESSAGE)
        return super().delete(model, pk)

    @staticmethod
    def _fetch_data(model, criteria, user):
        # if not auth user or customer return shops by criteria which are active
        if not user or user.role == UserRoles.customer:
            criteria = criteria | {"active": True}
            return model.query.filter_by(**criteria).all()

        # if admin return all shops by criteria
        if helpers.is_admin(user):
            return model.query.filter_by(**criteria).all()

        # Here user role is shop_owner
        holder_shops = []
        # if user want not specified holder or want his own shop fetch his shops from db by criteria
        if not criteria.get('holder_id') or criteria.get('holder_id') == user.id:
            holder_criteria = criteria | {"holder_id": user.id}
            holder_shops = model.query.filter_by(**holder_criteria).all()

        # if user do not want his own shops fetch the rest shops by criteria which are active
        foreign_shops = []
        if not criteria.get('holder_id') == user.id:
            foreign_criteria = criteria | {"active": True}
            foreign_shops = model.query.filter_by(**foreign_criteria).all()

        # fastest way to remove duplicates in python according to
        # https://stackoverflow.com/questions/1675321/fastest-way-to-remove-duplicates-in-lists-python
        return set(itertools.chain(holder_shops, foreign_shops))
