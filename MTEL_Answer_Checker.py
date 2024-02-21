import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import random

correct_messages = [
    "CORRECT: YOU ARE A GENIUS!",
    "CORRECT: EXPECTED, YOU ARE TOO GOOD FOR THIS TEST!",
    "CORRECT: YOU ARE DOING GREAT!",
    "YESSSSS!",
    "CORRECTTTT BUT YOU ALREADY KNEW THAT, THIS WAS JUST A FORMALITY!",
    "CORRECT: EASY MONEY",
    "CORRECT: HOW ARE YOU SO SMART",
    "Correct: I always knew you could do it",
    "WHOOP WHOOP! CORRECT ANSWER",
    "WINNER WINNER!! YOU GOT IT RIGHT",
    "WOW, AGAIN!?!? YOU ARE CORRECT",
    "LETS GO! YOU GOT IT RIGHT!"
]

wrong_messages = [
    "WRONG: THE WRONG ANSWERS ARE WHERE YOU LEARN, I BELIEVE IN YOU",
    "Wrong: \" The best time to study for the MTEL was 20 years ago, the second best time is now \"",
    "Wrong: \" You cannot teach a man anything, you can only help him find it wihin himself \"",
    "Wrong: \" A journey of 1000 miles begins with a signle step \"",
    "Wrong: \"Everything around you that you call life was made up by people that were no smarter than you.\" - Steve Jobs",
    "Wrong: Do not give up",
    "Wrong: The struggle is worth it",
    "No, you are not correct. But this does not mean you should not keep trying. Please continue to think and grow and prosper",
    "Wrong. :(",
    "Not right, sorry",
    "incorrect",
    "not correct",
    "sorry u are wrong",
    "you are wrong, better now then on the test tho !",
    "wrong: you should be happy. imagine if you got all these right, you would be wasting your time studying",
]

def get_hint(solution_text):
    # Extract a substring from the solution text to serve as the hint
    start_index = solution_text.find("Correct Response:") + len("Correct Response:")
    end_index = solution_text.find("Incorrect Response:")
    hint_text = solution_text[start_index+4:end_index].strip()
    return hint_text

def check_answer():
    try:
        user_question = int(question_entry.get())  # Convert to integer
        user_answer = answer_entry.get().upper()  # Convert to uppercase

        if answers[user_question + 1] == user_answer:
            result_message = random.choice(correct_messages)
            display_hint = False
        else:
            result_message = random.choice(wrong_messages)
            display_hint = True

        # Show result message in a new window
        result_window = tk.Toplevel(root)
        result_window.title("Result")
        result_label = tk.Label(result_window, text=result_message)
        result_label.pack(padx=10, pady=10)

        # Display the "Solution?" button in the new window
        solution_button = tk.Button(result_window, text="Solution?", command=lambda: show_solution(user_question))
        solution_button.pack(padx=10, pady=5)

        # Display the "Hint" button only when the answer is wrong
        if display_hint:
            hint_button = tk.Button(result_window, text="Hint? (May give it away or be completely useless)", command=lambda: show_hint(user_question))
            hint_button.pack(padx=10, pady=5)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid question number.")

def show_solution(question_number):
    try:
        solution_window = tk.Toplevel(root)
        solution_window.title("Solution")
        solution_label = tk.Label(solution_window, text=solutions[question_number + 1])
        solution_label.pack(padx=10, pady=10)
    except IndexError:
        messagebox.showerror("Error", "Solution not found.")

def show_hint(question_number):
    try:
        hint_window = tk.Toplevel(root)
        hint_window.title("Hint? (May give it away or be completely useless)")
        hint_label = tk.Label(hint_window, text=hints[question_number + 1])
        hint_label.pack(padx=10, pady=10)
    except IndexError:
        messagebox.showerror("Error", "Hint not found.")

url = "https://www.mtel.nesinc.com/content/PracticeTest/MA065_AnswerKey_85.html#collapseAnswers"
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    span_elements = soup.find_all('span', class_='collapseAnswers')
    answers = [span.text.strip() for span in span_elements]

    solution_elements = soup.find_all('span', class_='collapseObjectives')
    solutions = [span.text.strip() for span in solution_elements]

    hints = [get_hint(solution) for solution in solutions]

    # Create GUI
    root = tk.Tk()
    root.title("Answer Checker")

    question_label = tk.Label(root, text="Question Number:")
    question_label.grid(row=0, column=0, padx=5, pady=5)

    question_entry = tk.Entry(root)
    question_entry.grid(row=0, column=1, padx=5, pady=5)

    answer_label = tk.Label(root, text="Your Answer:")
    answer_label.grid(row=1, column=0, padx=5, pady=5)

    answer_entry = tk.Entry(root)
    answer_entry.grid(row=1, column=1, padx=5, pady=5)

    check_button = tk.Button(root, text="Check Answer", command=check_answer)
    check_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()


