from django.core.exceptions import ValidationError


def image_size(image):
    max_size = 2000
    if image.size > (max_size * 1024):
        raise ValidationError(f'image size must be less than {max_size}KB!!')
