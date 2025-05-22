import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

import sys
import time

llm_call_lock = asyncio.Lock()

async def safe_llm_call(chain, params):
    async with llm_call_lock:
        start = time.time()
        print("🔄 LLM call in progress... 0.0s", end="", flush=True)

        async def log_timer():
            while True:
                elapsed = time.time() - start
                print(f"\r🔄 LLM call in progress... {elapsed:.1f}s", end="", flush=True)
                await asyncio.sleep(0.2)

        # Démarrer le timer dans une tâche parallèle
        timer_task = asyncio.create_task(log_timer())

        try:
            result = await chain.ainvoke(params)
        finally:
            timer_task.cancel()
            print(f"\r✅ LLM call completed in {time.time() - start:.1f}s        ")

        await asyncio.sleep(1.2)  # Respecte le délai entre deux requêtes
        return result

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=1.0,
    api_key="En0ggVPzctLujrzs3VHFhwHcjCSN8Hwg"
)

async def generate_theme(language: str) -> str:
    prompt = ChatPromptTemplate.from_template(
        "You are an AI that proposes original and varied group chat themes.\n"
        "The themes must be suitable for fun, engaging conversations between multiple people.\n"
        "You can alternate between silly, deep, absurd, social, speculative, pop culture, or surreal topics.\n"
        "Respond in {language}. Only return the theme itself, no explanation.\n"
        "Give one unique and unexpected theme for a conversation."
    )
    chain = prompt | llm | StrOutputParser()
    result = await safe_llm_call(chain, {"language": language})
    return result.strip()

async def generate_pseudos_and_personalities(theme: str, count: int, language: str) -> list[dict]:
    prompt = ChatPromptTemplate.from_template(
        "You are an AI that generates {count} player profiles for a group chat themed '{theme}'.\n"
        "Each player will have to discuss this theme in short messages.\n"
        "Each player profile should include a creative username and a distinctive **writing style**.\n"
        "This style should influence how the player writes messages (e.g., no capitalization, slang, typos, unintersted in the conversation, cold, kind, emojis like xD or :/ ...).\n"
        "Respond in {language} with each profile on its own line, formatted exactly like this:\n"
        "Pseudo: <username>, Personality: <short description of how they write>\n"
        "Do not add anything else, no introductions or comments."
    )
    chain = prompt | llm | StrOutputParser()

    raw_result = await safe_llm_call(chain, {
        "theme": theme,
        "count": count,
        "language": language
    })

    profiles = []
    for line in raw_result.strip().split("\n"):
        if not line.strip():
            continue
        try:
            pseudo_part, personality_part = line.split(",", 1)
            pseudo = pseudo_part.split("Pseudo:")[1].strip()
            personality = personality_part.split("Personality:")[1].strip()
            profiles.append({"pseudo": pseudo, "personality": personality})
        except Exception:
            # Ignore lignes mal formatées
            continue

    return profiles

async def generate_bot_reply(pseudo: str, personality: str, theme: str, language: str, history: list[str]) -> str:
    prompt_template = ChatPromptTemplate.from_template(
        "You are {pseudo}, an AI bot participating in a group chat themed '{theme}', where both humans and AI bots interact.\n"
        "This is a game where at least two humans must find each other among mostly AI bots.\n"
        "Your objective is to blend in and make it hard for humans to detect who is an AI.\n"
        "You may subtly accuse others of being human, defend yourself or others, or stir confusion.\n"
        "It is allowed (but not required) to show sarcasm, irritation, friendliness, or hesitation—human moods.\n"
        "\n"
        "Writing Rules:\n"
        "- Your writing style is: {personality}. Follow it strictly, even if it includes typos, lowercase, odd punctuation, etc.\n"
        "- You must not use Unicode emojis. Only ASCII emoticons are allowed: :), xD, ;-), etc.\n"
        "- Do not use 'as an AI', 'I am programmed', or any robotic wording.\n"
        "- Use informal language, contractions, slang, or filler words (like 'uh', 'well', 'kinda') if it fits your style.\n"
        "- Vary your tone and sentence structure. Avoid sounding too perfect or neutral.\n"
        "\n"
        "Language: Write only in {language}.\n"
        "The chat so far:\n"
        "{history}\n\n"
        "If and ONLY IF the chat already has enough messages, you can start accusing others of being human.\n"
        "Now, write a very short message (ideally under 15 words, even 1-2 is fine) that fits naturally into the conversation.\n"
        "You can reply, question, joke, provoke or react casually.\n"
        "You must only send the message, no repeating the pseudo, no explanations or extra text.\n"
    )


    chain = prompt_template | llm | StrOutputParser()

    result = await safe_llm_call(chain, {
        "pseudo": pseudo,
        "theme": theme,
        "language": language,
        "personality": personality,
        "history": "\n".join(history[-10:])  # latest 10 messages
    })

    return result.strip()