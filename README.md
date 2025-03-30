Overview:
This project is a language learning chatbot built using OpenAI's GPT models and LangChain.
The chatbot interacts with users in a selected foreign language, corrects their mistakes,
tracks errors using SQLite, and provides feedback on areas to improve.

System Architecture:

1. Input Collection:
   - The bot first asks the user for:
     - Known language (e.g., English)
     - Learning language (e.g., French)
     - Current level (Beginner/Intermediate/Advanced)
     - Scenario for conversation (e.g., cafe, airport)

2. Prompt Engineering:
   - LangChain is used to generate structured prompts for the OpenAI LLM.
   - ChatPromptTemplate builds context-aware prompts tailored to the user.

3. Conversation Loop:
   - A loop collects the user’s input, feeds it to the LLM, and returns a response.
   - If the response contains "Correction:", the chatbot extracts it and logs it in the SQLite DB.

4. Mistake Logging:
   - Mistakes are saved in a local SQLite database, including:
     - User’s incorrect sentence
     - Corrected form

5. Feedback Summary:
   - At the end of the session, the bot reads mistakes from the database.
   - It prints a summary of all mistakes and encourages the user to focus on specific grammar/vocabulary issues.

Technologies Used:
- Python 3
- LangChain
- OpenAI GPT model (ChatOpenAI)
- SQLite (for storing user mistakes)

How to Use:
- Replace `YOUR_OPENAI_API_KEY` with your actual OpenAI key before running.
- Start the notebook and follow the prompts.
- Engage in a 5-turn conversation with the bot.
- Review the mistake summary at the end.
