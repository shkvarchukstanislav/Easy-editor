from PIL import Image, ImageFilter, ImageEnhance

import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageProcessor:
    def __init__(self, label):
        self.image = None
        self.workdir = ''
        self.filename = None
        self.save_dir = 'Modified/'
        self.label = label

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(self.workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self):
        path = os.path.join(self.workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, "temp." + self.filename.split(".")[-1])
        self.image.save(fullname)

    def do_bw(self):
        if self.image:
            self.image = self.image.convert("L")
            self.saveImage()
            image_path = os.path.join(self.workdir, self.save_dir, "temp." + self.filename.split(".")[-1])
            self.showImage(image_path)

    def do_left(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.saveImage()
            image_path = os.path.join(self.workdir, self.save_dir, "temp." + self.filename.split(".")[-1])
            self.showImage(image_path)

    def do_right(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.saveImage()
            image_path = os.path.join(self.workdir, self.save_dir, "temp." + self.filename.split(".")[-1])
            self.showImage(image_path)

    def do_flip(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.saveImage()
            image_path = os.path.join(self.workdir, self.save_dir, "temp." + self.filename.split(".")[-1])
            self.showImage(image_path)

    def do_sharpen(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.saveImage()
            image_path = os.path.join(self.workdir, self.save_dir, "temp." + self.filename.split(".")[-1])
            self.showImage(image_path)


    def showImage(self, path):
        self.label.hide()
        pixmapimage = QPixmap(path)
        w, h = self.label.width(), self.label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmapimage)
        self.label.show()
