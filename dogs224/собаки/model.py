
'''import roboflow


def model_initialization(projectname = "toocandogs",api="Wb68uTXkugSzoRdiNY5P", version = "3"):
    rf = roboflow.Roboflow(api_key="Wb68uTXkugSzoRdiNY5P")

    project = rf.workspace().project("toocandogs")
    model = project.version("4").model
    # optionally, change the confidence and overlap thresholds
    # values are percentages
    model.confidence = 20
    model.overlap = 25
    return model
# # predict on a local image
# perdiction = model.predict('doog.jpg')
# #
# #
# #
# # Predict on a hosted image via URL
# # prediction = model.predict("https://...", hosted=True)
# print(type(perdiction))
# print(perdiction)
# # Plot the prediction in an interactive environment
# perdiction.plot()

# Convert predictions to JSON

def prediction(file_name, model):

    return model.predict(file_name).json()
#perdiction = prediction('doog.jpg')
'''
from inference import get_model

# Load model (downloads and caches weights)
model = get_model(
    model_id="toocandogs/4",
    api_key="Wb68uTXkugSzoRdiNY5P"
)
print("Model weights cached!")
image = "умка.jpg"
results = model.infer(image)
print(results)
'''from inference import get_model
import supervision as sv
import cv2

# define the image url to use for inference
image_file = "doog.jpg"
image = cv2.imread(image_file)

# load a pre-trained rfdetr model
model = get_model(model_id="toocandogs/4")

# run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
print(results)
'''
'''
# import the inference-sdk
from inference_sdk import InferenceHTTPClient

# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="Wb68uTXkugSzoRdiNY5P"
)
print(CLIENT)
print(CLIENT.get_model_description("toocandogs/4"))
# infer on a local image
result = CLIENT.infer("doog.jpg", model_id="toocandogs/4")
print(result)
'''
