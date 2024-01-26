import wave,os,time

dir_path = os.path.dirname(os.path.realpath(__file__))

def concatenate_audio_wave(audio_clip_paths, output_path,character):
    try:
        data = []
        for clip in audio_clip_paths:
            if clip == "":
                clip = ".wav"
            w = wave.open(f"{dir_path}\\voiceclips\\{character}\\"+clip, "rb")
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
        output = wave.open(output_path, "wb")
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()
    except Exception as e:
        None
def safe_del(filepath,recursionCounter):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        else:
            return False
    except Exception as e:
        time.sleep(1)
        if recursionCounter < 15:
            safe_del(filepath,recursionCounter+1)
        return e