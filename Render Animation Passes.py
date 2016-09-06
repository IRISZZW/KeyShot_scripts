# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.2.0
# Renders animation frames with optional passes.
import os

def ambOcclusionPass():
    lux.setEnvironmentImage("All White.hdr")
    for node in lux.getSceneTree().find(""):
        node.setMaterial("Matte White")

def toonShaderPass():
    for node in lux.getSceneTree().find(""):
        node.setMaterial("Toon Outline Black")

def render(folder, fmt, frame, pass_, width, height, env, mmap):
    fmt = fmt.replace("%d", str(frame)).replace("%s", pass_)
    path = os.path.join(folder, fmt)
    lux.renderImage(path = path, width = width, height = height)
    lux.setEnvironmentImage(env)
    lux.applyMaterialMapping(mmap)

def main():
    frames = lux.getAnimationInfo()["frames"]
    if frames == 0:
        raise Exception("No animation in scene! Please create one and try again.")

    values = [("folder", lux.DIALOG_FOLDER, "Output folder:", None),
              ("fmt", lux.DIALOG_TEXT, "Output file format:", "frame.%d.%s.jpg"),
              ("width", lux.DIALOG_INTEGER, "Output width:", 800),
              ("height", lux.DIALOG_INTEGER, "Output height:", 800),
              ("start", lux.DIALOG_INTEGER, "Start frame:", 1, (1, frames)),
              ("end", lux.DIALOG_INTEGER, "End frame:", 10, (1, frames)),
              (lux.DIALOG_LABEL, "---"),
              (lux.DIALOG_LABEL, "Passes:"),
              ("occl", lux.DIALOG_CHECK, "Ambient occlusion", True),
              ("toon", lux.DIALOG_CHECK, "Toon outline shading", True)]
    opts = lux.getInputDialog(title = "Render Animation Passes",
                              desc = "Render animation frames with optional passes.",
                              values = values,
                              id = "renderanimationpasses.py.luxion")
    if not opts: return

    if len(opts["folder"]) == 0:
        raise Exception("Folder cannot be empty!")
    fld = opts["folder"]

    fmt = opts["fmt"]
    if len(fmt) == 0:
        raise Exception("Output format cannot be empty!")
    if fmt.find("%d") == -1:
        raise Exception("Output format must contain '%d' to express the frame number!")
    if fmt.find("%s") == -1:
        raise Exception("Output format must contain '%s' to express the pass!")

    width = opts["width"]
    height = opts["height"]

    start = opts["start"]
    end = opts["end"]
    if start > end:
        raise Exception("Start frame cannot be larger than end frame!")

    if not opts["occl"] and not opts["toon"]:
        raise Exception("You must select at least one pass!")

    env = lux.getEnvironmentImage()
    mmap = lux.getMaterialMapping()

    for frame in range(start, end+1):
        lux.setAnimationFrame(frame)

        # Passes to apply.
        if opts["occl"]:
            ambOcclusionPass()
            render(fld, fmt, frame, "occl", width, height, env, mmap)

        if opts["toon"]:
            toonShaderPass()
            render(fld, fmt, frame, "toon", width, height, env, mmap)

main()
