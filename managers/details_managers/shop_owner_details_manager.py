from managers.base_manager import BaseManager
from models import ShopOwnerDetailsModel
from utils.helpers import is_admin


class ShopOwnerDetailsManager(BaseManager):
    MODEL = ShopOwnerDetailsModel
    UNIQUE = True

    def edit(self, data, pk, **kwargs):
        self._check_access(pk, **kwargs)

        details = self._get_instance(pk)
        user = kwargs.get('user')
        if is_admin(user):
            return super().edit(data, pk, **kwargs)

        if details.verified:
            fields = ("confirm_identity_documents_photo", "confirm_identity_documents_extension")
            [data.pop(field) for field in fields if data.get(field) is not None]

        return super().edit(data, pk, **kwargs)
