import sys, os, glob, json
from wasteDetection.pipeline.training_pipeline import TrainPipeline
from wasteDetection.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template, Response, send_from_directory
from flask_cors import CORS, cross_origin
from wasteDetection.constant.application import APP_HOST, APP_PORT

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

def get_latest_output_file(base_path="yolov3/runs/detect"):
    try:
        # Get all subdirectories in the detect folder
        list_of_dirs = glob.glob(f"{base_path}/*")
        if not list_of_dirs:
            raise FileNotFoundError("No output directories found in runs/detect")

        # Find the most recent directory
        latest_dir = max(list_of_dirs, key=os.path.getmtime)
        predicted_image_path = os.path.join(latest_dir, "inputImage.jpg")

        if not os.path.exists(predicted_image_path):
            raise FileNotFoundError(f"Predicted image not found in {latest_dir}")

        return predicted_image_path
    except Exception as e:
        print(f"Error locating output file: {e}")
        raise

@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return "Training Successful!!" 


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
def predictRoute():
    try:
        # Process the image and run prediction
        image = request.json['image']
        decodeImage(image, clApp.filename)

        # Run your YOLO detection script
        os.system("cd yolov3/ && python detect.py --weights best.pt --img 416 --conf 0.5 --source ../data/inputImage.jpg")

        # Encode the output image into base64
        output_image_path = "yolov3/runs/detect/exp/inputImage.jpg"
        opencodedbase64 = encodeImageIntoBase64(output_image_path)

        # Load the JSON detections
        with open("yolov3/runs/detect/exp/inputImage.json", "r") as f:
            detections = json.load(f)

        # Return the JSON response
        result = {
            "image": opencodedbase64.decode('utf-8'),
            "detections": detections
        }

        return jsonify(result)

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": str(e)})


@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        os.system("cd yolov3/ && python detect.py --weights best.pt --img 416 --conf 0.5 --source 0")
        os.system("rm -rf yolov3/runs")
        return "Camera starting!!" 
    except ValueError as val:
        print(val)
        return Response("Value not found inside json data")


if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host=APP_HOST, port=APP_PORT)
