import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

import asyncio

llm_call_lock = asyncio.Lock()

async def safe_llm_call(chain, params):
    async with llm_call_lock:
        result = await chain.ainvoke(params)
        await asyncio.sleep(1)  # pause pour respecter le 1 req/sec
    return result

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.8,
    api_key="En0ggVPzctLujrzs3VHFhwHcjCSN8Hwg"
)

async def generate_theme(language: str) -> str:
    prompt = ChatPromptTemplate.from_template(
        "You are an AI that proposes creative group chat themes.\n"
        "Respond in {language}. Only return the theme itself without explanation.\n"
        "Give one original theme for a conversation."
    )
    chain = prompt | llm | StrOutputParser()
    result = await safe_llm_call(chain, {"language": language})
    return result.strip()

async def generate_pseudos_and_personalities(theme: str, count: int, language: str) -> list[dict]:
    prompt = ChatPromptTemplate.from_template(
        "You are an AI that generates {count} player profiles for a group chat themed '{theme}'.\n"
        "For each player, provide a creative username and a short personality description.\n"
        "Respond in {language} with each profile on its own line, formatted exactly as:\n"
        "Pseudo: <username>, Personality: <personality description>\n"
        "Do not add anything else."
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