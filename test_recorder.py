import pyaudio
import recorder

p = pyaudio.PyAudio()
device_dict = recorder.list_input_devices(p)
print("----------------------record device dict---------------------")
print(device_dict)
print("-------------------------------------------------------------")
device_index = int(input('device index:'))

r = recorder.Recorder(p, device_index)
r.record(5,'test.wav')