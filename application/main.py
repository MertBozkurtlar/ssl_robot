import sys
import torch
import os
import numpy as np
from modules import input

loc = os.path.abspath("../data/trainings")
sys.path.insert(0, loc)
import Resnet
model_loc = os.path.abspath(f"{loc}/vm_model.pth")
device = "cpu"

def mic_turntable_pipeline():
    '''
    Pipeline to run the program on realtime mode
    Starts the microphone stream, and feeds it with the callback function that will be called in the input loop
    '''
    # Model #
    global device
    global vm_net
    global turntable

    turntable = False
    vm_net = model.ResNet(model.Bottleneck, layers=[3, 4, 6, 3], num_classes=73).to(device)
    vm_net.load_state_dict(torch.load(model_loc, map_location=device))
    vm_net.eval()
    input.input_init(pred_callback)

    
def pred_callback(rec):
    '''
    Callback function to be called by (function) input.input_init
    Takes the stft of recorded audio and feeds it to the model,
    then turns the turntable by the predicted angle
    '''
    count = 0
    signal = librosa.util.normalize(rec)
    spectogram = librosa.stft(signal, n_fft=400, hop_length=160)
    frame = spectogram[:,:,:-1]
    phase = np.angle(frame)
    phase = torch.from_numpy(phase)
    phase = phase.reshape(1,8,201,20)

    # Prediction
    pred = vm_net(phase)
    prediction = pred[0].argmax()
    prediction = prediction * 5 if prediction != 72 else "silent"
    os.system('clear')
    print(f"{count}: {prediction}")
    count += 1
        

#TODO: To be implemented
def turn_table(degree):
    '''
    Helper function for (function) pred_callback
    Opens a serial connection to turntable and rotates it by given degree
    '''
    # import serial
    # #400[/deg] (144000 -> 360deg)
    # ser = serial.Serial('/dev/ttyUSB0', baudrate=38400)
    # conv_degree = -degree * 400
    # code = "$I" + str(conv_degree) + ",3¥r¥n"
    # ser.write(b'0=250¥r¥n')
    # ser.write(b'1=1000¥r¥n')
    # ser.write(b'3=100¥r¥n')
    # ser.write(b'5=50¥r¥n')
    # ser.write(b'8=32000¥r¥n')
    # ser.write(b'$O¥r¥n')

    # ser.write(code.encode())
    # ser.close()
    
mic_turntable_pipeline()