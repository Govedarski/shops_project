import itertools

from sqlalchemy.exc import InvalidRequestError

from models import AdminRoles, UserRoles


class ShopManager:
    @classmethod
    def get_list(cls, model, criteria, **kwargs):
        user = kwargs.get('user')
        try:
            return cls._fetch_data(model, criteria, user)
        except InvalidRequestError:
            # not sure empty list or BadRequest
            return []

    @staticmethod
    def _fetch_data(model, criteria, user):
        # if not auth user or customer return shops by criteria which are active
        if not user or user.role == UserRoles.customer:
            criteria = criteria | {"active": True}
            return model.query.filter_by(**criteria).all()

        # if admin return all shops by criteria
        if user.role in AdminRoles:
            return model.query.filter_by(**criteria).all()

        # Here user role is shop_owner
        holder_shops = []
        # if user want not specified holder or want his own shop fetch his shops from db by criteria
        if not criteria.get('holder_id') or criteria.get('holder_id') == user.id:
            holder_criteria = criteria | {"holder_id": user.id}
            holder_shops = model.query.filter_by(**holder_criteria).all()

        # if user don't want his own shops fetch the rest shops by criteria which are active
        foreign_shops = []
        if not criteria.get('holder_id') == user.id:
            foreign_criteria = criteria | {"active": True}
            foreign_shops = model.query.filter_by(**foreign_criteria).all()

        # fastest way to remove duplicates in python according to
        # https://stackoverflow.com/questions/1675321/fastest-way-to-remove-duplicates-in-lists-python
        return set(itertools.chain(holder_shops, foreign_shops))
