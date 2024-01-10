import json
from difflib import get_close_matches

def load_knowledge_base(filepath: str) -> dict:
    with open (filepath, 'r') as file:
        data: dict = json.load(file)
    return data

#save the answers to the json file, so that the chatbot can use them again
def save_knowledge_base(file_path: str, data:dict):
    with open(file_path, 'w') as file:
        json.dump (data, file, indent = 2)

#finds the most simillar question the one already made by the user
def find_best_match (user_question: str, questions: list[str]) -> str | None: 
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

#gets the answer for the question
def get_answer_for_question (question:str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
#chatbot itself
def chat_bot():
    knowledge_base: dict = load_knowledge_base('chatbot/knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer : str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('chatbot/knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')


#start the chatbot
if __name__ == '__main__':
    chat_bot()