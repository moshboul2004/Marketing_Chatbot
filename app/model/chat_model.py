import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.settings import model





def get_response(username, query, chat_history):
    logging.info("Generating response for the user query.")

    template = """
    You are a helpful marketing assistant. Answer the following questions considering the history of the conversation:
    Chat history: {chat_history} 
    User question: {user_question}

    If the user mentions their name do it, refer to them as that name, otherwise immediately refer to them as "{username}".

    When asked to create a caption, ensure it is engaging, concise, and tailored to the target audience. Use creative language that captures attention and encourages interaction.
    """

    prompt = ChatPromptTemplate.from_template(template)
    logging.info("Prompt template created.")

    chain = prompt | model | StrOutputParser()
    logging.info("Chain created for processing the prompt.")

    response = chain.invoke({
        "chat_history": chat_history,
        "user_question": query,
        "username": username
    })

    logging.info("Response generated from the model.")
    return response


