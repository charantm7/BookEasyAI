from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def main():
    load_dotenv()


    model  = init_chat_model("gemini-2.0-flash", model_provider='google_genai')

    history = []

    # using the chatprompttemplate to create a chat template

    # while True:
    #     code_lang = input("Code lang: ")
    #     user_text = input(">> ")
        
    #     if user_text:
    #         system_input = "Respond to the message from the user by giving the code in {language}"
    #         prompt_template = ChatPromptTemplate.from_messages([("system", system_input), ("user", "{text}")])

    #         prompt = prompt_template.invoke({"language": code_lang, "text":user_text})
            
    #         respose = model.invoke(prompt)
    #         print(respose.content)
        
    #     else:

    #         print("Say something")


    # #creating a history for the chat 

    sysmsg = SystemMessage(content="You are the best ai assistant")
    history.append(sysmsg)

    while True:
        user = input('>>')
        if user.lower() == 'exit':
            break

        # it tells the ai that it is a humanmesage
        history.append(HumanMessage(content=user))

        response = model.invoke(history)
        print(response.content)

        history.append(AIMessage(response.content))


    print("History")
    for item in history:
        if item.type == "system":
            print(f'System message: {item.content}')
        
        elif item.type == "human":
            print(f"[User]     {item.content}")
        elif item.type == "ai":
            print(f"[Assistant] {item.content}")
        




        



if __name__ == '__main__':
    main()

