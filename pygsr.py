from pyaudio import PyAudio, paInt16
from wave import open as open_audio
from urllib2 import Request, urlopen
from os import system
from json import loads
import urllib2
import subprocess

class Pygsr:
    def __init__(self, file="audio"):
        self.format = paInt16
        self.rate = 44100
        self.channel = 1
        self.chunk = 1024
        self.file = file

    def convert(self):
        fh = open("NUL","w")
        subprocess.call(['flac', '-f', self.file], stdout=fh, stderr=fh)


    def record(self, time, device_i):
        audio = PyAudio()
        #print audio.get_device_info_by_index(1)
        stream = audio.open(input_device_index=device_i,output_device_index=device_i,format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        print "Recording..."
        frames = []
        for i in range(0, self.rate / self.chunk * time):
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        print "Recording Complete"
        stream.close()
        audio.terminate()
        write_frames = open_audio(self.file, 'wb')
        write_frames.setnchannels(self.channel)
        write_frames.setsampwidth(audio.get_sample_size(self.format))
        write_frames.setframerate(self.rate)
        write_frames.writeframes(''.join(frames))
        write_frames.close()
        self.convert()

    def speech_to_text(self, language):
        url = "http://www.google.com/speech-api/v1/recognize?lang=%s" % language
        file_upload = "%s.flac" % self.file
        audio = open(file_upload, "rb").read()
        header = {"Content-Type": "audio/x-flac; rate=48000"}
        data = Request(url, audio, header)
        try:
            post = urlopen(data)
            response = post.read()
            phrase = loads(response)['hypotheses'][0]['utterance']
            return phrase, response
        except urllib2.HTTPError, err:
            if err.code == 400:
                 return "Error: No se pudo reconocer", "400"
