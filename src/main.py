from PIL import Image
import glob, os

def cropImage(path, input, height, width):
    k = 1
    im = Image.open(input)
    imgwidth, imgheight = im.size
    print("Width: %s, Height: %s" % (imgwidth, imgheight))

    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            a = im.crop(box)
            #try:
            writePath = os.path.join(path, "img-%s.png" % k)
            print("Writing to %s" % writePath)
            a.save(writePath, compress_level=0)
            #except:
            #    print("Exception!!!")
            #    pass
            k +=1

if __name__=='__main__':
    print("Running...")
    cropImage("./samples", "./samples/test.jpg", 600, 800)