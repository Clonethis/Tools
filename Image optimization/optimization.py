from distutils.command.build import build
from pathlib import Path
from PIL import Image
import os
import shutil

import glob


# usage: in images put jpg images -> results in webp

# time for create this in cpp -> in python it is painfully slow like 10' for 20 pics https://developers.google.com/speed/webp/docs/api
def createImage(image, base, percentage=0.98, quality=40):
    print("Create image Run")
    name = base.split(".")[0]+'.jpg'
    width, height = image.size
    resized_dimensions = (int(width * percentage),
                          int(height * percentage))
    print("newDimensions:", resized_dimensions)

    resizedImage = image.resize(resized_dimensions, resample=1)
    print(resizedImage.size)
    resizedImage.save(name, format="jpeg", optimize=True,
                      quality=quality, method=6)  # Convert image to webp
    print("Resize end")

# Converts to webp -> unless it is acceptably small


def convert_to_webp(source, destination):
    # image resizing
    percentage = 0.9

    percentageOffset = 0.07

    # quality on which parsing should begin
    quality = 90

    # iterative step
    qualityOffset = 3

# parsed image size will be below this value ( in bytes )
    maximalImageSize = 100000

    print("Running convert fc")
    dest = Path(destination)
    print(dest)
    print("source", source)

    image = Image.open(source)  # Open image
    base = os.path.split(source)[1]
    imageName = base.split(".")[0]
    createImage(image, base)

    # unless is image below particular image size, process will still run.
    while os.path.getsize(imageName+'.jpg') >= maximalImageSize:
        # print("while running")
        print("size: ", os.path.getsize(imageName+'.jpg'))
        # print('percentage', percentage, "nice: ", quality)
        createImage(image, base, percentage, quality)

        if((percentage - percentageOffset) <= 0):
            percentageOffset = 0.005

            percentage -= percentageOffset
        if((quality-qualityOffset) <= 0):
            qualityOffset = 1

            quality -= qualityOffset
        else:
            print("Else po", percentageOffset, " qo: ", qualityOffset)
            percentage -= percentageOffset
            quality -= qualityOffset

        print("percentage:", percentage, "quality", quality)
    return destination


# puts images to build folder
def move(imageList):
    for fileName in imageList:
        new_path = os.path.join('./build', fileName)
        shutil.move(fileName, new_path)


def main():

    # all paths to images
    paths = Path("images").glob("**/*.jpg")

    # path for output images
    buildPath = Path("./build")

    # Solves if there was solution created before
    if(buildPath.exists()):
        print("build allready exists,removing build")
        # remove old account directory
        shutil.rmtree(buildPath)
        print("buildPath exists: ", buildPath.exists())
        os.mkdir(buildPath)
        print("buildPath exists: ", buildPath.exists())

    else:
        os.mkdir(buildPath)

# Iterates over all images in "./images"
    for path in paths:

        webp_path = convert_to_webp(path, buildPath)
        print("Image tell,: ", webp_path)
        print(webp_path)

    imageArray = glob.glob('./*.jpg')
    move(imageArray)
    print("done")


main()
