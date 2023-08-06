import sys
import time
import torch
from pathlib import Path
import functools
from qtpy import QtCore
from qtpy import QtWidgets
from qtpy import QtGui
import requests
import subprocess
from labelme.app import MainWindow
from labelme.utils import newIcon
from labelme.utils import newAction
from labelme import utils
from labelme.config import get_config
from annolid.annotation import labelme2coco
from annolid.data import videos
from annolid.gui.widgets import ExtractFrameDialog
from annolid.gui.widgets import ConvertCOODialog
from annolid.gui.widgets import TrainModelDialog
from qtpy.QtWebEngineWidgets import QWebEngineView
import webbrowser
__appname__ = 'Annolid'
__version__ = "1.0.0"


def start_tensorboard(log_dir=None,
                      tensorboard_url='http://localhost:6006'):

    process = None
    if log_dir is None:
        here = Path(__file__).parent
        log_dir = here.parent.resolve() / "runs" / "logs"
    try:
        r = requests.get(tensorboard_url)
    except requests.exceptions.ConnectionError:
        process = subprocess.Popen(
            ['tensorboard', f'--logdir={str(log_dir)}'])
        time.sleep(8)
    return process


class VisualizationWindow(QtWidgets.QDialog):

    def __init__(self):
        super(VisualizationWindow, self).__init__()
        self.setWindowTitle("Visualization Tensorboard")
        self.process = start_tensorboard()
        self.browser = QWebEngineView()
        self.browser.setUrl(QtCore.QUrl(self.tensorboar_url))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.browser)
        self.setLayout(vbox)
        self.show()

    def closeEvent(self, event):
        if self.process is not None:
            time.sleep(3)
            self.process.kill()
        event.accept()


class AnnolidWindow(MainWindow):
    def __init__(self,
                 config=None
                 ):
        super(AnnolidWindow, self).__init__()

        self.flag_dock.setVisible(True)
        self.label_dock.setVisible(True)
        self.shape_dock.setVisible(True)
        self.file_dock.setVisible(True)
        self.here = Path(__file__).resolve().parent
        action = functools.partial(newAction, self)

        coco = action(
            self.tr("&COCO format"),
            self.coco,
            'Ctrl+C+O',
            "coco",
            self.tr("Convert to COCO format"),
        )

        coco.setIcon(QtGui.QIcon(str(
            self.here / "icons/coco.png")))

        frames = action(
            self.tr("&Extract frames"),
            self.frames,
            'Ctrl+Shift+E',
            "Extract frames",
            self.tr("Extract frames frome a video"),
        )

        models = action(
            self.tr("&Train models"),
            self.models,
            "Ctrl+Shift+T",
            "Train models",
            self.tr("Train neural networks")
        )
        models.setIcon(QtGui.QIcon(str(
            self.here / "icons/models.png")))

        frames.setIcon(QtGui.QIcon(str(
            self.here / "icons/extract_frames.png")))

        visualization = action(
            self.tr("&Visualization"),
            self.visualization,
            'Ctrl+Shift+V',
            "Visualization",
            self.tr("Visualization results"),
        )

        visualization.setIcon(QtGui.QIcon(str(
            self.here / "icons/visualization.png")))

        self.menus = utils.struct(
            recentFiles=QtWidgets.QMenu(self.tr("Open &Recent")),
            frames=self.menu(self.tr("&Extract Frames")),
            coco=self.menu(self.tr("&COCO")),
            models=self.menu(self.tr("&Train models")),
            visualization=self.menu(self.tr("&Visualization")),
        )

        _action_tools = list(self.actions.tool)
        _action_tools.insert(0,frames)
        _action_tools.append(coco)
        _action_tools.append(models)
        _action_tools.append(visualization)
        self.actions.tool = tuple(_action_tools)
        self.tools.clear()
        utils.addActions(self.tools, self.actions.tool)
        utils.addActions(self.menus.frames, (frames,))
        utils.addActions(self.menus.coco, (coco,))
        utils.addActions(self.menus.models, (models,))
        utils.addActions(self.menus.visualization, (visualization,))
        self.statusBar().showMessage(self.tr("%s started.") % __appname__)
        self.statusBar().show()
        self.setWindowTitle(__appname__)
        self.settings = QtCore.QSettings("Annolid", 'Annolid')

    def frames(self):
        dlg = ExtractFrameDialog()
        video_file = None
        out_dir = None

        if dlg.exec_():
            video_file = dlg.video_file
            num_frames = dlg.num_frames
            algo = dlg.algo
            out_dir = dlg.out_dir

        if video_file is None:
            return
        videos.extract_frames(
            video_file,
            num_frames=num_frames,
            algo=algo,
            out_dir=out_dir
        )
        if out_dir is None:
            out_frames_dir = str(Path(video_file).resolve().with_suffix(''))
        else:
            out_frames_dir = str(Path(out_dir) / Paht(video_file).name)

        QtWidgets.QMessageBox.about(self,
                                    "Finished",
                                    f"Done! Results are in folder: \
                                         {out_frames_dir}")
        self.statusBar().showMessage(
            self.tr(f"Finshed extracting frames."))
        self.importDirImages(out_frames_dir)

    def models(self):

        dlg = TrainModelDialog()
        config_file = None
        out_dir = None

        if dlg.exec_():
            config_file = dlg.config_file
            batch_size = dlg.batch_size
            algo = dlg.algo
            out_dir = dlg.out_dir

        if config_file is None:
            return

        # start training models
        if not torch.cuda.is_available():
            QtWidgets.QMessageBox.about(self,
                                        "Not GPU available",
                                        "At least one GPU  is required to train models.")
            return

        subprocess.Popen(['annolid-train',
                          f'--config={config_file}',
                          f'--batch_size={batch_size}'])

        process = start_tensorboard()

        if out_dir is None:
            out_runs_dir = Path(__file__).parent.parent / \
                'segmentation' / 'yolact' / 'runs'
        else:
            out_runs_dir = Path(out_dir) / Path(config_file).name / 'runs'

        out_runs_dir.mkdir(exist_ok=True, parents=True)

        QtWidgets.QMessageBox.about(self,
                                    "Started",
                                    f"Results are in folder: \
                                         {str(out_runs_dir)}")
        self.statusBar().showMessage(
            self.tr(f"Training..."))

    def coco(self):
        """
        Convert Labelme annotations to COCO format.
        """
        output_dir = None
        labels_file = None
        input_anno_dir = None
        coco_dlg = ConvertCOODialog()
        if coco_dlg.exec_():
            input_anno_dir = coco_dlg.annotation_dir
            labels_file = coco_dlg.label_list_text
            output_dir = coco_dlg.out_dir
        else:
            return

        if input_anno_dir is None:
            QtWidgets.QMessageBox.about(self,
                                        "No input file or directory",
                                        f"Please check and open the  \
                                        files or directories.")
            return

        if output_dir is None:
            self.output_dir = Path(input_anno_dir).parent / \
                (Path(input_anno_dir).name + '_coco_dataset')

        else:
            self.output_dir = output_dir

        if labels_file is None:
            labels_file = str(self.here.parent / 'annotation' /
                              'labels_custom.txt')

        labelme2coco.convert(
            str(input_anno_dir),
            output_annotated_dir=str(self.output_dir),
            labels_file=labels_file
        )
        self.statusBar().showMessage(self.tr("%s ...") % "converting")
        QtWidgets.QMessageBox.about(self,
                                    "Finished",
                                    f"Done! Results are in folder: \
                                         {str(self.output_dir)}")
        self.statusBar().showMessage(self.tr("%s Done.") % "converting")

    def visualization(self):
        try:
            url = 'http://localhost:6006/'
            process = start_tensorboard(tensorboard_url=url)
            webbrowser.open(url)
        except Exception:
            vdlg = VisualizationWindow()
            if vdlg.exec_():
                pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("icon"))
    win = AnnolidWindow()

    win.show()
    win.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
