from io import BytesIO

from app.testing import register
from app.testing.types import FactoryProtocol
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


@register
def uploaded_image(self: FactoryProtocol) -> SimpleUploadedFile:
    """Can be used in both DRF API and mixer.
    DRF won't let you use invalid image, so the content is a real image.
    """
    bytes_io = BytesIO()
    Image.new("RGB", size=(10, 10), color=(0, 255, 255)).save(bytes_io, "GIF")
    bytes_io.seek(0)
    image_content = bytes_io.read()
    return SimpleUploadedFile("image.gif", image_content, "image/gif")
