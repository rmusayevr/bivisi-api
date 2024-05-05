

class Uploader:

    # USER AVATAR
    @staticmethod
    def user_avatar(instance, filename):
        return f"USER-AVATAR/{instance.username}/{filename}"

    # SLIDER IMAGE
    @staticmethod
    def slider_image(instance, filename):
        return f"Slider-Image/{filename}"
