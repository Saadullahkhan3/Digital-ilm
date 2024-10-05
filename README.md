# 📖 Digital Ilm

Learn effortlessly—no login required for students to attempt quizzes, just a name. Ideal for quick tests or environments where authentication is an issue, such as classrooms. Only tutors need to authenticate.

Digital Ilm is a Django-based multiple-choice question (MCQ) platform designed to facilitate seamless interaction between tutors and students. It simplifies the process of submitting, answering, and reviewing questions while focusing on user-friendly functionality.

> Watch Demo video on Youtube: [Digital ilm - Demo](https://youtu.be/ALe6aF5nnGM?si=GEYBr4AFiNU26pZ2)

---

## 🌟 **Features**
**1. MCQ Platform**

- **Tutor-side:** Tutors can submit question sheets for students to attempt.
- **Student-side:** Students can participate without needing to create an account, making it perfect for environments where authentication is a barrier.

**2. Leaderboard**
- After completing a question sheet, students are redirected to a leaderboard.
- There are two views of the leaderboard:
    1. **Redirected View:** When students are redirected after completing a question sheet, their result appears at the top of the leaderboard with a special card and a shareable link.
    2. **General View:** Anyone visiting the leaderboard sees a list of all participants and their scores.

---

### 💻 **Tech Stack:**
- Python
- Django
- HTML
- CSS
- Bootstrap(4 & 5)
- JavaScript | AJAX
- Git & GitHub
  
## 🛠️ **Installation**

- `Python` 3 or higher: This project is developed in `Python 3.12.5`

_Virtual Environment is recommended!_
### Virtual Environment:

- Create: `python -m venv .venv`
- Activate: 
    - Windows: `.venv\Scripts\activate`
    - Unix(Mac/Linux): `source .venv/bin/activate`
- Install **Django**: `pip install django==4.1.13`
- Deactivate(when no longer needed): `deactivate`

### Setup Digital ilm:
- Clone this repository: `git clone https://github.com/Saadullahkhan3/Digital-ilm.git`
- Open terminal in the same directory, where repo was cloned.
- Activate virtual environment.
- Change path into cloned repository directory: `cd Digital-ilm`
- Change path into Django project: `cd Digitalilm`
- Migrate: `python manage.py migrate`
- Start server: `python manage.py runserver`

### Accessing the App
- Navigate to `http://localhost:8000/` in your browser to ensure the server is running properly.

---

## 🧩 **User Roles**
### Tutor
- Tutors can:
    - Register an account.
    - Create, edit, or delete their question sheets.
    - View all question sheets they’ve submitted.
    - Access a personalized dashboard to manage their content.

### Student
- Students can:
    - Submit answers to any question sheet.
    - Provide just their name when attempting quizzes (no login required).
    - View their score on the leaderboard after quiz completion.
    - Share their leaderboard position through a unique URL.

---

## 🧩 **Model Descriptions**
### QuestionSheet
Represents a sheet containing multiple questions.

- **Fields:**
    - `title`: The name of the question sheet.
    - `tutor`: A foreign key reference to the Tutor (Django's built-in User model).
    - `level`: The difficulty level of the question sheet.

- **Methods:**
    - `all_questions()`: Returns all associated questions.
    - `all_students()`: Returns all students who attempted this sheet.

### Question
Represents individual questions in a question sheet.

- **Fields:**
    - `question`: The text of the question.
    - `answer`: The correct answer (choices: 'a', 'b', 'c', 'd').
    - `a`, `b`, `c`, `d`: The options `a` and `b` are mandatory, while `c` and `d` are optional. This allows for flexibility in providing either **2**, **3**, or **4** answer choices.

- **Methods:**
    - `answer_with_id()`: Returns the answer along with the question ID.
    - `all()`: Returns a dictionary containing the question id, question text, all available option values, and the correct option.

### Student
Represents a student who attempts a question sheet.

- **Fields:**
    - `name`: The student’s name.
    - `score`: The student’s score after completing the question sheet.
    - `attempted_sheet`: A foreign key linking to the QuestionSheet.

---

## 🧩 **Key Views and Functionalities**
### Explore Quizzes
- Allows users to browse and select question sheets to attempt.

### Submit Answers
- Upon submission, the system checks each answer against the correct ones stored in the database.
- The student’s score is calculated and saved.

### Leaderboard
- Anyone can view students' names and their scores for any specific question sheet.
- Students who are redirected after completing a question sheet have their result displayed at the top of the leaderboard with a special card and a shareable URL.

### Tutor Profile
- Tutors can view their personal dashboard to see and manage the question sheets they have submitted.

---

## 🧩 **URLs**
### General
- `'/'`: Home page.
- `'learn/'`: Explore quizzes page.

### Question Sheet
_Two different URLs but same work_
- `'/<int:question_sheet_id>/'`: Displays a specific question sheet by ID.
- `'/<int:question_sheet_id>/sheet/'`: Displays a specific question sheet by ID.

### Leaderboard
- `'/<int:question_sheet_id>/leaderboard/'`: Displays the leaderboard for a specific question sheet.

### Tutor
- `'register/'`: Tutor registration page.
- `'tutor/'`: Tutor profile page.
- `'confirm-logout/'`: Confirmation page for logout actions.

#### Tutor Tools
- `'create-question-sheet/'`: Create a new question sheet.
- `'/<int:question_sheet_id>/edit/'`: Edit an existing question sheet.
- `'/<int:question_sheet_id>/delete/'`: Delete a question sheet.

**Internal Utility Endpoints**
- `'get-question-form/'`: AJAX endpoint for dynamically adding question forms.

---

> Made with kindness through the collaboration of Saadullah Khan and Shayan Adnan. 🙌

---

<h2 id="saadullah-khan"><a href="https://www.linkedin.com/in/saadullahkhan3/">🔗 Saadullah Khan</a></h2>
<h2 id="shayan-adnan"><a href="https://www.linkedin.com/in/shayan-adnan-29a1102a5/">🔗 Shayan Adnan</a></h2>
