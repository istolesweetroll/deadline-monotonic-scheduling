from PyQt6.QtWidgets import QApplication, QWidget,  QMessageBox
from PyQt6 import uic, QtTest
from PyQt6.QtCore import pyqtSlot, QProcess
import sys


class UI(QWidget):
    def __init__(self):
        super().__init__()
        # this is used for loading ui file
        uic.loadUi("untitled.ui", self)
        self.read_data();
        self.welcomeBackground.setStyleSheet("background-image:url(./—Pngtree—liquid marble texture  fluid_988813)");
        self.resultsBackground.setStyleSheet("background-image:url(./—Pngtree—liquid marble texture  fluid_988813)");
        self.error.setVisible(False);
        self.setFixedSize(644, 450)
        self.start_2.clicked.connect(self.switch_to_results);
        self.reset.clicked.connect(self.switch_to_welcome);

    def switch_to_results(self):

        self.welcome.setVisible(False);
        with open('data.txt', 'w') as file:
            file.write(self.textEdit.toPlainText());
        self.progressBar.setValue(0);
        i = 0;
        while i < 10:
            self.progressBar.setValue(self.progressBar.value() + 10);
            QtTest.QTest.qWait(100);
            i = i + 1;

        self.displayResults.setStyleSheet("background-image:url(./gfg_earliest_deadline_first.png)");


    def switch_to_welcome(self):
        self.welcome.setVisible(True);


    def read_data(self):
        f = open('data.txt', 'r')
        with f:
            data = f.read()
            self.textEdit.setText(data)


app = QApplication([])
window = UI()
window.show()
app.exec()
