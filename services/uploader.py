

class Uploader:

    # USER AVATAR
    @staticmethod
    def user_avatar(instance, filename):
        return f"Accounts/Avatars/{filename}"

    # USER COVER IMAGE
    @staticmethod
    def user_cover_image(instance, filename):
        return f"Accounts/Cover-images/{filename}"
    
    # USER CHAT MEDIA
    @staticmethod
    def user_chat_media(instance, filename):
        return f"Accounts/Chat-media/{filename}"


    # SLIDER IMAGE
    @staticmethod
    def slider_image(instance, filename):
        return f"Slider/{filename}"
    
    # Stream IMAGE
    @staticmethod
    def stream_image(instance, filename):
        return f"Stream/{filename}"

    # Product COVER IMAGE
    @staticmethod
    def product_cover_image(instance, filename):
        return f"Products/Cover-images/{filename}"

    # Product ORIGINAL VIDEO
    @staticmethod
    def product_original_video(instance, filename):
        return f"Products/Original-video/{filename}"

    # Product COMPRESS VIDEO
    @staticmethod
    def product_compress_video(instance, filename):
        return f"Products/Compress-video/{filename}"
