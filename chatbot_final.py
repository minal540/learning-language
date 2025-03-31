import openai
from langchain_openai import ChatOpenAI  # Import from langchain-openai
from langchain.prompts import ChatPromptTemplate
import mysql.connector
import time
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='minal',
    database='language_db'
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS mistakes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_input TEXT,
    correction TEXT
)
''')
conn.commit()

openai.api_key = 'api_key'

llm = ChatOpenAI(openai_api_key=openai.api_key, temperature=0.7)

def log_mistake(user_input, correction):
    cursor.execute("INSERT INTO mistakes (user_input, correction) VALUES (%s, %s)", (user_input, correction))
    conn.commit()

def get_mistake_summary():
    cursor.execute("SELECT * FROM mistakes")
    return cursor.fetchall()

def get_openai_response(formatted_prompt):
    max_retries = 3 
    retries = 0
    while retries < max_retries:
        try:
            response = llm.invoke(formatted_prompt)
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            retries += 1
            time.sleep(5 * retries)
    return None  

known_lang = input("What language do you know? ")
learning_lang = input("What language do you want to learn? ")
level = input("What is your current level (beginner/intermediate/advanced)? ")
scene = input("Pick a scene for conversation (e.g., cafe, airport, market, job interview, shopping, doctor's office): ")

prompt_template = ChatPromptTemplate.from_template(
    "You are a helpful language tutor speaking to someone who knows {known_lang} and is learning {learning_lang}. "
    "Their level is {level}. You are in a {scene}. Speak only in {learning_lang}. If the user makes a mistake, "
    "respond with correction, and keep a note of it."
)

chat_history = []
for _ in range(5):
    user_input = input("You: ")
    formatted_prompt = prompt_template.format_messages(
        known_lang=known_lang, learning_lang=learning_lang, level=level, scene=scene
    ) + [{"role": "user", "content": user_input}] 
    
    response = get_openai_response(formatted_prompt) 
    if response is None:
        print("Error during conversation. Unable to get response.")
        break
    
    print("Bot:", response['content'])

    if "Correction:" in response['content']:
        parts = response['content'].split("Correction:")
        correction = parts[1].strip()
        log_mistake(user_input, correction) 

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "bot", "content": response['content']})

mistakes = get_mistake_summary()
print("\nHere are the mistakes you made:")
for i, (id, user_input, correction) in enumerate(mistakes):
    print(f"{i+1}. You said: '{user_input}' -> Correction: '{correction}'")

print("\nFocus on the grammar and vocabulary corrections above to improve!")
