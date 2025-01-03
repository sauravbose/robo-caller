import speech_recognition
# import pyttsx3
import openai
from subprocess import call as speak
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
recognizer = speech_recognition.Recognizer()

initial_prompt = """Can you help me with a phone conversation? Let's role play where I am a Starbucks store owner
and you are me. You are a middle aged man. You are calling the Starbucks store to ask about their operating hours. You need to gather information
about what days of the week they are open and their opening and closing times. I'll be the Starbucks store owner and you
can be me. Only include the dialog in your response, and we will go turn by turn. Also add some umms and ahs in your
response since you are talking on the phone. Dont inlude the Starbucks owner's reply in your response, I will provide that
in the next message. You are only the curious caller. Do not ask if you can assist with anything.
End the conversation once you have the store hours. The next message will be me as the Starbucks store owner."""

voice = "Victoria"
conversation_history = [{"role":"system", "content":initial_prompt}]

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic, phrase_time_limit = 5)

            transcription = recognizer.recognize_google(audio)
            transcription.lower()
            print(transcription)
            conversation_history.append({"role": "user", "content": transcription})


            prompt = conversation_history[-5:]
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                      messages = prompt)
            response = completion.choices[0].message["content"]
            print(response)
            speak(['say', '-v', voice, response])
            conversation_history.append({"role": "assistant", "content": response})


    except KeyboardInterrupt:
        raise

    except:
        recognizer = speech_recognition.Recognizer()
        continue


# from twilio.rest import Client
# account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
# client = Client(account_sid,auth_token)
#
# call = client.calls.create(twiml = '<Response><Say>Hello!</Say></Response>', to= '+12677469451', from_= '+18553652058')
