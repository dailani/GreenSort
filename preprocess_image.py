from google.cloud import vision
from PIL import Image

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations
            
    return objects

def crop_seperate_objects(objects, image_path):
        # Open the original image
    original = Image.open(image_path)
    
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
        cropped_images.append(cropped)

        for i, cropped in enumerate(cropped_images):
            cropped.save(f'artifacts/cropped_{i}.jpg')
    
def test_function(path):
    objects = localize_objects(path)
    crop_seperate_objects(objects, path)

test_function('artifacts/etrash.jpeg')