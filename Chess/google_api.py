#taken from: https://realpython.com/python-speech-recognition/#putting-it-all-together-a-guess-the-word-game
import random
import time

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    while True:
        # set the list of words, maxnumber of guesses, and prompt limit
        pool = ["rook", "b4"]

        # create recognizer and mic instances
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        # show instructions and wait 3 seconds 
        print("Say something:\n")
        time.sleep(1)

        while True:
            print('Speak!')
            guess = recognize_speech_from_mic(recognizer, microphone)
            #print("this is guess: ",guess["transcription"], '\n')
    
            # test = guess["transcription"]["alternative"]
            # for item in test.items():
            #      print(item)
            choices = []
            for alt in guess["transcription"]: #["alternative"]:cho
                for newalt in alt["alternative"]:
                    print(newalt)
                # if choice in pool:
                #     ret= True
                # ret= False
                #choices.append(choice['transcript'])
            
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))

        # show the user the transcription
        #print(guess["transcription"])
        print('\n',"You said: {}".format(guess["transcription"]))
