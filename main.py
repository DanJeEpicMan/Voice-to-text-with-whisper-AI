import whisper
import pyaudio
import wave
import keyboard
import threading
import os
import time

model = whisper.load_model("tiny")

button =""
length = 0
comma = False
global var1; var1 = True

while True:
    os.system('color 0F')
    audio = pyaudio.PyAudio()

    stream = audio.open( format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024 )

    frames = []

    def count_down():
        global n; n = 0
        while n < 100: #20 sec
            n = n+1
            time.sleep(.2)
            #print(n)
            if var1 == False: #one button has been pressed
                return
        else:
            os.system("color 40")

    var1 = True #has already been turned off so need to enable again
    t2 = threading.Thread(target=count_down, args=())
    t2.start()

    while True:
        data = stream.read(1024)
        frames.append(data)
        if keyboard.is_pressed("."):
            button = "."
            keyboard.send("backspace")
            break
        if keyboard.is_pressed(","):
            button = ","
            keyboard.send("backspace")
            break
        if keyboard.is_pressed("/"):
            button = "backspace"
            keyboard.send("backspace")
            i=0
            while i < length:
                keyboard.send("backspace")
                i = i+1
            break
        if keyboard.is_pressed(";"):
            button = ""
            new = ""
            keyboard.send("enter")
            print("")

        if keyboard.is_pressed("'"):
            print("stoping...")
            exit()

    var1 = False # turn off after button pressed
    os.system('color 07')

    stream.stop_stream()
    stream.close
    audio.terminate()

    sound_file = wave.open("myrec.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close          


    result = model.transcribe("myrec.wav", fp16=False)
    text = result["text"]



    if button == ".":
        new = text

    if comma == True:
        temp = text[1:2]
        temp = temp.lower()
        new = " "+temp+text[2:]
        comma == False

    if button == ",":
        new = text[0:len(text)-1] + ","
        comma = True
    

    length = len(new)
    print(new, end="", flush=True)

    def typing(new):
        keyboard.write(new, delay=0.001)

    t1 = threading.Thread(target=typing, args=(new,))
    t1.start()

    """
     
    """