# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.1.0
# Render ambient occlusion of current scene.
import os

def main():
    values = [("folder", lux.DIALOG_FOLDER, "Output folder:", None),
              ("name", lux.DIALOG_TEXT, "Image name:", "occlusion.png"),
              ("width", lux.DIALOG_INTEGER, "Output width:", 800),
              ("height", lux.DIALOG_INTEGER, "Output height:", 800),
              ("time", lux.DIALOG_INTEGER, "Render max time (s):", 10, (1, 86400))]
    opts = lux.getInputDialog(title = "Render Ambient Occlusion",
                              desc = "Render ambient occlusion of current scene.",
                              values = values,
                              id = "renderambientocclusion.py.luxion")
    if not opts: return

    if len(opts["folder"]) == 0:
        raise Exception("Folder cannot be empty!")

    if len(opts["name"]) == 0:
        raise Exception("Image name cannot be empty!")

    env = lux.getEnvironmentImage()
    mmap = lux.getMaterialMapping()

    lux.setEnvironmentImage("All White.hdr")
    for node in lux.getSceneTree().find(""):
        node.setMaterial("Matte White")

    path = os.path.join(opts["folder"], opts["name"])
    width = opts["width"]
    height = opts["height"]

    ropts = lux.getRenderOptions()
    ropts.setMaxTimeRendering(opts["time"])

    lux.renderImage(path = path, width = width, height = height, opts = ropts)

    lux.setEnvironmentImage(env)
    lux.applyMaterialMapping(mmap)

main()
