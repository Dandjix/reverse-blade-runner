def build_chain():
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_mistralai.chat_models import ChatMistralAI

    llm = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.8,
        api_key="En0ggVPzctLujrzs3VHFhwHcjCSN8Hwg"
    )

    prompt = ChatPromptTemplate.from_template(
        "You are user named {username} in a group chat.\n"
        "Keep your responses short.\n"
        "Do not prepend your name to the response, it is done automatically.\n"
        "Here's the recent conversation:\n{context}\n\nRespond as if you're part of this chat:"
    )
    return prompt | llm | StrOutputParser()

chain = build_chain()

async def get_ai_response(context: str,username : str) -> str:
    return chain.invoke({"context": context,"username":username})
