# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.1.1
# Renders frames similar to a panoramic VR.
import os
from math import cos, sin, pi

def main():
    values = [("cam", lux.DIALOG_ITEM, "Camera to use:", lux.getCamera(),
               lux.getCameras()),
              ("frames", lux.DIALOG_INTEGER, "#Frames:", 6, (1, 360)),
              ("fmt", lux.DIALOG_TEXT, "Output file format:", "frame.%d.png"),
              ("folder", lux.DIALOG_FOLDER, "Output folder:", None),
              ("width", lux.DIALOG_INTEGER, "Output width:", 800),
              ("height", lux.DIALOG_INTEGER, "Output height:", 800)]
    opts = lux.getInputDialog(title = "Render Panoramic Frames",
                              desc = "Renders frames similar to a panoramic VR. This script assumes the camera is already positioned correctly.",
                              values = values,
                              id = "renderpanframes.py.luxion")
    if not opts: return

    cam = opts["cam"][1]
    frames = opts["frames"]

    fmt = opts["fmt"]
    if len(fmt) == 0:
        raise Exception("Output format cannot be empty!")
    if fmt.find("%d") == -1:
        raise Exception("Output format must contain '%d'!")

    folder = opts["folder"]
    if len(folder) == 0:
        raise Exception("Folder cannot be empty!")

    width = opts["width"]
    height = opts["height"]

    oldcam = lux.getCamera()
    angle = (360 / frames) * pi / 180 # radians

    lux.setCamera(cam)
    for i in range(frames):
        # Rotate around Y-axis by angle.
        dir = lux.getCameraDirection()
        dir = (dir[0] * cos(angle) + dir[2] * sin(angle),
               dir[1],
               -dir[0] * sin(angle) + dir[2] * cos(angle))
        lux.setCameraDirection(dir)

        path = os.path.join(folder, fmt.replace("%d", str(i)))
        print("Rendering {} of {} frames: {}".format(i+1, frames, path))
        lux.renderImage(path = path, width = width, height = height)

    # Reset to old camera.
    lux.setCamera(oldcam)

main()
