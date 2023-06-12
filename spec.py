import matplotlib.pyplot as plt
import librosa
import numpy as np
SR =48000   

def energy(w):
    l = len(w)
    sigma = np.dot(w,w.T)
    return 10*np.log10(sigma/l)


path = '/home/ohad/BROCA_recorder/mics_test'


fig, (ax1,ax2,ax3) = plt.subplots(nrows=3,figsize=(18,25))
w5,sr = librosa.load(f'{path}/silence_stend.wav',sr=SR,mono=False)
# w5 = w5[1,:]
en5 = energy(w5)
Pxx5, freqs5, bins5, im5 = ax3.specgram(w5,Fs=sr)
ax3.set_title(f"Silnce Stend Mic - refrence, Energy={en5}")


vmin,vmax = im5.get_clim() #set max and min freqs to get all on the same color scale!

w1,sr = librosa.load(f'{path}/stend1_mic_test.wav',sr=SR,mono=False)
# w1 = w1[1,:]
en1=energy(w1)
Pxx1, freqs1, bins1, im1 = ax1.specgram(w1,Fs=sr,vmin=vmin,vmax=vmax)
vmin,vmax = im1.get_clim()
ax1.set_title(f"Speech at 65dB, Energy={en1} dB (stend1_mic_test.wav)")

w2,sr = librosa.load(f'{path}/stend2_mic_test.wav',sr=SR,mono=False)
# w2 = w2[1,:]
en2=energy(w2)
Pxx2, freqs2, bins2, im2 = ax2.specgram(w2,Fs=sr,vmin=vmin,vmax=vmax)
ax2.set_title(f"Speech at 65dB, Energy={en2} dB (stend2_mic_test.wav)")

# w3,sr = librosa.load(f'{path}/speech_70db.wav',sr=SR,mono=False)
# w3 = w3[1,:]
# en3=energy(w3)
# Pxx3, freqs3, bins3, im3 = ax3.specgram(w3,Fs=sr,vmin=vmin,vmax=vmax)
# ax3.set_title(f"Speech at 70dB, Energy={en3} dB")

# w4,sr = librosa.load(f'{path}/white_noise_70db.wav',sr=SR,mono=False)
# w4 = w4[1,:]
# en4=energy(w4)
# Pxx4, freqs4, bins4, im4 = ax4.specgram(w4,Fs=sr,vmin=vmin,vmax=vmax)
# ax4.set_title(f"White noise at 70dB, Energy={en4} dB")

# w6 = w5+w5
# en6=energy(w6)
# Pxx6, freqs6, bins6, im6 = ax6.specgram(w6,Fs=sr,vmin=vmin,vmax=vmax)
# ax6.set_title(f"Silence + Silence, Energy={en6} dB")

fig.supxlabel('Time [sec]',fontsize=23)
fig.supylabel('Frequency [Hz]',fontsize=23)
axes = [ax1,ax2,ax3]
fig.colorbar(im5, ax=axes)

# fig.suptitle(f'Path: {path} \n\n SNR_65dB = {en1-en5} \n SNR_70dB = {en3-en5}',fontsize=23)

fig.savefig(f"{path}/spec.png")