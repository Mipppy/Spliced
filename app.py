from flask import Flask, render_template, redirect, request,session, flash
from flask_session import Session
from cs50 import SQL
import os,wave
dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///new.db")

@app.route("/", methods=["GET", "POST"])
def home():
    if (request.method == "POST"):
        None
    else:
        characters = db.execute("SELECT name FROM character")
        return render_template("index.html", characters=characters)
    
@app.route("/createaudio", methods=["POST"])
def createfile():
    textdata = request.form.get("text")
    textdata = ' '.join(filter(None, textdata.replace('\r\n', ' ').split('\n')))
    textdata = [word for word in textdata.split(" ") if word] 
    character = request.form.get("character")
    characterVoiceFiles = db.execute("SELECT voicelines.file, voicelines.name FROM character JOIN voicelines ON voicelines.character = character.name WHERE character.name = ?", character)
    neededFiles,arrayOfFiles,notFoundWords,fullWords,neededSubAudioFiles,finalList = [],[],[],[],[],[]
    for key in characterVoiceFiles:
        arrayOfFiles.append(key)
    arrayIter = list(arrayOfFiles)
    arrayIter2 = list(textdata)
    for string in arrayIter2:
        found = False
        for array in arrayIter:
            if found == True:
                continue
            if str(array['name']).lower() == str(string).lower():
                neededFiles.append(array['file'])
                fullWords.append(array['file'])
                found = True
        if found == False:    
            notFoundWords.append(str(string).lower())
            fullWords.append(str(string).lower())
    for word in notFoundWords:
        subList = [word]
        for char in word:
            if char == None or char == "":
                continue
            subList.append(subList.append(char + ".wav"))
        
        neededSubAudioFiles.append(list(filter(None, subList)))        
    for word in fullWords:
        found = False
        print(dir_path+'\\voiceclips\\'+character+'\\.wav')
        finalArr,otherArray,finalSound = [],[],""
        for arr in neededSubAudioFiles:
            if str(arr[0]) == word:
                finalArr = arr
                found = True
        if found == True:
            finalArr.pop(0)
            for arr in finalArr:
                finalList.append(arr)
            finalList.append("")                
        else:
            finalList.append(word)
            finalList.append("")
    concatenate_audio_wave(finalList, "concatFiles\\out.wav",character)
    return redirect("/")

def concatenate_audio_wave(audio_clip_paths, output_path,character):
    data = []
    for clip in audio_clip_paths:
        if clip == "":
            clip = ".wav"
        print(f"{dir_path}\\voiceclips\\{character}\\"+clip)
        w = wave.open(f"{dir_path}\\voiceclips\\{character}\\"+clip, "rb")
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
    output = wave.open(output_path, "wb")
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()
