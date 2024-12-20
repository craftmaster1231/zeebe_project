import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel,
    QDialog, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

# Функция для получения данных о бизнес-процессах через gRPC
def getAvailableBP():
    return {
        "available_id": [1, 2, 3],
        "bp_name": ["БП 1", "БП 2", "БП 3"],
        "tasks": {
            1: ["Заказ пиццы", "Заказ супа", "Заказ пюрешки"],
            2: ["Осмотр автомобиля", "Осмотр пациента", "Осмотр окрестностей"],
            3: ["Диалог с участковым", "Диалог с медбратом", "Диалог с бабушкой-соседкой"]
        }
    }

# Функция для получения данных о воркерах через gRPC
def getAllWorkers():
    return {
        "worker_id": [1, 2, 3],
        "worker_name": ["Worker 1", "Worker 2", "Worker 3"],
        "count_tasks": [0, 0, 0]
    }

# Диалог для отображения задач выбранного БП
class BPTasksDialog(QDialog):
    def __init__(self, bp_name, tasks, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Задачи для {bp_name}")
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout()

        label = QLabel(f"Задачи для {bp_name}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Таблица для отображения задач
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["№ задачи", "Название задачи"])
        self.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks, 1):
            self.table.setItem(row - 1, 0, QTableWidgetItem(str(row)))
            self.table.setItem(row - 1, 1, QTableWidgetItem(task))

        layout.addWidget(self.table)
        self.setLayout(layout)


# Окно для отображения списка БП
class BPListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список БП")
        self.setStyleSheet("background-color: #e8eaf6;")
        self.resize(600, 300)

        self.bp_data = getAvailableBP()
        self.selected_bp_id = None

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["№ БП", "Название БП"])
        self.table.setRowCount(len(self.bp_data["available_id"]))

        for row, (bp_id, bp_name) in enumerate(zip(self.bp_data["available_id"], self.bp_data["bp_name"])):
            self.table.setItem(row, 0, QTableWidgetItem(str(bp_id)))
            self.table.setItem(row, 1, QTableWidgetItem(bp_name))

        self.table.cellClicked.connect(self.select_bp)
        layout.addWidget(self.table)

        self.bp_tasks_button = QPushButton("Задачи БП")
        self.bp_tasks_button.setEnabled(False)
        self.bp_tasks_button.clicked.connect(self.show_bp_tasks)
        layout.addWidget(self.bp_tasks_button)

        self.start_bp_button = QPushButton("Запустить БП")
        self.start_bp_button.setEnabled(False)
        self.start_bp_button.clicked.connect(self.start_bp)
        layout.addWidget(self.start_bp_button)

        self.setLayout(layout)

    def select_bp(self, row, column):
        self.selected_bp_id = int(self.table.item(row, 0).text())
        self.bp_tasks_button.setEnabled(True)
        self.start_bp_button.setEnabled(True)

    def show_bp_tasks(self):
        if self.selected_bp_id is not None:
            bp_name = self.bp_data["bp_name"][self.selected_bp_id - 1]
            tasks = self.bp_data["tasks"].get(self.selected_bp_id, [])
            dialog = BPTasksDialog(bp_name, tasks, self)
            dialog.exec_()

    def start_bp(self):
        if self.selected_bp_id is not None:
            bp_name = self.bp_data["bp_name"][self.selected_bp_id - 1]
            tasks = self.bp_data["tasks"].get(self.selected_bp_id, [])
            self.parent().add_tasks_to_worker(bp_name, tasks)
            self.parent().add_running_bp(self.selected_bp_id, bp_name)

# Окно для отображения задач воркера
class WorkerTasksDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Задачи воркера")
        self.setStyleSheet("background-color: #f5f5f5;")
        self.resize(600, 300)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "№ задачи", "Название задачи", "Время запуска задачи", "Номер БП", "Название БП"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_tasks(self, tasks):
        self.table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            for col, value in enumerate(task):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

# Окно для отображения списка воркеров
class WorkerListDialog(QDialog):
    def __init__(self, worker_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список воркеров")
        self.setStyleSheet("background-color: #e8eaf6;")
        self.resize(600, 300)

        self.worker_data = worker_data

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["№ Воркера", "Название Воркера", "Кол-во задач"])
        self.table.setRowCount(len(self.worker_data["worker_id"]))

        self.refresh_table()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def refresh_table(self):
        for row, (worker_id, worker_name, count_tasks) in enumerate(zip(
            self.worker_data["worker_id"],
            self.worker_data["worker_name"],
            self.worker_data["count_tasks"]
        )):
            self.table.setItem(row, 0, QTableWidgetItem(str(worker_id)))
            self.table.setItem(row, 1, QTableWidgetItem(worker_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(count_tasks)))

# Окно для отображения списка запущенных БП
class RunningBPDialog(QDialog):
    def __init__(self, running_bps, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список запущенных БП")
        self.setStyleSheet("background-color: #e8eaf6;")
        self.resize(600, 300)

        self.running_bps = running_bps
        self.selected_bp_id = None

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "№ БП", "Название БП", "Номер экземпляра БП", "Время запуска"
        ])
        self.table.cellClicked.connect(self.select_bp)
        layout.addWidget(self.table)

        self.refresh_table()

        # Кнопка "Задачи БП"
        self.bp_tasks_button = QPushButton("Задачи БП")
        self.bp_tasks_button.setEnabled(False)
        self.bp_tasks_button.clicked.connect(self.show_bp_tasks)
        layout.addWidget(self.bp_tasks_button)

        self.setLayout(layout)

    def refresh_table(self):
        self.table.setRowCount(len(self.running_bps))
        for row, bp in enumerate(self.running_bps):
            for col, value in enumerate(bp):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def select_bp(self, row, column):
        self.selected_bp_id = int(self.table.item(row, 0).text())
        self.bp_tasks_button.setEnabled(True)

    def show_bp_tasks(self):
        if self.selected_bp_id is not None:
            bp_data = getAvailableBP()
            bp_name = bp_data["bp_name"][self.selected_bp_id - 1]
            tasks = bp_data["tasks"].get(self.selected_bp_id, [])
            dialog = BPTasksDialog(bp_name, tasks, self)
            dialog.exec_()


# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер бизнес-процессов")
        self.resize(600, 400)
        self.setStyleSheet("background-color: #e8eaf6;")

        self.worker_data = getAllWorkers()
        self.tasks = []
        self.running_bps = []
        self.bp_instance_counter = {}

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        buttons = [
            ("Список БП", self.open_bp_list),
            ("Список воркеров", self.open_worker_list),
            ("Задачи воркера", self.open_worker_tasks),
            ("Список запущенных БП", self.open_running_bps),
        ]

        for text, callback in buttons:
            button = QPushButton(text)
            button.setStyleSheet("background-color: #3949ab; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
            if callback:
                button.clicked.connect(callback)
            layout.addWidget(button)

        central_widget.setLayout(layout)

        self.worker_tasks_dialog = WorkerTasksDialog(self)

    def open_bp_list(self):
        dialog = BPListDialog(self)
        dialog.exec_()

    def open_worker_list(self):
        dialog = WorkerListDialog(self.worker_data, self)
        dialog.exec_()

    def open_worker_tasks(self):
        self.worker_tasks_dialog.update_tasks(self.tasks)
        self.worker_tasks_dialog.exec_()

    def open_running_bps(self):
        dialog = RunningBPDialog(self.running_bps, self)
        dialog.exec_()

    def add_tasks_to_worker(self, bp_name, tasks):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        for i, task in enumerate(tasks):
            worker_id = (i % len(self.worker_data["worker_id"])) + 1
            self.tasks.append((len(self.tasks) + 1, task, current_time, worker_id, bp_name))
            self.worker_data["count_tasks"][worker_id - 1] += 1

        self.worker_tasks_dialog.update_tasks(self.tasks)

    def add_running_bp(self, bp_id, bp_name):
        # Получить текущий номер экземпляра для данного БП
        if bp_id not in self.bp_instance_counter:
            self.bp_instance_counter[bp_id] = 0
        self.bp_instance_counter[bp_id] += 1
        instance_id = self.bp_instance_counter[bp_id]

        # Записать данные о новом запущенном БП
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.running_bps.append((bp_id, bp_name, instance_id, current_time))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

