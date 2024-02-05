import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from datetime import timedelta

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.sezione_testo_1 = QLabel("Inserisci il numero di minuti da convertire in HH:MM", self)
        self.sezione_testo_1.setFont(QFont("Arial", 14, QFont.Bold))
        self.sezione_testo_1.setStyleSheet("text-transform: uppercase;")
        self.sezione_testo_1.setAlignment(Qt.AlignCenter)
        self.btn_minus_25 = QPushButton("-25", self)
        self.input_text_1 = QLineEdit("0", self)
        self.btn_plus_25 = QPushButton("+25", self)
        self.btn_converti = QPushButton("Converti", self)
        self.risultato_1 = QLabel("")

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.btn_minus_25)
        layout_1.addWidget(self.input_text_1)
        layout_1.addWidget(self.btn_plus_25)

        layout_2 = QVBoxLayout()
        layout_2.addWidget(self.sezione_testo_1)
        layout_2.addLayout(layout_1)
        layout_2.addWidget(self.btn_converti)
        layout_2.addWidget(self.risultato_1)

        self.sezione_testo_2 = QLabel("Inserisci il tempo nel formato HH:MM", self)
        self.sezione_testo_2.setFont(QFont("Arial", 14, QFont.Bold))
        self.sezione_testo_2.setStyleSheet("text-transform: uppercase;")
        self.sezione_testo_2.setAlignment(Qt.AlignCenter)

        self.input_text_2 = QLineEdit("0:00", self)
        self.btn_somma = QPushButton("Somma", self)
        self.risultato_2 = QLabel("")

        layout_3 = QVBoxLayout()
        layout_3.addWidget(self.sezione_testo_2)
        layout_3.addWidget(self.input_text_2)
        layout_3.addWidget(self.btn_somma)
        layout_3.addWidget(self.risultato_2)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(layout_2)
        main_layout.addLayout(layout_3)

        self.tempo_totale = timedelta()

        self.setMinimumSize(500, 400)

        self.first_show = True

        self.btn_minus_25.clicked.connect(self.sottrai_25_minuti)
        self.btn_plus_25.clicked.connect(self.aggiungi_25_minuti)
        self.btn_converti.clicked.connect(self.converti_minuti)
        self.btn_somma.clicked.connect(self.somma_tempo)

        self.input_text_1.installEventFilter(self)
        self.input_text_2.installEventFilter(self)

    def aggiungi_25_minuti(self):
        try:
            minuti = int(self.input_text_1.text())
            if minuti >= 0:
                minuti += 25
                self.input_text_1.setText(str(minuti))
        except ValueError:
            pass

    def sottrai_25_minuti(self):
        try:
            minuti = int(self.input_text_1.text())
            if minuti >= 25:
                minuti -= 25
                self.input_text_1.setText(str(minuti))
            else:
                minuti = 0
                self.input_text_1.setText(str(minuti))
        except ValueError:
            pass

    def converti_minuti(self):
        try:
            minuti = int(self.input_text_1.text())
            ore, minuti = divmod(minuti, 60)
            self.risultato_1.setText(f"Risultato: {ore:02d}:{minuti:02d}")
        except ValueError:
            pass

    def somma_tempo(self):
        try:
            tempo_input = self.input_text_2.text()
            ore, minuti = map(int, tempo_input.split(':'))
            tempo_da_aggiungere = timedelta(hours=ore, minutes=minuti)

            minuti_totali = int(self.tempo_totale.total_seconds() / 60)
            minuti_totali += int(tempo_da_aggiungere.total_seconds() / 60)

            self.tempo_totale = timedelta(minutes=minuti_totali)

            ore_totale, minuti_totale = divmod(minuti_totali, 60)

            self.risultato_2.setText(f"Risultato: {int(ore_totale):02d}:{int(minuti_totale):02d}")
        except ValueError:
            pass

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            obj.selectAll()
        return False
    
    def center_on_screen(self):
        window_geometry = self.geometry()
        primary_screen = QApplication.primaryScreen()
        screen_geometry = primary_screen.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def showEvent(self, event):
        super().showEvent(event)
        if self.first_show:
            self.center_on_screen()
            self.first_show = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.setWindowTitle("Tomato Calculator")
    ex.setGeometry(100, 100, 450, 400)
    ex.show()
    sys.exit(app.exec_())