import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Minkoww_Window(QWidget):
    def __init__(self):
        super(Minkoww_Window, self).__init__()

        self.setWindowTitle("Minkoww")
        self.setMinimumSize(1280, 720)

        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # 왼쪽에 시간선 그래프 영역
        self.graph_frame = QFrame(self)
        self.graph_layout = QVBoxLayout(self.graph_frame)
        self.canvas = FigureCanvas(Figure(figsize=(10, 8)))  # 그래프 크기 조정

        self.ax = self.canvas.figure.subplots()
        self.graph_layout.addWidget(self.canvas)
        self.layout.addWidget(self.graph_frame)
        self.draw_graph()

        # 오른쪽에 객체 속성 정의 영역
        self.control_frame = QFrame(self)
        self.control_layout = QVBoxLayout(self.control_frame)

        self.obj_label = QLabel("Object Properties", self)
        self.obj_speed_label = QLabel("Speed:", self)
        self.obj_speed_input = QLineEdit(self)
        self.add_obj_button = QPushButton("Add Object", self)
        self.add_obj_button.clicked.connect(self.add_object)

        self.object_list = QListWidget(self)

        self.control_layout.addWidget(self.obj_label)
        self.control_layout.addWidget(self.obj_speed_label)
        self.control_layout.addWidget(self.obj_speed_input)
        self.control_layout.addWidget(self.add_obj_button)
        self.control_layout.addWidget(self.object_list)

        self.layout.addWidget(self.control_frame)

        self.obj_speed_input.returnPressed.connect(self.add_object)

    def draw_graph(self):
        self.ax.clear()
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.set_xlabel('Space (x)')
        self.ax.set_ylabel('Time (ct)')
        self.ax.set_title('Minkowski Spacetime Diagram')

        # 1사분면 범위로 설정
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

        # 빛의 경로 그리기 (기울기 1)
        self.ax.plot([0, 10], [0, 10], color='red', linestyle='--', linewidth=1)

    def add_object(self):
        try:
            speed = float(self.obj_speed_input.text())
            t = np.linspace(0, 10, 100)
            x = speed * t

            self.ax.plot(x, t, label=f'Speed: {speed}')
            self.ax.legend()
            self.canvas.draw()

            # 객체 속성을 리스트에 추가
            item = QListWidgetItem(f"Speed: {speed}")
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda: self.remove_object(item, speed))
            select_button = QPushButton("Select")
            select_button.clicked.connect(lambda: self.select_object(item, speed))
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_layout.addWidget(QLabel(f"Speed: {speed}"))
            item_layout.addWidget(remove_button)
            item_layout.addWidget(select_button)
            item_layout.addStretch()
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.object_list.addItem(item)
            self.object_list.setItemWidget(item, item_widget)

        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Please enter a numeric value for speed.")

    def select_object(self, item, speed):
        row = self.object_list.row(item)
        self.object_list.takeItem(row)

        line_color = None
        for line in self.ax.get_lines():
            label = line.get_label()
            if label == f"Speed: {speed}":
                line_color = line.get_color()
                break

        # 못 찾은 경우
        if line_color is None:
            line_color = 'black'

        t = np.linspace(0, 10, 100)
        inverse_speed = 1 / speed
        # 일정 간격으로 y축을 올려가며 시간선 그리기
        for i in range(100):
            x_inverse = inverse_speed * t - i*0.5  # y축으로 0.5씩 올려가며 그립니다.
            label = f'Inverse Speed {i + 1}: {speed}'
            self.ax.plot(x_inverse, t, color=line_color, linestyle='--', label=label, linewidth=1,
                         alpha=0.5)

        self.ax.legend()
        self.canvas.draw()

    def remove_object(self, item, speed):
        row = self.object_list.row(item)
        self.object_list.takeItem(row)

        # 그래프에서 해당 객체의 경로를 제거
        for line in self.ax.get_lines():
            label = line.get_label()
            if label == f"Speed: {speed}":
                line.remove()

        # 축 범위 다시 설정
        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()

        # 그래프를 다시 그려서 격자를 포함한 모든 요소를 업데이트
        self.draw_graph()

        # 리스트의 다른 객체들에 대한 시간선 격자를 다시 그리기
        for i in range(self.object_list.count()):
            list_item = self.object_list.item(i)
            speed_str = list_item.text().split(": ")[1]
            speed = float(speed_str)

            t = np.linspace(0, 10, 100)
            x = speed * t

            self.ax.plot(x, t, label=f'Speed: {speed}')
            self.ax.legend()
            self.canvas.draw()

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Minkoww_Window()
    window.show()
    sys.exit(app.exec())
