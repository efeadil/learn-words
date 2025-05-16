# learn-words
# 📚 Learn Words - English Vocabulary Quiz App

This is a simple interactive PyQt5 application that quizzes users on English vocabulary from an Excel file. It supports audio feedback for correct and incorrect answers, making learning more engaging.

## 🚀 Features

- Select a custom range of rows from the Excel file
- Randomized question order
- Audio feedback for correct/incorrect answers
- Option to retry incorrect answers
- Clean and beginner-friendly GUI



---

## ⚙️ Installation

### 1. Install required libraries

```bash
pip install PyQt5 pandas

2. Clone or download the project
 git clone https://github.com/efeadil/learn-words.git
cd learn-words
3. Add your Excel file
Make sure you have an Excel file named abc.xlsx in the root folder with the following structure:

Word (Question)	Hint	Answer
apple	fruit	elma

It must contain three columns: question, hint, and correct answer.

4. Add sound files
Place these .wav files in the project folder:

correct_sound.wav — plays on correct answers

incorrect_sound.wav — plays on wrong answers
▶️ Running the App
Run the Python script:
 python pwt5.py
 
 Then follow the on-screen instructions to start the quiz.