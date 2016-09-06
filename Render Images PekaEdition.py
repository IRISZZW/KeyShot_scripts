# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.3.0
# Renders all models with a chosen extension to images.
import os

def cleanExt(ext):
    while ext.startswith("."):
        ext = ext[1:]
    return ext

def main():
    values = [("folder", lux.DIALOG_FOLDER, "Folder to import from:", None),
              ("expfolder", lux.DIALOG_FOLDER, "Folder to export to:", None),
              ("iext", lux.DIALOG_TEXT, "Input file format to read:", "bip"),
              ("oext", lux.DIALOG_TEXT, "Output image format:", "png"),
              ("width", lux.DIALOG_INTEGER, "Output width:", 800),
              ("height", lux.DIALOG_INTEGER, "Output height:", 800)]
    opts = lux.getInputDialog(title = "Render Images",
                              desc = "Rendes all models with a chosen input extension to images of chosen output extension.",
                              values = values,
                              id = "renderimagespekaedition.py.luxion")
    if not opts: return

    if len(opts["folder"]) == 0:
        raise Exception("Folder cannot be empty!")
    fld = opts["folder"]
    expfld = opts["expfolder"]

    if len(opts["iext"]) == 0:
        raise Exception("Input extension cannot be empty!")
    iext = cleanExt(opts["iext"])

    if len(opts["oext"]) == 0:
        raise Exception("Output extension cannot be empty!")
    oext = cleanExt(opts["oext"])

    width = opts["width"]
    height = opts["height"]

    for f in [f for f in os.listdir(fld) if f.endswith(iext)]:
        path = fld + os.path.sep + f
        expPath = expfld + os.path.sep + f
        lux.newScene()
        
        opts = lux.getImportOptions()
        opts["snap_to_ground"] = False
        opts["adjust_environment"] = False
        
        print("Importing {}".format(path))
        lux.importFile(path, opts = opts)
        path = path + "." + oext

        print("Rendering {}".format(expPath))
        path = expPath + "." + oext
        lux.renderImage(path = path, width = width, height = height)

main()
