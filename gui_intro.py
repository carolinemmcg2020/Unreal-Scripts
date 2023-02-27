import unreal
import sys
sys.path.append("C:\Program Files\Python39\Lib\site-packages")

from PySide2 import QtCore, QtGui, QtUiTools, QtWidgets
from PySide2.QtCore import Qt

#instances of unreal classes
editor_level_lib = unreal.EditorLevelLibrary()

class SimpleGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SimpleGUI, self).__init__(parent)

        # load the created ui widget
        self.widget = QtUiTools.QUiLoader().load("C:\Qt Projects\Basic_ui\\form.ui")

        # attach the widget to the "self GUI"
        self.widget.setParent(self)

        # set the UI geometry (if UI is not centered/visible)
        self.widget.setGeometry(0,0, self.widget.width(), self.widget.height())

        # find the interaction elements (XML Structure)
        self.text_l = self.widget.findChild(QtWidgets.QTextEdit, "textBox_L")
        self.text_r = self.widget.findChild(QtWidgets.QTextEdit, "textBox_R")
        self.checkbox = self.widget.findChild(QtWidgets.QCheckBox, "checkBox")

        # find and assign sliders
        self.slider = self.widget.findChild(QtWidgets.QSlider, "horizontalSlider")
        self.slider.sliderMoved.connect(self.on_slide)

        # find buttons and set up handlers
        self.btn_ok = self.widget.findChild(QtWidgets.QPushButton, "btn_ok")
        self.btn_ok.clicked.connect(self.ok_clicked)

        self.btn_cancel = self.widget.findChild(QtWidgets.QPushButton, "btn_cancel")
        self.btn_cancel.clicked.connect(self.cancel_clicked)

    # triggered on slide of the slider
    def on_slide(self):
        slider_value = self.slider.value()

        # move the selected actor according to the slider value
        selected_actors = editor_level_lib.get_selected_level_actors()

        if len(selected_actors) > 0:
            actor = selected_actors[0]

            # get old transform, change y axis value and write back
            new_transform = actor.get_actor_transform()
            new_transform.translation.y = slider_value

            actor.set_actor_transform(new_transform, True, True)


    # triggered on click of btn_ok
    def ok_clicked(self):
        text_l = self.text_l.toPlainText()
        text_r = self.text_r.toPlainText()
        is_checked = self.checkbox.isChecked()

        unreal.log("Text Left Value: {}". format(text_l))
        unreal.log("Text Right Value: {}". format(text_r))
        unreal.log("Checkbox Value: {}". format(is_checked))


    # cancel function
    def cancel_clicked(self):
        unreal.log("Canceled")
        self.close()        

        

# only create an instance of the GUI when it's not alerady running
app = None
if not QtWidgets.QApplication.instance():
    app =QtWidgets.QApplication(sys.argv)

# start the GUI
main_window = SimpleGUI()
main_window.show()