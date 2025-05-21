import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

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
    result = await chain.ainvoke({"language": language})  # ✅ await + ainvoke
    return result.strip()


async def generate_usernames(theme: str, count: int, language: str) -> list[str]:
    prompt = ChatPromptTemplate.from_template(
        "You are an AI that creates usernames for group chats.\n"
        "The current topic is: \"{theme}\"\n"
        "Generate {count} creative, natural-sounding usernames relevant to that theme.\n"
        "Respond in {language}. Only return a comma-separated list of usernames."
    )
    chain = prompt | llm | StrOutputParser()
    await asyncio.sleep(1)  # ✅ Respecter 1 req/sec avant d’envoyer
    result = await chain.ainvoke({
        "theme": theme,
        "count": count,
        "language": language
    })
    return [name.strip() for name in result.split(",")]
