import pyaudio
import logging
import sys
import threading
import wave

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def list_input_devices(p:pyaudio.PyAudio):
        """
            returns dict {device_name:device index} use the dict to pass the index for user selected device
        """
        device_index_dict = {}
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(numdevices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            if (device_info.get('maxInputChannels')) > 0:
                  device_index_dict[device_info.get('name')] = i
        return device_index_dict
    
class Recorder:
    def __init__(self, pyaudio:pyaudio.PyAudio, device_index,
                 rate = 48000, format = pyaudio.paInt16, 
                 channels=1, chunk =2048) -> None:
        self.p = pyaudio
        self.index = device_index
        self.rate = rate
        self.format = format
        self.channels = channels
        self.chunk = chunk
    
    
    def record(self,duration, file, recording_started:super(threading.Event,None)=None):
        stream = self.p.open(format=self.format, channels=self.channels,
                rate=self.rate, input=True,input_device_index = self.index,
                frames_per_buffer=self.chunk)
        if recording_started is not None:
            recording_started.set()
        logging.debug(f'recording {duration} seconds into {file}')
        record_frames = []
        for i in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            record_frames.append(data)
        logging.debug("recording stopped")
        stream.stop_stream()
        stream.close()
        
        waveFile = wave.open(file, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.p.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(record_frames))
        waveFile.close()
        logging.debug(f'saved to {file}')