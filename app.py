from flask import Flask, render_template, redirect, request, flash, send_file, after_this_request
from cs50 import SQL
import os,wave,random,string, threading,time
from helper import *
dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
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
    try:
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
        for string1 in arrayIter2:
            found = False
            for array in arrayIter:
                if found == True:
                    continue
                if str(array['name']).lower() == str(string1).lower():
                    neededFiles.append(array['file'])
                    fullWords.append(array['file'])
                    found = True
            if found == False:    
                notFoundWords.append(str(string1).lower())
                fullWords.append(str(string1).lower())
        for word in notFoundWords:
            subList = [word]
            for char in word:
                if char == None or char == "":
                    continue
                subList.append(subList.append(char + ".wav"))
            
            neededSubAudioFiles.append(list(filter(None, subList)))        
        for word in fullWords:
            found = False
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

        randIntFor = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
        concatenate_audio_wave(finalList, f"concatFiles\\{randIntFor}.wav",character)
        @after_this_request
        def deleteFileAfterReq(response):
            threading.Thread(target=safe_del, args=(f"{dir_path}\\concatFiles\\{randIntFor}.wav",0)).start()
            return response
        return send_file(f"concatFiles\\{randIntFor}.wav", as_attachment=True, download_name=f"{character} Spliced.wav")
    except Exception as e:
        return render_template("error.html")