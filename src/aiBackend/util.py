import io

from google.cloud import vision
from PIL import Image
import base64


def crop_seperate_objects(imageStr: str) -> list[str]:
    # Open the original image
    b: bytes = base64.decodebytes(bytes(imageStr, "utf8"))

    original = Image.open(io.BytesIO(b))

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=b)

    objects = client.object_localization(image=image).localized_object_annotations

    cropped_images = []

    # Iterate through each object in the JSON data
    for obj in objects:
        vertices = obj.bounding_poly.normalized_vertices

        # Convert normalized vertices to actual pixel coordinates
        width, height = original.size
        x1 = int(vertices[0].x * width)
        y1 = int(vertices[0].y * height)
        x2 = int(vertices[2].x * width)
        y2 = int(vertices[2].y * height)

        # Crop the image based on the vertices
        cropped = original.crop((x1, y1, x2, y2))
        with io.BytesIO() as buffer:
            cropped.save(buffer, format="JPEG")
            cropped_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            cropped_images.append(cropped_base64)
            buffer.close()

        return cropped_images
