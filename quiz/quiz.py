import json
import random

def load_questions(filename='questions.json'):
    """Load questions from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def get_user_choice():
    """Prompt user to select different topics."""
    print("Choose a topic: capital of states, cricket questions, General Knowledge")
    choice = input().lower()
    while choice not in ['capital of states', 'cricket questions', 'general knowledge']:
        print("Invalid choice. Please choose from capital of states, cricket questions, or General Knowledge.")
        choice = input().lower()
    return choice

def ask_question(question_data):
    """Ask a question and return whether the user's answer is correct and the correct answer."""
    print(question_data['question'])
    options = question_data['options']
    random.shuffle(options)  
    for idx, option in enumerate(options):
        print(f"{chr(65 + idx)}. {option}")
    
    user_answer = input("Your answer (A, B, C, or D): ").upper()
    option_dict = dict(zip('ABCD', options))
    correct_answer = question_data['answer']
    
    if user_answer in 'ABCD':
        return option_dict[user_answer] == correct_answer, correct_answer, option_dict[user_answer]
    return False, correct_answer, None

def quiz_game():
    """Run the quiz game."""
    questions_data = load_questions()
    choice = get_user_choice()
    questions = questions_data[choice]
    score = 0
    incorrect_answers = []  # To keep track of incorrect answers

    random.shuffle(questions) 

    for question_data in questions:
        is_correct, correct_answer, user_answer = ask_question(question_data)
        if is_correct:
            score += 1
        else:
            incorrect_answers.append({
                "question": question_data['question'],
                "options": question_data['options'],
                "user_answer": user_answer,
                "correct_answer": correct_answer
            })

    if incorrect_answers:
        print("\nHere are the questions you got wrong:")
        for item in incorrect_answers:
            print(f"Question: {item['question']}")
            print(f"Options: {', '.join(item['options'])}")
            print(f"Your Answer: {item['user_answer']}")
            print(f"Correct Answer: {item['correct_answer']}")
            print()  # Print a blank line for better readability
    print(f"Quiz over! Your score: {score}/{len(questions)}")

if __name__ == "__main__":
    quiz_game()
