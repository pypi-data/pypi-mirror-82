from pathlib import Path
from qtpy import QtCore
from qtpy import QtWidgets


class ConvertCOODialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(ConvertCOODialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Convert to COCO format datasets ")
        self.annotation_dir = None
        self.out_dir = None
        self.label_list_text = None

        qbtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonbox = QtWidgets.QDialogButtonBox(qbtn)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        hboxLayOut = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()

        
        self.groupBoxFiles = QtWidgets.QGroupBox(
            f"Please select annotaton directory")
        self.annoFileLineEdit = QtWidgets.QLineEdit(self)
        self.annoFileButton = QtWidgets.QPushButton(
            'Open Annotations Directory', self)
        self.annoFileButton.clicked.connect(
            self.onOutAnnoDirButtonClicked)
        hboxLayOut.addWidget(self.annoFileLineEdit)
        hboxLayOut.addWidget(self.annoFileButton)
        self.groupBoxFiles.setLayout(hboxLayOut)

        hboxLabelLayOut = QtWidgets.QVBoxLayout()

        self.groupBoxLabelFiles = QtWidgets.QGroupBox(
            "Please choose a label tet file")
        self.inputLabelFileLineEdit = QtWidgets.QLineEdit(self)
        self.inputLabelFileButton = QtWidgets.QPushButton(
            'Open Labels File', self)
        self.inputLabelFileButton.clicked.connect(
            self.onInputFileButtonClicked)
        hboxLabelLayOut.addWidget(self.inputLabelFileLineEdit)
        hboxLabelLayOut.addWidget(self.inputLabelFileButton)
        self.groupBoxLabelFiles.setLayout(hboxLabelLayOut)

        self.groupBoxOutDir = QtWidgets.QGroupBox(
            "Please choose output directory (Optional)")
        self.outFileDirEdit = QtWidgets.QLineEdit(self)
        self.outDirButton = QtWidgets.QPushButton(
            'Select Output Directory', self)
        self.outDirButton.clicked.connect(self.onOutDirButtonClicked)
        hboxLayOutDir = QtWidgets.QHBoxLayout()
        hboxLayOutDir.addWidget(self.outFileDirEdit)
        hboxLayOutDir.addWidget(self.outDirButton)
        self.groupBoxOutDir.setLayout(hboxLayOutDir)

        vbox.addWidget(self.groupBoxFiles)
        vbox.addWidget(self.groupBoxLabelFiles)
        vbox.addWidget(self.groupBoxOutDir)
        vbox.addWidget(self.buttonbox)

        self.setLayout(vbox)
        self.show()

    def onInputFileButtonClicked(self):
        self.label_list_text, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open labels txt file",
            directory=str(Path()),
            filter='*'

        )
        if self.label_list_text is not None:
            self.inputLabelFileLineEdit.setText(self.label_list_text)

    def onOutDirButtonClicked(self):
        self.out_dir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                  "Select Directory")
        if self.out_dir is not None:
            self.outFileDirEdit.setText(self.out_dir)

    def onOutAnnoDirButtonClicked(self):
        self.annotation_dir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                         "Select Directory")
        if self.annotation_dir is not None:
            self.annoFileLineEdit.setText(self.annotation_dir)
