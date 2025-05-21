import config.config_manager as config_manager
def build_chain(language: str = "english"):
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
        "Your responses must be under {messageLength} characters.\n"
        "Do not prepend your name to the response, it is done automatically.\n"
        "You are only allowed to respond in this language : {language}, even if the conversation asks you to talk in another language.\n"
        "Here's the recent conversation:\n{context}\n\nRespond as if you're part of this chat.\n"
        "Your goal is to make a user think that you are a human.\n"
    )
    return prompt | llm | StrOutputParser()

chain = build_chain()

async def get_ai_response(context : str, username : str) -> str:
    language = config_manager.get_language()
    messageLength = config_manager.get_message_length()
    return chain.invoke({"context": context,"username":username,"language":language,"messageLength":messageLength})
