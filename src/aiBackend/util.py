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
    Battery,
    Old batteries,
    Filing folder,
    Alarm system,
    Alteisen,
    Old glass,
    Old dresses,
    Old oil,
    Waste paper,
    Tire,
    Aluminium,
    Antenna,
    Aquarium,
    drug,
    Asbestos,
    ash,
    Car battery,
    Autofelgen,
    Machine,
    car tire,
    Auto parts,
    oven,
    Bathtub,
    Batteries,
    Construction,
    Building rubble,
    stain,
    clothing,
    lighting,
    Lighting body,
    Petrol,
    Bed,
    Bed linen,
    Bioabfall,
    Screen devices,
    Bleechs, sheet metal parts,
    Lead batteries,
    Flower boxes,
    Flower pots,
    Floor coverings,
    Boiler,
    drilling machine,
    Fire protection system,
    frying pan,
    brake fluid,
    Bread maker,
    Books,
    Iron,
    Ceranfeld,
    Chemical,
    Computer/PC,
    Computer scrap,
    Computer parts,
    Couch,
    Roofing felt,
    Roof tile,
    Insulation,
    Ceiling slabs,
    Disinfectant,
    Dislike,
    Dispersion,
    Display,
    tricycle,
    Drucker, Toner,
    Printer cartridges,
    Extractor hood,
    DVD - Player,
    Owner kocher,
    Equipped kitchen,
    Iron parts,
    Cupboard,
    Ice cube leaders,
    Electrical devices,
    Elektrooboiler,
    Electrical appliances,
    Elektrogrill,
    Electric stove,
    Electrocular,
    Electrical cleaning devices,
    Electric motors,
    Electronic,
    Electro,
    Power tool,
    Energy -saving lamps,
    epilator,
    Erdaushub,
    Espresso machine,
    Leftovers,
    Bicycle, bicycles,
    Bicycle parts,
    Colors, color buckets,
    fax machine,
    rims,
    Window, window frame,
    TV,
    hard disk,
    Slices,
    Fire extinguisher,
    Fieberhermometer,
    Fitness equipment,
    Flachglas,
    Bottle,
    Meat,
    Tiles,
    Tile cutter,
    hairdryer,
    Foil,
    Foil welding device,
    Camera,
    Photos, photo paper,
    Photolor,
    Deep fryer,
    Frost protection,
    Garden waste,
    Garden tools,
    Gardening,
    garden furniture,
    garden fence,
    Gasentladungs ​​lamps,
    Gas devices,
    Gasofen,
    Gas bottles,
    Gas cartridges,
    Gas grill,
    Host,
    Freezer,
    freezer,
    freezer,
    Slot machine,
    Dishes,
    dishwasher,
    Machinery machine,
    Gips, Gipskarton,
    Smoothing iron,
    Vote,
    Mususteine,
    Glass fiber products,
    Glass wolle,
    Glass,
    Light bulb,
    Grass section, green section,
    Grill, grill accessories,
    Green waste,
    Rubber,
    Hairdryer,
    Halogen lamp,
    Handy,
    Household batteries,
    Household appliances,
    Household appliances,
    Heimorgel,
    Home trainer,
    Heißmangel,
    heating system,
    radiator,
    Heating oil,
    Radiator,
    Heating,
    Herd,
    Hi-fi systems,
    Hi-fi devices,
    high pressure cleaner,
    Hollywoodschaukel,
    Wood,
    Wood preservative,
    Hometrainer,
    Dog droppings,
    Impregnation,
    Induction stove,
    Induction hob,
    Insect spray,
    Insulating can,
    insulating material,
    It devices,
    Jägerzaun,
    Jealousy,
    Yoghurt cup,
    Cable,
    Tile,
    coffee machine,
    coffee grinder,
    Cage,
    Kartonage,
    Cassettes,
    Cash register,
    In the catalog,
    cat litter,
    Bend,
    Candles,
    stroller,
    Piano,
    Adhesive tapes,
    adhesive,
    Clothing,
    Priority,
    climbing frame,
    air conditioner,
    Climatic car,
    Air conditioner,
    Bone,
    Button,
    Kocher,
    Hob, hob,
    Pot, cookware,
    Suitcase,
    Capacitors,
    Consetce,
    Convectomate,
    Pillow,
    Copy,
    Copy,
    Cork, nature,
    Cosmetics,
    Kitchen,
    Kitchen appliances,
    Kitchen,
    Radiator,
    Cooling system,
    Refrigerator,
    Refrigerator,
    Freezer,
    Synthetic resin,
    Plastics,
    Plastic packaging,
    Lacquer,
    charger,
    Laminate,
    Lamp,
    Laptop,
    glaze,
    Slatted frame,
    Laub,
    Wheel,
    drive,
    Lauge,
    Groceries,
    LED bulbs,
    Manager,
    Leadership,
    glue,
    Director,
    Fluorescent tubes,
    fairy lights,
    Lithiumbatterien,
    Curling,
    solvent,
    Air filter,
    awning,
    Mattress,
    Medication,
    Messer,
    Measuring device,
    Metal,
    Metal scrap,
    Metal parts,
    microwave,
    Milk frother,
    Milk bag,
    Mineral wool,
    Mixer,
    Furniture,
    Furniture polish,
    Modem,
    Engine,
    Motorcycle tires,
    Motorcycle parts,
    Mouse,
    Munition,
    Musical instrument,
    Night storage stoves,
    Nail,
    Nail polish,
    sewing machine,
    Negative,
    Neon tube,
    power adapter,
    Ni-CD Batterieen,
    Nitroverdener,
    Notebook,
    OBSTRESTE,
    Oven,
    Oil filter,
    The beer,
    Elaps,
    Beer radiator,
    Beer tank,
    Packpapier,
    Pallet,
    Palisade,
    Paper,
    cardboard,
    Screen,
    parquet,
    Pesticides,
    PET bottles,
    Pans,
    Plant,
    Pesticide,
    Brush cleaner,
    Pizza oven,
    Playstation,
    plastic cup,
    Plastic cutlery,
    Plastic objects,
    Plastic cabinet,
    Plastic belt,
    Boost,
    plastic bags,
    Record player,
    Upholstered furniture,
    porcelain,
    Postcards,
    On the prospectus,
    PU foam cans,
    Cleaning agent,
    PVC-Boden,
    Type of waste,
    Mercury thermometer,
    Mercury stamping lamps,
    Radiator,
    Radio, radio recorder,
    Radiocker,
    mowing machine,
    razor,
    Room spray,
    Receiver,
    Regal,
    Regents,
    Tires,
    cleaning supplies,
    Rice cooker,
    Rigip plate,
    pipe cleaner,
    Role grains,
    Roller,
    wheelchair,
    X -rays,
    Rustless,
    Rust protection,
    Red light lamp,
    Router,
    soot,
    Sawing,
    acid,
    Safe,
    Sandpit,
    Sandwichmaker,
    Oxygen bottles,
    Pest control,
    Pollutants,
    Record,
    Record player,
    Rocking chair,
    Foammum,
    Foam,
    Slingshot,
    Sleds,
    folder,
    Wardrobe,
    Screw,
    Desk,
    Shoes,
    Second adhesive,
    Armchair,
    Side by Side,
    Ski,
    Snowboard,
    Sofa,
    Solar systems,
    Solar cells,
    Sunbed,
    parasol,
    Chipboard,
    Food fat, food oil,
    Dining,
    Bulky waste,
    Spiegel,
    Gaming,
    Game console,
    toys,
    Spirit,
    Spray can,
    Sports equipment,
    Spray,
    kitchen sink,
    dishwasher,
    Blender,
    Vacuum cleaner,
    Floor lamp,
    Streusplit,
    Chair, chairs,
    Styrofoam,
    surfboard,
    Tannenbaum,
    Mat,
    Wallpaper,
    calculator,
    Diving equipment,
    Telephone,
    Telecommunications devices,
    Carpet,
    Carpet glue,
    Terpentine,
    Thermomet is electricity.,
    Thermostat,
    Tierkadaver,
    Tier,
    Table,
    table tennis table,
    Toaster,
    Toilet lid,
    Transformer,
    Treasure,
    Wood,
    dryer,
    Type,
    Door frame,
    Door frame,
    TV,
    Weed killer,
    Underbody protection,
    Consumer electronics,
    Vacuumer,
    Ventilator,
    Video system,
    Video box,
    Camcorder,
    Video recorder,
    Bird bar,
    Waffle iron,
    weapons,
    Wall cladding,
    Heat bottle,
    Bathroom sink,
    Wasolate,
    Laundry,
    Crawl,
    Washing slider,
    Tumble dryer,
    Wall lamp,
    washing machine,
    laundry detergent,
    Water filter,
    Kettle,
    Toilet pool,
    WC cleaner,
    Alarm clock,
    Christmas tree,
    Tool electr.,
    Wii consoles Controler,
    Xbox Konsole Controler,
    cement,
    brick,
    Zinkers,
    Zink,
    Spark plugs.

    Text: objects: ['laptop', 'macbook air', 'laptop computer'], object_materials: ['aluminium', 'macbook air', 'metal']
    Categories: [Computer]

    Text: objects: ['person', 'man', 'glasses'], object_materials: ['plastic', 'glass', 'metal']
    Categories: [Meat, Plastic objects, Glass]

    Text: object_type:['bottle', 'wine bottle', 'klar'], object_material:['glass', 'plastic', 'bottle']
    Categories: [Glass, Plastic objects]

    Text: object_type:['bottle', 'glass bottle', 'empty bottle'], object_material:['glass', 'clear glass', 'plastic']
    Categories: [Glass, Plastic objects]

    Text: ['bowl', 'container', 'plastic container'], object_material:['plastic', 'clear plastic', 'plastic container']
    Categories: [Paper, Plastic objects]

    Text: ['person', 'man', 'desk'], object_material:['plastic', 'wood', 'metal']

    Categories: [Plastic objects, Wood, Metal]

    Text: object_type:['bottle', 'spray bottle', 'spray'], object_material:['plastic', 'unanswerable', 'plastik']
    Categories: [Plastic objects, Spray]

    Text: object_type: ['chair', 'armchair', 'pillow'], object_material:['fabric', 'linen', 'cotton']
    Categories: [Chair, Couch, Clothing]

    Text: object_type:['pepsi', 'pepsi can', 'can'], object_material:['metal', 'pepsi', 'aluminum']
    Categories: [Metal, Aluminium]

    Text: object_type:['pool table', 'snooker table', 'pool'], object_material:['pool table', 'wood', 'velvet']
    Categories: [Wood, Couch]

    Text: object_type:['pool table', 'snooker table', 'pool'], object_material:['pool table', 'wood', 'velvet']
    Categories: [Wood, Table]

    Text: object_type:['marker', 'blue marker', 'schneider marker'], object_material:['plastic', 'germany', 'paper']
    Categories: [Plastic objects]

    Text: object_type:['box', 'cardboard box', 'unanswerable'], object_material:['cardboard', 'paper', 'wood']
    Categories: [cardboard, Paper, Wood]


    Text: object_type:{t}, object_material:{m}
    The answer is: """, **parameters)

    return response.text
    #print(f"Response from Model: {response.text}")
