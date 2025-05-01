from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget,
                             QWidget, QMessageBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QComboBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
import json
from collections import defaultdict
import random


class ArabicPredictorGUI(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.word_probs = defaultdict(dict)
        self.history = []
        self.corrections = {}
        self.load_matrices()
        self.init_ui()
        self.setWindowTitle("نظام توقع الكلمات العربية - Arabic Word Predictor")
        self.resize(1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

    def load_matrices(self):
        """Load word probability matrix"""
        try:
            with open(self.config["word_matrix_file"], 'r', encoding='utf-8') as f:
                self.word_probs = json.load(f)
        except FileNotFoundError:
            QMessageBox.critical(self, "خطأ", "لم يتم العثور على ملف مصفوفة الكلمات")
            exit(1)

    def init_ui(self):
        """Initialize the GUI components"""
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Font setup for Arabic support
        arabic_font = QFont("Arial", 12)
        arabic_font.setStyleStrategy(QFont.PreferAntialias)

        # Input Section
        input_layout = QHBoxLayout()
        self.input_label = QLabel("أدخل كلمة / Enter a word:")
        self.input_label.setFont(arabic_font)
        self.input_field = QLineEdit()
        self.input_field.setFont(arabic_font)
        self.input_field.setPlaceholderText("اكتب كلمة هنا... / Type a word here...")

        # Correction controls
        correction_layout = QVBoxLayout()
        self.correction_label = QLabel("تصحيح الكلمة / Correct word:")
        self.correction_label.setFont(arabic_font)
        self.correction_combo = QComboBox()
        self.correction_combo.setFont(arabic_font)
        self.correct_button = QPushButton("تأكيد التصحيح / Confirm Correction")
        self.correct_button.clicked.connect(self.apply_correction)

        correction_layout.addWidget(self.correction_label)
        correction_layout.addWidget(self.correction_combo)
        correction_layout.addWidget(self.correct_button)

        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addLayout(correction_layout)

        # Suggestions Section
        self.suggestions_label = QLabel("الكلمات المقترحة / Suggested words:")
        self.suggestions_label.setFont(arabic_font)
        self.suggestions_list = QListWidget()
        self.suggestions_list.setFont(arabic_font)
        self.suggestions_list.itemClicked.connect(self.use_suggestion)
        self.suggestions_list.setMinimumHeight(100)

        # Probability Table
        self.prob_table = QTableWidget()
        self.prob_table.setColumnCount(2)
        self.prob_table.setHorizontalHeaderLabels(["الكلمة / Word", "الاحتمالية / Probability"])
        self.prob_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.prob_table.setFont(arabic_font)
        self.prob_table.setMinimumHeight(150)

        # Phrase Generation Section
        self.generate_label = QLabel("إنشاء جملة / Generate phrase:")
        self.generate_label.setFont(arabic_font)

        generate_controls = QHBoxLayout()
        self.phrase_length = QComboBox()
        self.phrase_length.addItems(["5", "8", "10", "15"])
        self.phrase_length.setCurrentIndex(1)
        self.generate_button = QPushButton("إنشاء جملة / Generate Phrase")
        self.generate_button.clicked.connect(self.generate_phrase)

        generate_controls.addWidget(QLabel("طول الجملة / Phrase length:"))
        generate_controls.addWidget(self.phrase_length)
        generate_controls.addWidget(self.generate_button)
        generate_controls.addStretch()

        self.phrase_output = QTextEdit()
        self.phrase_output.setFont(arabic_font)
        self.phrase_output.setReadOnly(True)

        # History Section
        self.history_label = QLabel("التاريخ / History:")
        self.history_label.setFont(arabic_font)
        self.history_list = QListWidget()
        self.history_list.setFont(arabic_font)
        self.history_list.itemClicked.connect(self.load_from_history)
        self.clear_history_button = QPushButton("مسح التاريخ / Clear History")
        self.clear_history_button.clicked.connect(self.clear_history)

        # Add components to main layout
        layout.addLayout(input_layout)
        layout.addWidget(self.suggestions_label)
        layout.addWidget(self.suggestions_list)
        layout.addWidget(self.prob_table)
        layout.addLayout(generate_controls)
        layout.addWidget(self.phrase_output)
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_list)
        layout.addWidget(self.clear_history_button)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Enable prediction on text change with slight delay
        self.suggestion_timer = QTimer()
        self.suggestion_timer.setInterval(300)
        self.suggestion_timer.setSingleShot(True)
        self.suggestion_timer.timeout.connect(self.update_suggestions)
        self.input_field.textChanged.connect(self.suggestion_timer.start)

    def update_suggestions(self):
        """Update suggestions as user types"""
        current_word = self.input_field.text().strip()
        self.suggestions_list.clear()
        self.prob_table.setRowCount(0)

        if not current_word:
            return

        # Update correction combo
        self.correction_combo.clear()
        self.correction_combo.addItem("-- اختر تصحيحا -- / Select correction --")
        if current_word not in self.word_probs:
            self.correction_combo.addItems(sorted(self.word_probs.keys(), key=lambda x: -len(x))[:20])

        if current_word in self.word_probs:
            next_words = sorted(
                self.word_probs[current_word].items(),
                key=lambda x: x[1],
                reverse=True
            )

            # Show top 5 suggestions in list
            for word, prob in next_words[:5]:
                self.suggestions_list.addItem(f"{word} ({prob:.2%})")

            # Show full probability distribution in table
            self.prob_table.setRowCount(len(next_words))
            for row, (word, prob) in enumerate(next_words):
                self.prob_table.setItem(row, 0, QTableWidgetItem(word))
                prob_item = QTableWidgetItem(f"{prob:.2%}")

                # Color code probabilities
                if prob > 0.5:
                    prob_item.setBackground(QColor(200, 255, 200))
                elif prob > 0.2:
                    prob_item.setBackground(QColor(255, 255, 200))

                self.prob_table.setItem(row, 1, prob_item)

    def apply_correction(self):
        """Apply user correction to the current word"""
        current_word = self.input_field.text().strip()
        corrected_word = self.correction_combo.currentText()

        if corrected_word and corrected_word != "-- اختر تصحيحا -- / Select correction --":
            # Record the correction
            self.corrections[current_word] = corrected_word

            # Update the input field
            self.input_field.setText(corrected_word)

            # Add to history
            self.add_to_history(f"{current_word} → {corrected_word}")

            QMessageBox.information(self, "تم التصحيح", f"تم تغيير '{current_word}' إلى '{corrected_word}'")

    def use_suggestion(self, item):
        """Use selected suggestion"""
        suggested_text = item.text()
        suggested_word = suggested_text.split()[0]  # Extract just the word

        # Add to history before changing
        current_word = self.input_field.text().strip()
        if current_word:
            self.add_to_history(f"{current_word} → {suggested_word}")

        self.input_field.setText(suggested_word)
        self.update_suggestions()

    def generate_phrase(self):
        """Generate a phrase of specified length"""
        seed_word = self.input_field.text().strip()
        if not seed_word or seed_word not in self.word_probs:
            self.show_message("الرجاء إدخال كلمة صالحة من المفردات أولاً / Please enter a valid vocabulary word first")
            return

        length = int(self.phrase_length.currentText())
        phrase = [seed_word]
        current_word = seed_word

        for _ in range(length - 1):
            if current_word in self.word_probs and self.word_probs[current_word]:
                # Get top 3 most probable next words
                candidates = sorted(
                    self.word_probs[current_word].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]

                # Randomly select from top 3 with probability weighting
                words, probs = zip(*candidates)
                next_word = random.choices(words, weights=probs, k=1)[0]

                phrase.append(next_word)
                current_word = next_word
            else:
                break

        generated_phrase = " ".join(phrase)
        self.phrase_output.setPlainText(generated_phrase)
        self.add_to_history(f"Generated: {generated_phrase}")

    def add_to_history(self, entry):
        """Add an entry to the history"""
        self.history.append(entry)
        self.history_list.insertItem(0, entry)
        if self.history_list.count() > 50:  # Limit history size
            self.history_list.takeItem(self.history_list.count() - 1)

    def load_from_history(self, item):
        """Load a word from history"""
        text = item.text()
        if "→" in text:
            self.input_field.setText(text.split("→")[-1].strip())
        elif text.startswith("Generated:"):
            self.phrase_output.setPlainText(text[10:].strip())

    def clear_history(self):
        """Clear the history"""
        self.history = []
        self.history_list.clear()

    def show_message(self, text):
        """Show message in the output area"""
        self.phrase_output.setPlainText(text)

    def keyPressEvent(self, event):
        """Handle Enter key for prediction"""
        if event.key() == Qt.Key_Return:
            self.update_suggestions()
        else:
            super().keyPressEvent(event)