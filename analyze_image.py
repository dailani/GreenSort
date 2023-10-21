from vertexai.vision_models import ImageQnAModel, Image

def analyze_image(image_path):
    model = ImageQnAModel.from_pretrained("imagetext@001")

    image = Image.load_from_file(image_path)

    object_type = model.ask_question(
        image=image,
        question="What object is in the image? ",
        # Optional:
        number_of_results=3,
    )
    object_material = model.ask_question(
        image=image,
        question="What materials is this object made up of?",
        # Optional:
        number_of_results=3,
    )

    print(object_type)
    print(object_material)

    return object_type, object_material





analyze_image('artifacts/cropped_0.jpg')
analyze_image('artifacts/cropped_1.jpg')

