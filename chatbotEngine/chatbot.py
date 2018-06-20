#!/usr/bin/python3
import os
import aiml
import nltk
import subprocess
from botKernel import botKernel
from autocorrect import spell
import pyrebase
from nltk.tokenize.moses import MosesDetokenizer
import spellchecker

# Brain file used to boost startup time
BRAIN_FILE="brain.dump"

EXIT_FLAG=False

# Config of Firebase live database
config = {
  "apiKey": "AIzaSyDvBh8NnGf58sVj3Wj2F-o8vsZGfdRWigE",
  "authDomain": "chatbotdb-5070d.firebaseapp.com",
  "databaseURL": "https://chatbotdb-5070d.firebaseio.com",
  "storageBucket": "chatbotdb-5070d",
}
# Initialisin firebase database
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Using default AIML kernel
#chatbotKernel = aiml.Kernel()
chatbotKernel = botKernel()

# To boost the startup speed of the chatbot it is
# possible to save the parsed aiml files as a dump.
# This code checks if a dump exists. if not
# it loads the aiml from the xml files
# and saves the brain dump.
if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    chatbotKernel.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    ## Uncomment the desired learning set and ensure that the old brain.dump is deleted
    chatbotKernel.learn("std-startup.aiml")
    #chatbotKernel.learn("std-startup1.aiml")
    #chatbotKernel.learn("std-startup2.aiml")
    chatbotKernel.respond("load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    chatbotKernel.saveBrain("brain.dump")

# Default values that characterise the chatbot	
BOT_PREDICATES = {
    "name": "Chatty",
    "birthday": "January 1st 2018",
    "location": "Tokyo",
    "master": "Nijo",
    "website":"",
    "gender": "Female",
    "age": "1",
    "size": "too big",
    "religion": "I am god",
    "party": ""
}	

for key,val in BOT_PREDICATES.items():
    chatbotKernel.setBotPredicate(key, val)


# ------- ANDROID & WEB APP------ #
def stream_handler(post):    
        input = db.child("messages").child("user").get()
        if input.val() is not None:
            input_text = input.val()["message"]
            if input_text == "exit" or input_text == "close":
                response = "See you next time!"
            else:
                # process the input here (NLP):
                detokenizer = MosesDetokenizer()
                tokens = nltk.word_tokenize(input_text)
                corrected_tokens = []
                # Spellcheck each word
##                for word in tokens:
##                    # Autocorrect words
##                    corrected_tokens.append(spellchecker.correct(word))
##                tokens = detokenizer.detokenize(corrected_tokens, return_str=True)
                # end NLP
                # comment next line if NLP is needed
                tokens = detokenizer.detokenize(tokens, return_str=True)
                response = chatbotKernel.respond(tokens)
            data = {
                "id": "chatbotid123",
                "message": response,
                "sender": "chatbot"
            }

            db.child("messages").child("chatbot").set(data)

my_stream = db.child("messages").child("user").stream(stream_handler, None)

## ------- END ANDROID & WEB APP ------- #

## ------- IDLE ---------- #
## Uncomment to interact with bot using idle

## Endless loop which passes the use input to the chabot and prints
## its response. It also stores both user and bot responses on a database.
##while True:
##    input_text = input(">>> ")
##    if input_text == "exit" or input_text == "close":
##        response = "See you next time!"
##        EXIT_FLAG=True
##    else:
##        # process the input here (NLP):
##        detokenizer = MosesDetokenizer()
##        tokens = nltk.word_tokenize(input_text)
##        corrected_tokens = []
##        for word in tokens:
##            # Spellcheck each word
##            corrected_tokens.append(spelchek.correct(word))
##            tokens = detokenizer.detokenize(corrected_tokens, return_str=True)
##        # end NLP
##        response = chatbotKernel.respond(tokens)
##    print(response)
##    # Text-to-Speech
##    #response = response.replace(" ","_")
##    #subprocess.call('espeak -ven+f1 -g 10 -s 160 '+response, shell=True)
##    if EXIT_FLAG:
##        exit()
    
