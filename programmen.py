from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI

def main():
    # Create the LLM (Large Language Model) instance
    llm = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.25,
        api_key="En0ggVPzctLujrzs3VHFhwHcjCSN8Hwg"  # Consider using env vars instead
    )

    # Create the prompt template
    prompt = ChatPromptTemplate.from_template("Make a joke in the language : {language}")

    # Output parser for string outputs
    output_parser = StrOutputParser()

    # Create the chain: prompt -> model -> parse
    chain = prompt | llm | output_parser

    # Call the chain with input
    output = chain.invoke({"language": "Deutsch"})

    print(output)

if __name__ == "__main__":
    main()
