# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import pyopenpose as op

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--output_path", default="../../examples/output", help="Directory to save the processed output")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../models/"
    params["net_resolution"] = "-1x192"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(args[0].image_path)
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))

    # Print Keypoints
    print("Body keypoints: \n" + str(datum.poseKeypoints))

    # Save Image
    output_dir = args[0].output_path
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, "body_from_image.jpg")
    cv2.imwrite(output_file_path, datum.cvOutputData)
except Exception as e:
    print(e)
    sys.exit(-1)