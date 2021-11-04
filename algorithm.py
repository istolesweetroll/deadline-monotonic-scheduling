import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

    @staticmethod
    def validate_task(task: Task):
        if task.period >= task.deadline > task.execution_time:
            return True
        else:
            return False

    def run(self):
        # def run(self, tasks):
        tasks = self.read_data("data.txt")

        lowest_common_multiple = np.lcm.reduce([x.period for x in tasks])
        result = []
        itr = 0
        completed_tasks = []
        tasks.sort(key=lambda x: x.deadline, reverse=False)

        for task in tasks:
            if not self.validate_task(task):
                return result

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
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()
        # Setting Y-axis limits


        # Setting X-axis limits

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('seconds since start')
        gnt.set_ylabel('Processor')
        # Setting ticks on y-axis
        # Labelling tickes of y-axis
        gnt.set_yticks([1, 2, 3])
        gnt.set_yticklabels(['1', '2', '3'])
        # Setting graph attribute
        gnt.grid(True)
        # Declaring a bar in schedule

        for x in args[1]:

            gnt.broken_barh([(x[0], x[1]-x[0])], (x[2], 1),
                            facecolors='tab:purple')



        plt.savefig("gantt1.png");


if __name__ == "__main__":
    # list = [Task(1, 40, 10, 30), Task(2, 50, 10, 50), Task(3, 60, 20, 40), Task(4, 110, 10, 100)]
    # list.append(Task(1, 20, 3, 7))
    # list.append(Task(3, 10, 2, 9))
    # list.append(Task(2, 5, 2, 4))

    dms = Dms()
    results = dms.run()
    dms.save(results)