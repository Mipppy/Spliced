from flask import Flask, render_template, redirect, request,session, flash
from flask_session import Session
from cs50 import SQL

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
    textdata = request.form.get("text").split(" ")
    character = request.form.get("character")
    textdata = filter('\n',filter('\r\n',filter(None,textdata)))
    characterVoiceFiles = db.execute("SELECT voicelines.file, voicelines.name FROM character JOIN voicelines ON voicelines.character = character.name WHERE character.name = ?", character)
    neededFiles = []
    arrayOfFiles = []
    notFoundWords =[]
    fullWords = []
    for key in characterVoiceFiles:
        arrayOfFiles.append(key)
    for array in arrayOfFiles:
        for string in textdata:
            if str(array['name']).lower() == str(string).lower():
                neededFiles.append(array['file'])
                fullWords.append(array['file'])
            else:
                notFoundWords.append(str(string).lower())
                fullWords.append(str(string).lower())
    print(fullWords)
    for string2 in notFoundWords:
        
    return redirect("/")