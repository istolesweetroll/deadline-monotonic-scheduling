import matplotlib.pyplot as plt
import numpy as np
from PyQt6 import uic
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
import time

class UI(QWidget):
    def __init__(self):
        super().__init__()
        # this is used for loading ui file
        uic.loadUi("untitled.ui", self)
        f = open('data.txt', 'r')

        with f:
            data = f.read()
            self.textEdit.setText(data)

        self.welcomeBackground.setStyleSheet("background-image:url(./background.png) ")
        self.resultsBackground.setStyleSheet("background-image:url(./background.png)")
        self.reset.setVisible(False)
        self.error.setVisible(False)
        self.setFixedSize(644, 450)
        self.start_2.clicked.connect(self.switch_to_results)
        self.reset.clicked.connect(self.switch_to_welcome)

    def switch_to_welcome(self):
        self.welcome.setVisible(True)

    def switch_to_results(self):
        self.error.setVisible(False)
        with open('data.txt', 'w') as file:
            file.write(self.textEdit.toPlainText())
        if self.isInputGood():
            self.welcome.setVisible(False)
            dms = Dms()
            results = dms.run()
            dms.save(results)
            imageLabel = QLabel()
            image = QImage("./gantt1.png")
            self.reset.setVisible(True)
            imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scrollArea.setWidget(imageLabel)

        if not self.isInputGood():
            self.error.setVisible(True)

    def isInputGood(self):
        f = open("./data.txt",
                 "r")
        text = f.read()
        lines = text.split('\n')
        if len(lines) > 9:
            return False
        for line in lines:
            words = line.split(' ')
            length = len(line.split())
            if not all(c.isdecimal() for c in words[1:]) or line[0] != "t":
                f.close()
                return False
            if length != 4:
                f.close()
                return False
            if not words[1] >= words[3] > words[2]:
                f.close()
                return False
        f.close()
        return True

class Task:
    def __init__(self, task_name, period, execution_time, deadline):
        self.task_name = task_name
        self.period = period
        self.execution_time = execution_time
        self.deadline = deadline


class Dms:
    def read_data(self, filename: str):
        tasks = []
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
            for x in lines:
                tmp = x.split()
                tmp[0] = tmp[0][1:2]
                print(tmp[0])
                tasks.append(Task(int(tmp[0]), int(tmp[1]), int(tmp[2]), int(tmp[3])))

        return tasks

    def run(self):
        tasks = self.read_data("data.txt")

        lowest_common_multiple = np.lcm.reduce([x.period for x in tasks])
        result = []
        itr = 0
        completed_tasks = []
        tasks.sort(key=lambda x: x.deadline, reverse=False)

        for x in range(0, lowest_common_multiple):
            for task in tasks:
                if x % task.period == 0 and completed_tasks.__contains__(task) and not (x == 0):
                    completed_tasks.remove(task)

            if itr == 0:
                for task in tasks:
                    if not completed_tasks.__contains__(task):
                        completed_tasks.append(task)
                        result.append((x, x + task.execution_time, task.task_name))
                        itr = task.execution_time
                        break

            if itr != 0:
                itr -= 1

        return result

    def save(*args):
        xmax = 0;
        for x in args[1]:
            if x[1] > xmax:
                xmax = x[1]

        if(xmax > 150):
            fig, gnt = plt.subplots(figsize=(xmax/20, 4))
        else:
            fig, gnt = plt.subplots(figsize=(7.6, 4))


        gnt.set_xlabel('czas')
        gnt.set_ylabel('zadania')

        yticklabels = []
        facecolors = ['purple', 'red', 'blue', 'green', 'orange', 'yellow', 'pink', 'gray', 'black']
        for x in args[1]:
            if x[2] not in yticklabels:
                yticklabels.append(x[2])
        gnt.set_yticks(yticklabels)

        print(xmax)
        if (xmax > 150):
            plt.xticks(np.arange(0, xmax, 10))
        else:
            plt.xticks(np.arange(0, xmax, 1))

        gnt.grid(True)

        for x in args[1]:
                gnt.broken_barh([(x[0], x[1] - x[0])], (x[2], 1),
                                facecolors=facecolors[x[2] - 1])

        plt.xlim([0, xmax])
        plt.ylim([1, len(yticklabels)+1])
        plt.savefig("gantt1.png", bbox_inches='tight');


app = QApplication([])
window = UI()
window.show()
app.exec()
