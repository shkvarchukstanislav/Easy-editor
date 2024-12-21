from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog
)
import os
from imageProcessor import ImageProcessor



class EasyEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(700, 500)
        self.setWindowTitle('Easy Editor')

        self.lb_image = QLabel(" ")
        self.btn_dir = QPushButton("Dateien")
        self.lw_files = QListWidget()

        self.btn_left = QPushButton("Links.")
        self.btn_right = QPushButton("Rechts")
        self.btn_flip = QPushButton("Spiegel")
        self.btn_sharp = QPushButton("Schärfe")
        self.btn_bw = QPushButton("S/W")
        self.btn_save = QPushButton("speichern")

        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        col1.addWidget(self.btn_dir)
        col1.addWidget(self.lw_files)
        col2.addWidget(self.btn_save)
        col2.addWidget(self.lb_image)
        row_tools = QHBoxLayout()
        row_tools.addWidget(self.btn_left)
        row_tools.addWidget(self.btn_right)
        row_tools.addWidget(self.btn_flip)
        row_tools.addWidget(self.btn_sharp)
        row_tools.addWidget(self.btn_bw)
        col2.addLayout(row_tools)
        row.addLayout(col1, 20)
        row.addLayout(col2, 80)
        self.setLayout(row)





        self.workdir = ''
        self.processor = ImageProcessor(self.lb_image)

        self.btn_bw.clicked.connect(self.processor.do_bw)
        self.btn_right.clicked.connect(self.processor.do_right)
        self.btn_left.clicked.connect(self.processor.do_left)
        self.btn_flip.clicked.connect(self.processor.do_flip)
        self.btn_sharp.clicked.connect(self.processor.do_sharpen)
        self.btn_save.clicked.connect(self.processor.saveImage)

        self.btn_dir.clicked.connect(self.showFilenamesList)
        self.lw_files.currentRowChanged.connect(self.showChosenImage)


    def filter(self, files, extensions):
        result = []
        for file in files:
            for ext in extensions:
                if file.endswith(ext):  # -> image|.png|
                    result.append(file)
        return result

    def showFilenamesList(self):
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        self.workdir = QFileDialog.getExistingDirectory()
        self.processor.workdir = self.workdir
        files = os.listdir(self.workdir)
        filenames = self.filter(files, extensions)
        self.lw_files.clear()
        self.lw_files.addItems(filenames)

    def showChosenImage(self):
        if self.lw_files.currentRow() >= 0:
            filename = self.lw_files.currentItem().text()
            self.processor.loadImage(filename)
            self.processor.showImage(os.path.join(self.workdir, filename))

    def saveImage(self):
        if self.processor.image:
            save_dir = QFileDialog.getExistingDirectory()
            if save_dir:
                fullname = os.path.join(save_dir, self.processor.filename)
                self.processor.image.save(fullname)


app = QApplication([])

win = EasyEditor()
win.show()
app.exec()
