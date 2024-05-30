

class Uploader:

    # USER AVATAR
    @staticmethod
    def user_avatar(instance, filename):
        return f"Accounts/Avatars/{filename}"

    # USER COVER IMAGE
    @staticmethod
    def user_cover_image(instance, filename):
        return f"Accounts/Cover-images/{filename}"

    # SLIDER IMAGE
    @staticmethod
    def slider_image(instance, filename):
        return f"Slider-Image/{filename}"
