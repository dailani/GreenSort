import io

from google.cloud import vision
from PIL import Image
import base64


def crop_seperate_objects(image_str: str) -> list[str]:
    # Open the original image
    b: bytes = base64.decodebytes(bytes(image_str, "utf8"))
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


##caus python
from vertexai.vision_models import ImageQnAModel, Image as vertexaiImage


def analyze_image(image_str: str) -> dict[str, list[str]]:
    model = ImageQnAModel.from_pretrained("imagetext@001")

    b: bytes = base64.decodebytes(bytes(image_str, "utf8"))
    image = vertexaiImage(b)

    # object_type = threading.Thread(model.ask_question, args=('image', 'What object is in the image?', 3))
    object_type = model.ask_question(
        image=image,
        question="What object is in the image? ",
        # Optional:
        number_of_results=3,
    )

    # object_material = threading.Thread(model.ask_question,args=('image', 'What materials is this object made up of?', 3))
    object_material = model.ask_question(
        image=image,
        question="What materials is this object made up of?",
        # Optional:
        number_of_results=3,
    )
    response_data = {
        'things': object_type,
        'material': object_material
    }

    return response_data
