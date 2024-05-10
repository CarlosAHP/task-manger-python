import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget

class TaskManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['PID', 'Nombre', 'Memoria'])
        self.tree_widget.setColumnWidth(0, 50)
        self.tree_widget.setColumnWidth(1, 300)
        self.tree_widget.setColumnWidth(2, 100)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.filtrar_procesos)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)
        layout.addWidget(self.search_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def filtrar_procesos(self):
        # Aquí implementarías la lógica para filtrar los procesos
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskManagerGUI()
    window.show()
    sys.exit(app.exec_())
