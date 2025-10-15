
import roboflow

rf = roboflow.Roboflow(api_key="Wb68uTXkugSzoRdiNY5P")

project = rf.workspace().project("toocandogs")
model = project.version("3").model
# optionally, change the confidence and overlap thresholds
# values are percentages
model.confidence = 20
model.overlap = 25

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

def prediction(file_name):

    return model.predict(file_name).json()
perdiction = prediction('doog.jpg')