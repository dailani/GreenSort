import io
from typing import Dict, List

import vertexai
from vertexai.language_models import TextGenerationModel

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

def getcategory(material: list[str],things:list[str]) :
    m = ", ".join(material)

    t = ", ".join(things)

    vertexai.init(project="collabothon23fra-1264", location="us-central1")
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 1
    }
    model = TextGenerationModel.from_pretrained("text-bison")

    response = model.predict(f"""Multi-choice problem: 
    Which category(s) could this object belong to?
    Please only use the following categories: 
    Drain cleaner
    ,Battery | Rechargeable battery
    ,File/Data destruction
    ,File folder
    ,Recyclable glass
    ,Old clothes | Shoes
    ,Used oil
    ,Old tires
    ,Aluminum foil
    ,Dental amalgam
    ,Ammonia
    ,Aquarium/Terrarium (carriable by one person)
    ,Asbestos
    ,Ash
    ,Car roof box
    ,Car bicycle rack
    ,Car luggage rack
    ,Car child seat
    ,Slot car racing track
    ,Cars | Car parts
    ,Baking mold
    ,Oven
    ,Baking paper
    ,Bathroom fixtures
    ,Railway sleepers
    ,Construction waste mix
    ,Tree trunk
    ,Rubble
    ,Side table
    ,Gasoline canister
    ,Cutlery
    ,Duvet | packaged
    ,Bed frame
    ,Bed drawer
    ,Bed linen
    ,Beer tent set
    ,Picture frames | Canvases
    ,Pool table
    ,Organic waste
    ,Biodegradable trash bags
    ,Bitumen
    ,Bleach
    ,Lead foil
    ,Flowers
    ,Potting soil
    ,Flower box/Flower pot | Plastic, metal, untreated wood
    ,Flower box/Flower pot | Clay
    ,Floor coverings
    ,Boiler
    ,Brake fluid
    ,Bread
    ,Ironing board
    ,CD | DVD
    ,Chemical toilet
    ,Chemicals
    ,Computer
    ,Coronavirus test
    Couch | Sofa
    ,Roof antennas/Satellite dishes
    ,Roofing felt
    ,Roof tiles
    ,Mineral wool insulation material
    ,Disinfectant
    ,Floppy disk
    ,Latex paint
    ,Cans
    ,Tricycle
    ,Printer/Copier/Fax machine
    ,Printer cartridge
    ,Fertilizer
    ,Instantaneous water heater
    ,Disposable e-cigarettes
    ,Disposable tableware
    ,Electric grill
    ,Large electrical appliance (Washing machine, tumble dryer, refrigerator, etc.)
    ,Small electrical devices
    ,Energy-saving bulb
    ,Descaler
    ,Excavated soil
    ,Bicycle
    ,Bike trailer
    ,Bicycle child seat
    ,Bike tires
    ,Folding boat | dismantled
    ,Wheel rim
    ,Window
    ,Television
    ,Fire extinguisher
    ,Fireworks
    ,Wing/Piano | Wing dismantled
    ,Foil
    ,Coat rack
    ,Curtain rod
    ,Garden tool
    ,Garden shed
    ,Garden furniture | Treated wood
    ,Garden furniture | Plastic, metal, and untreated wood
    ,Garden hose
    ,Gas cartridge
    ,Gift ribbon
    ,Gift paper
    ,Dishware
    ,Beverage carton
    ,Poison
    ,Glass block
    ,Glass plates from furniture (except table glass plates)
    ,Glass pane
    ,Light bulb
    ,Grill | Gas grill without gas bottle
    ,Charcoal
    ,Garden waste
    ,Rubber
    ,Hairbrush
    ,Hair
    ,Hand cart
    ,Pet cage | Outside
    ,Pet cage | Inside
    ,Heater | Electric
    ,Heater | Non-electric
    ,Heating oil
    ,Patio heater
    ,Hollow glass
    ,Hollywood swing | dismantled
    ,Wood | treated
    ,Pallet wood furniture | uncontaminated
    ,Wooden furniture | treated
    ,Wooden furniture | untreated
    ,Wooden pallet
    ,Wood preservative
    ,Wooden toy
    ,Wood | untreated
    ,Hygiene paper
    ,Insect spray
    ,Insulated jug
    ,Blind | Exterior
    ,Blind | Interior
    ,Yogurt cup
    ,Cable
    ,Coffee filter
    ,Coffee capsule
    ,Cardboard
    ,Cassette
    ,Ceramics and porcelain
    ,Candle
    ,Stroller
    ,Cushion
    ,Box | Treated wood
    ,Box | Metal, plastic, untreated wood
    ,Clear plastic sleeve
    ,Tape
    ,Glue
    ,Small animal litter
    ,Bone
    ,Cooktop
    ,Suitcase
    ,Coal
    ,Recyclable Plastic
    ,Recyclable Glass
    ,Recyclable Paper

    Text: 
    objects: [\'laptop\', \'macbook air\', \'laptop computer\'],
    object_materials: [\'aluminium\', \'macbook air\', \'metal\']

    The answer is: [Computer]

    Text: objects: [\'person\', \'man\', \'glasses\'], object_materials: [\'plastic\', \'glass\', \'metal\']
    The answer is: [Organic waste, Recyclable Plastic]

    Text: object_type:[\'bottle\', \'wine bottle\', \'klar\'], object_material:[\'glass\', \'plastic\', \'bottle\']
    The answer is: [Recyclable Plastic, Recyclable Glass]

    Text: object_type:[\'bottle\', \'glass bottle\', \'empty bottle\'], object_material:[\'glass\', \'clear glass\', \'plastic\']
    The answer is: [Recyclable Plastic, Recyclable Glass]

    Text: object_type:[\'bowl\', \'container\', \'plastic container\'], object_material:[\'plastic\', \'clear plastic\', \'plastic container\']
    The answer is: [Recyclable Plastic]

    Text: object_type:[\'bowl\', \'container\', \'paper towel\'], object_material:[\'plastic\', \'paper\', \'paper towels\']
    The answer is: [Recyclable Plastic, Recyclable Paper]

    Text: object_type:[\'person\', \'man\', \'desk\'], object_material:[\'plastic\', \'wood\', \'metal\']
    The answer is: [Organic waste, Pallet wood furniture | uncontaminated, Wooden furniture | treated, Wooden furniture | untreated ]

    Text: object_type:[\'bottle\', \'spray bottle\', \'spray\'], object_material:[\'plastic\', \'unanswerable\', \'plastik\']
    The answer is: [Recyclable Plastic]

    Text: object_type:[\'chair\', \'armchair\', \'pillow\'], object_material:[\'fabric\', \'linen\', \'cotton\']
    The answer is: [Couch | Sofa]

    Text: object_type:[\'pepsi\', \'pepsi can\', \'can\'], object_material:[\'metal\', \'pepsi\', \'aluminum\']
    The answer is: [Cans]

    Text: object_type:[\'pool table\', \'snooker table\', \'pool\'], object_material:[\'pool table\', \'wood\', \'velvet\']
    The answer is: [Wooden furniture | treated]

    Text: object_type:[\'marker\', \'blue marker\', \'schneider marker\'], object_material:[\'plastic\', \'germany\', \'paper\']
    The answer is: [Recyclable Plastic]

    Text: object_type:['box', 'cardboard box', 'unanswerable'], object_material:['cardboard', 'paper', 'wood']
    The answer is: [Cardboard]

    Text: object_type:{t}, object_material:{m}
    The answer is: """, **parameters)

    return response.text
    #print(f"Response from Model: {response.text}")
