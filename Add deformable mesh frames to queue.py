# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.1.4
# Add frames of a alembic/maya file to render queue.

import os

def cleanExt(ext):
  while ext.startswith("."):
    ext = ext[1:]
  return ext
    
def checkDialogOptions(opts):
  if len(opts["file"]) == 0:
    raise Exception("File cannot be empty!")
  if len(opts["oext"]) == 0:
    raise Exception("Output extension cannot be empty!")
  if opts["start"] > opts["end"]:
    raise Exception("Start frame cannot be larger than end frame!") 
  if opts["samples"] == 0:
    raise Exception("Invalid render option!")    
    
def getUpdateGeometryImportOptions():
  io = lux.getImportOptions()
  io['adjust_camera_look_at'] = False
  io['adjust_environment'] = False
  io['update_mode'] = True
  io['merge'] = True
  io['new_import'] = False
  io['camera_import'] = True
  return io

def main():
  renderCombo = ["Max Time", "Max Samples"]
  values = [("file", lux.DIALOG_FILE, "Input Alembic/maya file:", None),
            ("oext", lux.DIALOG_TEXT, "Output image format:", "png"),
            ("start", lux.DIALOG_INTEGER, "Start frame:", 0, (0, 10000)),
            ("end", lux.DIALOG_INTEGER, "End frame:", 10, (0, 10000)),
            ("width", lux.DIALOG_INTEGER, "Render width:", 500, (1, 10000)),
            ("height", lux.DIALOG_INTEGER, "Render height:", 500, (1, 10000)),
            ("cam", lux.DIALOG_TEXT, "Use camera. Leave blank for current:", lux.getCamera()),
            ("kframes", lux.DIALOG_CHECK, "Increase Keyshot frames", False),
            ("process", lux.DIALOG_CHECK, "Process queue after running script", False),
            (lux.DIALOG_LABEL, "--"),
            ("render_type", lux.DIALOG_ITEM, "Render Type:", renderCombo[0], renderCombo),
            ("samples", lux.DIALOG_INTEGER, "Samples / Seconds", 32, (0, 10000))]

  opts = lux.getInputDialog(title = "Add deformable mesh frames to queue",
                            desc = "",
                            values = values,
                            id = "add_deform_mesh_frames.py.luxion")
  if not opts: return
    
  checkDialogOptions(opts)
    
  file = opts["file"]
    
  oext = cleanExt(opts["oext"])  
  start = opts["start"]
  end = opts["end"]
  width = opts["width"]
  height = opts["height"]
  cam = opts["cam"]
  increaseFrames = opts["kframes"]    
  process = opts["process"]
  renderType = opts["render_type"]
  samples = opts["samples"]
        
  io = getUpdateGeometryImportOptions()
    
  ro = lux.getRenderOptions()
  ro.setAddToQueue(True)
  if renderType[1] == "Max Samples":
    ro.setMaxSamplesRendering(samples)
  if renderType[1] == "Max Time":
    ro.setMaxTimeRendering(samples)

  for i in range (start, end+1):
    io['frame'] = i
    path = file
    print("Importing {}".format(path))
    if not lux.importFile(path, False, True, io):
      raise Exception("Error in import! User cancelled?")
    if len(cam) != 0:
      lux.setCamera(cam)
    if increaseFrames:
      lux.setAnimationFrame(i)
    path = path + "." + str(i).zfill(5) + "." + oext
    print("Rendering {}".format(path))
    if not lux.renderImage(path, width, height, ro):
      raise Exception("Error in render! User cancelled?")
         
  if process:
    print("Processing queue")
    lux.processQueue()           

main()