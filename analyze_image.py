from vertexai.vision_models import ImageQnAModel, Image
import threading
import os

def task1():
    print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 1: {}".format(os.getpid()))
 
def task2():
    print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 2: {}".format(os.getpid()))

def analyze_image(image_path):
    model = ImageQnAModel.from_pretrained("imagetext@001")

    image = Image.load_from_file(image_path)

    object_type = threading.Thread(model.ask_question, args=('image', 'What object is in the image?', 3))
    # object_type = model.ask_question(
    #     image=image,
    #     question="What object is in the image? ",
    #     # Optional:
    #     number_of_results=3,
    # )

    object_material = threading.Thread(model.ask_question, args=('image', 'What materials is this object made up of?', 3))
    # object_material = model.ask_question(
    #     image=image,
    #     question="What materials is this object made up of?",
    #     # Optional:
    #     number_of_results=3,
    # )

    print(object_type)
    print(object_material)

    return object_type, object_material


# creating threads
t1 = threading.Thread(target=task1, name='t1')
t2 = threading.Thread(target=task2, name='t2')

# starting threads
t1.start()
t2.start()

# wait until all threads finish
t1.join()
t2.join()

analyze_image('artifacts/cropped_0.jpg')
analyze_image('artifacts/cropped_1.jpg')

