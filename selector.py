from flask import Flask, render_template, request, redirect, url_for
from os import listdir, path
from shutil import copy2
import json

app = Flask(__name__, static_folder="/")

inputImages = []
inputDir = f"{path.dirname(__file__)}/input/"
outputDir = f"{path.dirname(__file__)}/output/"
viewType = ""
rawType = ""

def createDictList(inputImages, viewType, rawType):
    imageList = []
    for image in inputImages:
        img = None
        raw = None
        if image[-len(viewType):].upper() == viewType.upper():
            img = f"{image[0:-len(viewType)]}{viewType}"
            if f"{image[0:-len(viewType)]}{rawType}" in inputImages:
                raw = f"{image[0:-len(rawType)]}{rawType}"
            else:
                raw = None
            currentImage = {}
            currentImage["view"] = img
            currentImage["raw"] = raw
            imageList.append(currentImage)
    return imageList

def copy(imagesToCopy):
    for i in range(len(imagesToCopy)):
        v = imagesToCopy[str(i)]["img"]
        r = imagesToCopy[str(i)]["raw"]
        global inputDir
        global outputDir
        copy2(f"{inputDir}{v}", f"{outputDir}{v}")
        if v != None:
            copy2(f"{inputDir}{r}", f"{outputDir}{r}")
    pass


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        global viewType
        viewType = request.form.get("viewtype")
        global rawType
        rawType = request.form.get("rawtype")
        global inputImages
        inputImages = listdir(inputDir)
        inputImages.sort()
        return redirect(url_for("selector"))
    return render_template("upload.html")


@app.route("/selector", methods=["GET", "POST"])
def selector():
    try:
        imageList = createDictList(inputImages, viewType, rawType)
    except:
        return "error"
    return render_template("selector.html", imageList=imageList)


@app.route("/send", methods=["GET"])
def send():
    imagesToCopy = request.args.get("obj")
    imagesToCopy = json.loads(imagesToCopy)
    copy(imagesToCopy)
    return "irrelevant"
    

if __name__ == "__main__":
    app.run(debug=True)
