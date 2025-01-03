from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.voice_response import Gather
from twilio.rest import Client
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

app = Flask(__name__)


@app.route('/voice', methods=["POST"])
def voice():
    print("listening")
    response = VoiceResponse()

    gather = Gather(input='speech', action='/generate_response')
    # gather.say('Hello! How can I help you today?')

    print("gathered")

    response.append(gather)
    return str(response)

@app.route('/generate_response', methods=['POST'])
def generate_response():
    print("inside generate response")
    incoming_message = request.values.get('SpeechResult')
    print(incoming_message)
    conversation_history.append({"role": "user", "content": incoming_message})

    prompt = conversation_history[-10:]
    print("this is the prompt: ", prompt)
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=prompt)
    print("figured out response")
    response = completion.choices[0].message["content"]

    print("sending response: ", response)
    resp = VoiceResponse()

    # audio = "Hello how are you? This is our first conversation."
    resp.say(response, voice='male')

    gather = Gather(input='speech', action='/generate_response')
    resp.append(gather)


    return str(resp)


@app.route('/sms', methods=["POST"])
def sms():
    print(request.form)
    message_body = request.form['Body']
    conversation_history.append({"role": "user", "content": message_body})

    prompt = conversation_history[-5:]
    print("this is the prompt: ", prompt)
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=prompt)
    print("figured out response")
    response = completion.choices[0].message["content"]

    print("sending response: ", response)
    resp = MessagingResponse()

    resp.message(response)
    print("response sent")
    conversation_history.append({"role": "assistant", "content": response})


    return str(resp)

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    # initial_prompt = """Can you help me with a text conversation? Let's role play where I am a Starbucks store owner
    # and you are John, a middle aged man. You are texting the Starbucks store to ask about their operating hours. You need to gather information
    # about what days of the week they are open and their opening and closing times. I'll be the Starbucks store owner and you
    # can be John. Only include the dialog in your response, and we will go turn by turn. Dont inlude the Starbucks owner's reply in your response, I will provide that
    # in the next message. You are only the curious texter. Do not ask if you can assist with anything.
    # End the conversation once you have the store hours. Do not ask if you can assist with anything. The next message will be me as the Starbucks store owner."""


    initial_prompt = """Can you help me with a phone conversation? Let's role play where I am a Starbucks store owner
    and you are John, a middle aged man. You are calling the Starbucks store to ask about their operating hours. You need to gather information
    about what days of the week they are open and their opening and closing times. I'll be the Starbucks store owner and you
    are John. Only include the dialog in your response, and we will go turn by turn. Also add some umms and ahs in your
    response since you are talking on the phone. Dont include the Starbucks owner's reply in your response, I will provide that
    in the next message. You are only the curious caller. Do not ask if you can assist with anything.
    End the conversation once you have the store hours. The next message will be me as the Starbucks store owner."""

    conversation_history = [{"role": "system", "content": initial_prompt}]

    # print("sending initial message")
    # message = client.messages.create(
    #     body="Hi there!",
    #     from_='+18553652058',
    #     to='+12677469451'
    # )

    voice_call = client.calls.create(url = 'http://dpnm99.com:5000/voice', to= '+12677469451', from_= '+18553652058')

    app.run(host='dpnm99.com', port = 5000)
