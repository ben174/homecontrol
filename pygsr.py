from pyaudio import PyAudio, paInt16
from wave import open as open_audio
from urllib2 import Request, urlopen
import json
import subprocess
import settings


class Pygsr:
    def __init__(self, file="audio"):
        self.format = paInt16
        audio = PyAudio()
        if hasattr(settings, 'AUDIO_DEVICE_INDEX'):
            self.device_index = settings.AUDIO_DEVICE_INDEX
        elif hasattr(settings, 'AUDIO_DEVICE'):
            for i in range(audio.get_device_count()):
                curr_device = audio.get_device_info_by_index(i)
                print 'Found device: %s' % curr_device['name']
                if curr_device['name'] == settings.AUDIO_DEVICE:
                    print 'Assigning %s (Index: %s)' % (
                        settings.AUDIO_DEVICE, i
                    )
                    self.device_index = i
        elif not hasattr(self, 'device_index'):
            print 'No Audio device specified. Discovering...'
            for i in range(audio.get_device_count()):
                curr_device = audio.get_device_info_by_index(i)
                print 'Found device: %s' % curr_device['name']
                if curr_device['maxInputChannels'] > 0:
                    self.device_index = curr_device['index']
                    print 'Using device: %s' % curr_device['name']
                    break
        print audio.get_device_info_by_index(self.device_index)
        try:
            device = audio.get_device_info_by_index(self.device_index)
            calc_rate = device['defaultSampleRate']
            print 'Discovered Sample Rate: %s' % calc_rate
            self.rate = int(calc_rate)
        except:
            print 'Guessing sample rate of 44100'
            self.rate = 44100
        self.channel = 1
        self.chunk = 1024
        self.file = file

    def convert(self):
        fh = open("NUL", "w")
        subprocess.call(settings.FLAC_CONVERT.split(), stdout=fh, stderr=fh)

    def record(self, time):
        audio = PyAudio()
        stream = audio.open(input_device_index=self.device_index,
                            output_device_index=self.device_index,
                            format=self.format,
                            channels=self.channel,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk
                            )
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

    def speech_to_text(self):
        language = settings.LANGUAGE
        url = "http://www.google.com/speech-api/v1/recognize?lang=%s" % language
        audio = open("%s.flac" % self.file, "rb").read()
        header = {"Content-Type": "audio/x-flac; rate=48000"}
        data = Request(url, audio, header)
        post = urlopen(data)
        response = json.loads(post.read())
        if response['status'] != 0:
            print "Invalid response: %s" % response['status']
            print response
            return None
        phrase = response['hypotheses'][0]['utterance']
        return phrase, response
