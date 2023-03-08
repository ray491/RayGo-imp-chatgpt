import spacy
import openai
import random
import PySimpleGUI as sg
import concurrent.futures



def generate_response(prompt, entities, sentiment):
    try:
        if len(entities) == 0:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Chatbot: I'm not sure what you're asking about. Can you provide more context?\n{prompt}",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text
        else:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=(
                    f"Chatbot: You asked about the following entities: {', '.join(entities)}. How can I help you with that? (Sentiment: {sentiment})\n"
                    f"{prompt}"
                ),
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text
        return response
    except Exception as e:
        print(f"Error: {e}")
        response = "Sorry, I encountered an error. Can you try asking your question again?"
        return response

def chatbot():
    nlp = spacy.load("en_core_web_sm")
    openai.api_key = "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"


    # define the GUI layout
    layout = [
        [sg.Text("Welcome to the RayGo imp ai!")],
        [sg.Multiline(size=(60, 20), key="-CHAT-")],
        [sg.InputText(key="-IN-", size=(60, 1)), sg.Button("Send")],
    ]

    # create the GUI
    window = sg.Window("A.I", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Send":
            user_input = values["-IN-"]

            if user_input.lower() == "hello":
                response = "Hello there!"
            elif user_input.lower() == "how are you":
                response = "I'm doing well, thank you. How about you?"
            elif user_input.lower() == "Who is your creator?":
                response = "Ray Achakzai"
            elif user_input.lower() == "what's your name":
                response = "My name is Chatbot. Nice to meet you!"
            elif user_input.lower() == "bye":
                response = "Bye! Have a great day."
                window.close()
                break
            else:
                doc = nlp(user_input)
                entities = []
                for ent in doc.ents:
                    entities.append(ent.text)
                sentiment = doc.sentiment
                if sentiment >= 0.5:
                    sentiment = "positive"
                elif sentiment <= -0.5:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_response = executor.submit(generate_response, user_input, entities, sentiment)
                    response = future_response.result()

            # update the chat window with the response
            window["-CHAT-"].print(f"You: {user_input}\n")
            window["-CHAT-"].print(f"Chatbot: {response}\n")


    window.close()

chatbot()
