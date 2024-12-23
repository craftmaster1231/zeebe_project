import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QLabel, QLineEdit, QScrollArea, QFrame
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class PostgresApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PostgreSQL Interface")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.operation_dropdown = QComboBox(self)
        self.operation_dropdown.addItems([
            "Показать Core",
            "Показать Placement",
            "Показать Device_Connections",
            "Добавить запись в Core",
            "Добавить запись в Placement",
            "Добавить запись в Device_Connections",
            "Изменить запись в Core",
            "Изменить запись в Placement",
            "Удалить запись в Core",
            "Удалить запись в Placement",
            "Удалить запись в Device_Connections"
        ])
        self.operation_dropdown.currentIndexChanged.connect(self.update_form)
        self.layout.addWidget(self.operation_dropdown)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scrollable_content = QFrame(self)
        self.form_layout = QVBoxLayout(self.scrollable_content)
        self.scrollable_content.setLayout(self.form_layout)
        self.scroll_area.setWidget(self.scrollable_content)
        self.layout.addWidget(self.scroll_area)

        self.form_fields = {}

        self.execute_button = QPushButton("Выполнить команду", self)
        self.execute_button.clicked.connect(self.execute_command)
        self.execute_button.setEnabled(False)
        self.layout.addWidget(self.execute_button)

        self.output_display = QTableWidget(self)
        self.layout.addWidget(self.output_display)

        self.init_db()

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("postgres")
        self.db.setUserName("postgres")
        self.db.setPassword("postgres")
        if not self.db.open():
            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem("Ошибка: Не удалось подключиться к базе данных."))

    def update_form(self):
        while self.form_layout.count():
            widget = self.form_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        self.form_fields.clear()
        self.execute_button.setEnabled(False)

        selected_operation = self.operation_dropdown.currentText()

        if "Показать" in selected_operation:
            self.execute_button.setEnabled(True)

        elif "Добавить запись в" in selected_operation:
            if "Core" in selected_operation:
                self.create_form_for_core()
            elif "Placement" in selected_operation:
                self.create_form_for_placement()
            elif "Device_Connections" in selected_operation:
                self.create_form_for_device_connections()
            self.execute_button.setEnabled(True)

        elif "Изменить запись в Core" == selected_operation:
            self.create_update_form_for_core()
            self.execute_button.setEnabled(True)
        elif "Изменить запись в Placement" == selected_operation:
            self.create_update_form_for_placement()
            self.execute_button.setEnabled(True)


        elif "Удалить запись в" in selected_operation:
            if "Core" in selected_operation:
                self.create_delete_form_for_core()
            elif "Placement" in selected_operation:
                self.create_delete_form_for_placement()
            elif "Device_Connections" in selected_operation:
                self.create_delete_form_for_device_connections()
            self.execute_button.setEnabled(True)

    def create_form_for_core(self):
        fields = [
            "BuildingName", "DesignPowerCapacity", "DeviceName", "DeviceType",
            "Manufacturer", "Model"
        ]

        for field in fields:
            label = QLabel(field, self)
            input_field = QLineEdit(self)
            if field == "DesignPowerCapacity":
                input_field.setPlaceholderText("Введите число (десятичное)")
            self.form_fields[field] = input_field
            self.form_layout.addWidget(label)
            self.form_layout.addWidget(input_field)

    def create_form_for_placement(self):
        fields = [
            "SpaceName", "ParentId", "Type", "XCoordinate", "YCoordinate", "ZCoordinate",
            "Rotation", "RackSide", "RU", "Location", "UHeight", "XOffset", "XPosition"
        ]

        for field in fields:
            label = QLabel(field, self)
            if field == "ParentId":
                input_field = QComboBox(self)
                self.populate_combobox_with_ids(input_field, "Core")
            elif field in ["XCoordinate", "YCoordinate", "ZCoordinate", "Rotation", "XOffset", "XPosition"]:
                input_field = QLineEdit(self)
                input_field.setPlaceholderText("Введите число (десятичное)")
            elif field in ["RU", "Location", "UHeight"]:
                input_field = QLineEdit(self)
                input_field.setPlaceholderText("Введите целое число")
            else:
                input_field = QLineEdit(self)

            self.form_fields[field] = input_field
            self.form_layout.addWidget(label)
            self.form_layout.addWidget(input_field)

    def populate_combobox_with_ids(self, combobox, table_name, id_field="Id"):
        combobox.clear()
        query = QSqlQuery(f"SELECT {id_field} FROM {table_name}", self.db)
        while query.next():
            combobox.addItem(str(query.value(0)))

    def create_form_for_device_connections(self):
        fields = ["ConnectionFromDevice", "ConnectedFromPort", "ConnectedToDevice", "ConnectedToPort", "ConnectionType"]

        for field in fields:
            label = QLabel(field, self)
            if field in ["ConnectionFromDevice", "ConnectedToDevice"]:
                input_field = QComboBox(self)
                self.populate_combobox_with_ids(input_field, "Core")
            elif field == "ConnectionType":
                input_field = QComboBox(self)
                input_field.addItems(["POWER_CONNECTION", "DATA_CONNECTION"])
            else:
                input_field = QLineEdit(self)

            self.form_fields[field] = input_field
            self.form_layout.addWidget(label)
            self.form_layout.addWidget(input_field)

    def execute_command(self):
        selected_operation = self.operation_dropdown.currentText()

        if "Показать" in selected_operation:
            table_name = selected_operation.split(" ")[1]
            self.show_table(table_name)
        elif "Добавить запись в" in selected_operation:
            table_name = selected_operation.split(" ")[3]
            self.add_record(table_name)
        elif "Изменить запись в Core" == selected_operation:
            self.update_core()
        elif "Изменить запись в Placement" == selected_operation:
            self.update_placement()
        elif "Удалить запись в Core" == selected_operation:
            self.delete_core()
        elif "Удалить запись в Placement" == selected_operation:
            self.delete_placement()
        elif "Удалить запись в Device_Connections" == selected_operation:
            self.delete_device_connections()

    def show_table(self, table_name):
        query = QSqlQuery(self.db)

        if not query.exec(f"SELECT * FROM {table_name}"):
            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem(f"Ошибка: {query.lastError().text()}"))
            return

        record = query.record()
        num_cols = record.count()

        self.output_display.setRowCount(0)
        self.output_display.setColumnCount(num_cols)
        self.output_display.setHorizontalHeaderLabels([record.fieldName(i) for i in range(num_cols)])

        row = 0
        while query.next():
            self.output_display.insertRow(row)
            for col in range(num_cols):
                self.output_display.setItem(row, col, QTableWidgetItem(str(query.value(col))))
            row += 1

    def add_record(self, table_name):
        try:
            data = {field: field_widget.currentText() if isinstance(field_widget, QComboBox)
                    else field_widget.text()
                    for field, field_widget in self.form_fields.items()}
            columns = ", ".join(data.keys())
            values = ", ".join([f"'{value}'" for value in data.values()])
            query_text = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

            query = QSqlQuery(self.db)
            if not query.exec(query_text):
                raise Exception(query.lastError().text())

            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem(f"Запись успешно добавлена в {table_name}."))

        except Exception as e:
            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem(f"Ошибка: {str(e)}"))

    def create_update_form_for_core(self):
        # Выпадающий список для выбора Id
        id_label = QLabel("Id", self)
        id_combobox = QComboBox(self)
        self.populate_combobox_with_ids(id_combobox, "Core")
        self.form_layout.addWidget(id_label)
        self.form_layout.addWidget(id_combobox)
        self.form_fields["Id"] = id_combobox

        # Поля для изменения остальных данных
        fields = [
            "BuildingName", "DesignPowerCapacity", "DeviceName", "DeviceType",
            "Manufacturer", "Model"
        ]

        for field in fields:
            label = QLabel(field, self)
            input_field = QLineEdit(self)
            if field == "DesignPowerCapacity":
                input_field.setPlaceholderText("Введите число (десятичное)")
            self.form_fields[field] = input_field
            self.form_layout.addWidget(label)
            self.form_layout.addWidget(input_field)

        # Обработчик изменения Id для автозаполнения полей
        id_combobox.currentIndexChanged.connect(lambda: self.populate_update_fields(id_combobox.currentText()))

    def create_update_form_for_placement(self):
        # Выпадающий список для выбора SpaceId
        space_id_label = QLabel("SpaceId", self)
        space_id_combobox = QComboBox(self)
        self.populate_combobox_with_ids(space_id_combobox, "Placement", id_field="SpaceId")
        self.form_layout.addWidget(space_id_label)
        self.form_layout.addWidget(space_id_combobox)
        self.form_fields["SpaceId"] = space_id_combobox

        # Поля для изменения остальных данных
        fields = [
            "SpaceName", "ParentId", "Type", "XCoordinate", "YCoordinate", "ZCoordinate",
            "Rotation", "RackSide", "RU", "Location", "UHeight", "XOffset", "XPosition"
        ]

        for field in fields:
            label = QLabel(field, self)
            if field in ["XCoordinate", "YCoordinate", "ZCoordinate", "Rotation", "XOffset", "XPosition"]:
                input_field = QLineEdit(self)
                input_field.setPlaceholderText("Введите число (десятичное)")
            elif field in ["RU", "Location", "UHeight"]:
                input_field = QLineEdit(self)
                input_field.setPlaceholderText("Введите целое число")
            elif field == "ParentId":
                input_field = QComboBox(self)
                self.populate_combobox_with_ids(input_field, "Core", id_field="Id")
            else:
                input_field = QLineEdit(self)

            self.form_fields[field] = input_field
            self.form_layout.addWidget(label)
            self.form_layout.addWidget(input_field)

        # Обработчик изменения SpaceId для автозаполнения полей
        space_id_combobox.currentIndexChanged.connect(
            lambda: self.populate_update_fields_for_placement(space_id_combobox.currentText()))

    def populate_update_fields(self, selected_id):
        if not selected_id:
            return

        query = QSqlQuery(self.db)
        if not query.exec(f"SELECT * FROM Core WHERE Id = '{selected_id}'"):
            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem(f"Ошибка: {query.lastError().text()}"))
            return

        if query.next():
            # Заполнение полей значениями из базы данных
            for field, input_field in self.form_fields.items():
                if field == "Id":
                    continue
                if isinstance(input_field, QLineEdit):
                    input_field.setText(str(query.value(field)))

    def populate_update_fields_for_placement(self, selected_space_id):
        if not selected_space_id:
            return

        query = QSqlQuery(self.db)
        if not query.exec(f"SELECT * FROM Placement WHERE SpaceId = '{selected_space_id}'"):
            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem(f"Ошибка: {query.lastError().text()}"))
            return

        if query.next():
            # Заполнение полей значениями из базы данных
            for field, input_field in self.form_fields.items():
                if field == "SpaceId":
                    continue
                if isinstance(input_field, QLineEdit):
                    input_field.setText(str(query.value(field)))
                elif isinstance(input_field, QComboBox):
                    index = input_field.findText(str(query.value(field)))
                    if index != -1:
                        input_field.setCurrentIndex(index)

    def update_core(self):
        try:
            data = {}
            # Собрать данные из полей
            for field, field_widget in self.form_fields.items():
                if isinstance(field_widget, QComboBox):
                    data[field] = field_widget.currentText()
                elif isinstance(field_widget, QLineEdit):
                    data[field] = field_widget.text()

            id_to_update = data.pop("Id", None)

            if not id_to_update:
                raise ValueError("Поле Id обязательно для обновления записи.")

            # Формировать SET-выражение для запроса
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items() if value])
            query_text = f"UPDATE Core SET {set_clause} WHERE Id = '{id_to_update}';"

            query = QSqlQuery(self.db)
            if not query.exec(query_text):
                raise Exception(query.lastError().text())

            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem("Запись успешно обновлена."))

        except Exception as e:
            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem(f"Ошибка: {str(e)}"))

    def update_placement(self):
        try:
            data = {}
            # Собрать данные из полей
            for field, field_widget in self.form_fields.items():
                if isinstance(field_widget, QComboBox):
                    data[field] = field_widget.currentText()
                elif isinstance(field_widget, QLineEdit):
                    data[field] = field_widget.text()

            space_id_to_update = data.pop("SpaceId", None)

            if not space_id_to_update:
                raise ValueError("Поле SpaceId обязательно для обновления записи.")

            # Формировать SET-выражение для запроса
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items() if value])
            query_text = f"UPDATE Placement SET {set_clause} WHERE SpaceId = '{space_id_to_update}';"

            query = QSqlQuery(self.db)
            if not query.exec(query_text):
                raise Exception(query.lastError().text())

            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem("Запись успешно обновлена."))

        except Exception as e:
            self.output_display.setRowCount(1)
            self.output_display.setColumnCount(1)
            self.output_display.setItem(0, 0, QTableWidgetItem(f"Ошибка: {str(e)}"))

    def create_delete_form_for_core(self):
        # Выпадающий список для выбора Id
        id_label = QLabel("Id", self)
        id_combobox = QComboBox(self)
        self.populate_combobox_with_ids(id_combobox, "Core")
        self.form_layout.addWidget(id_label)
        self.form_layout.addWidget(id_combobox)
        self.form_fields["Id"] = id_combobox

    def create_delete_form_for_placement(self):
        # Выпадающий список для выбора SpaceId
        space_id_label = QLabel("SpaceId", self)
        space_id_combobox = QComboBox(self)
        self.populate_combobox_with_ids(space_id_combobox, "Placement", id_field="SpaceId")
        self.form_layout.addWidget(space_id_label)
        self.form_layout.addWidget(space_id_combobox)
        self.form_fields["SpaceId"] = space_id_combobox

    def create_delete_form_for_device_connections(self):
        # Выпадающий список для выбора ConnectionFromDevice
        from_device_label = QLabel("ConnectionFromDevice", self)
        from_device_combobox = QComboBox(self)
        self.populate_combobox_with_ids(from_device_combobox, "Device_Connections", id_field="ConnectionFromDevice")
        self.form_layout.addWidget(from_device_label)
        self.form_layout.addWidget(from_device_combobox)
        self.form_fields["ConnectionFromDevice"] = from_device_combobox

        # Выпадающий список для выбора ConnectionToDevice
        to_device_label = QLabel("ConnectionToDevice", self)
        to_device_combobox = QComboBox(self)
        self.populate_combobox_with_ids(to_device_combobox, "Device_Connections", id_field="ConnectedToDevice")
        self.form_layout.addWidget(to_device_label)
        self.form_layout.addWidget(to_device_combobox)
        self.form_fields["ConnectionToDevice"] = to_device_combobox

    def delete_core(self):
        try:
            selected_id = self.form_fields["Id"].currentText()
            query = QSqlQuery(self.db)
            if not query.exec(f"DELETE FROM Core WHERE Id = '{selected_id}'"):
                raise Exception(query.lastError().text())
            self.show_message("Запись успешно удалена из Core.")
        except Exception as e:
            self.show_message(f"Ошибка: {str(e)}")

    def delete_placement(self):
        try:
            selected_space_id = self.form_fields["SpaceId"].currentText()
            # Проверка на существование потомков
            query = QSqlQuery(self.db)
            if query.exec(f"SELECT COUNT(*) FROM Placement WHERE ParentId = '{selected_space_id}'"):
                query.next()
                if query.value(0) > 0:
                    raise Exception("Невозможно удалить запись, так как у неё есть потомки.")
            if not query.exec(f"DELETE FROM Placement WHERE SpaceId = '{selected_space_id}'"):
                raise Exception(query.lastError().text())
            self.show_message("Запись успешно удалена из Placement.")
        except Exception as e:
            self.show_message(f"Ошибка: {str(e)}")

    def delete_device_connections(self):
        try:
            from_device = self.form_fields["ConnectionFromDevice"].currentText()
            to_device = self.form_fields["ConnectionToDevice"].currentText()
            query = QSqlQuery(self.db)
            if not query.exec(
                    f"DELETE FROM Device_Connections WHERE ConnectionFromDevice = '{from_device}' AND ConnectedToDevice = '{to_device}'"):
                raise Exception(query.lastError().text())
            self.show_message("Запись успешно удалена из Device_Connections.")
        except Exception as e:
            self.show_message(f"Ошибка: {str(e)}")

    def show_message(self, message):
        self.output_display.setRowCount(1)
        self.output_display.setColumnCount(1)
        self.output_display.setItem(0, 0, QTableWidgetItem(message))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PostgresApp()
    window.show()
    sys.exit(app.exec_())
