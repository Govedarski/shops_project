from constants.Image_suffix import IMAGE_SUFFIX_IN_DB


class ImageMixin:
    """Mixin for all models which has image_url fields in themselves"""

    @classmethod
    def get_all_image_field_names(cls):
        """Returns list of all model field's names"""
        return [x[0:-len(IMAGE_SUFFIX_IN_DB)] for x in cls.__dict__.keys() if x.endswith(IMAGE_SUFFIX_IN_DB)]
