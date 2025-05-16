from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt
import pandas as pd
import sys
import os
from PyQt5.QtMultimedia import QSound
import os


class QuizDialog(QDialog):
    def __init__(self, main_app, soru, cevap1, cevap2):
        super().__init__()

        self.main_app = main_app
        self.soru = soru
        self.cevap1 = cevap1
        self.cevap2 = cevap2

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label_soru = QLabel(self.soru)
        layout.addWidget(label_soru)

        label_cevap1 = QLabel(self.cevap1)
        layout.addWidget(label_cevap1)

        # label_cevap2 = QLabel(self.cevap2)
        #  layout.addWidget(label_cevap2)

        self.cevap_kutusu = QLineEdit(self)
        layout.addWidget(self.cevap_kutusu)

        button_gonder = QPushButton("Gönder", self)
        button_gonder.clicked.connect(self.gonder_clicked)
        layout.addWidget(button_gonder)

        self.setLayout(layout)
        self.setWindowTitle("Quiz Penceresi")

    def gonder_clicked(self):
        kullanici_cevap = self.cevap_kutusu.text().strip().lower()
        dogru_cevap = self.cevap2.strip().lower()

        if kullanici_cevap == dogru_cevap:
            # ✅ DOĞRU SESİ
            sound_path = os.path.join(os.getcwd(), "correct_sound")
            QSound.play(sound_path)

            QMessageBox.information(self, "Doğru", "Doğru cevap!", QMessageBox.Ok)
            self.main_app.dogrular.append(self.soru)
        else:
            # ❌ YANLIŞ SESİ
            sound_path = os.path.join(os.getcwd(), "incorrect_sound")
            QSound.play(sound_path)

            QMessageBox.warning(
                self, "Yanlış", f"Yanlış. Doğru cevap: {dogru_cevap}", QMessageBox.Ok
            )
            self.main_app.yanlislar.append(self.soru)

        self.accept()
        self.main_app.show()

        
    def closeEvent(self, event):
        cevap = QMessageBox.question(
            self,
            "Çıkmak istiyor musun?",
            "Quizden çıkmak istiyor musun?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if cevap == QMessageBox.Yes:
            QApplication.quit()  # Uygulamayı tamamen kapatır
        else:
            event.ignore()  # Pencereyi kapatma


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.veri = None
        self.dogrular = []  # Doğru bilinenler listesi
        self.yanlislar = []

    def init_ui(self):
        layout = QVBoxLayout()

        self.baslangic_satir_edit = QLineEdit(self)
        self.bitis_satir_edit = QLineEdit(self)

        layout.addWidget(QLabel("Başlangıç Satırı:"))
        layout.addWidget(self.baslangic_satir_edit)

        layout.addWidget(QLabel("Bitiş Satırı:"))
        layout.addWidget(self.bitis_satir_edit)

        button_basla = QPushButton("Başla", self)
        button_basla.clicked.connect(self.basla_clicked)
        layout.addWidget(button_basla)

        self.setLayout(layout)
        self.setWindowTitle("Quiz Uygulaması")

    def basla_clicked(self):
        baslangic_satir = int(self.baslangic_satir_edit.text())
        bitis_satir = int(self.bitis_satir_edit.text())

        exel = os.path.join(os.path.dirname(__file__), "abc.xlsx")

        self.veri = pd.read_excel(
            exel, skiprows=baslangic_satir - 1, nrows=bitis_satir - baslangic_satir + 1
        )

        # Shuffle rows of the DataFrame
        self.veri = self.veri.sample(frac=1).reset_index(drop=True)

        self.soru_sorma()

    def soru_sorma(self):
        for index, row in self.veri.iterrows():
            soru = row.iloc[0]
            cevap1 = row.iloc[1]
            cevap2 = row.iloc[2]

            if soru in self.yanlislar or soru in self.dogrular:
                continue  # Eğer soru daha önce yanlış ya da doğru bilindi ise atla

            # PyQt5 dialog penceresini oluştur
            quiz_penceresi = QuizDialog(self, soru, cevap1, cevap2)

            # Ana pencereyi gizle ve QuizDialog penceresini göster
            self.hide()
            quiz_penceresi.exec_()

        # Tüm sorular sorulduktan sonra yanlış bilinenleri tekrar sormak için tekrar çağır
        if self.yanlislar:
            tekrar_sor = QMessageBox.question(
                self,
                "Tekrar Sor",
                "Yanlış bildiklerinizi tekrar sormak ister misiniz?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if tekrar_sor == QMessageBox.Yes:
                self.yanlislar = []  # Yanlış bilinenleri sıfırla
                self.soru_sorma()
            else:
                QMessageBox.information(
                    self, "Bitti", "Quiz tamamlandı!", QMessageBox.Ok
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
