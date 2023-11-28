# Processamento dos dados brutos da boia do SIODOC

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.io import loadmat
from datetime import datetime
from importlib import reload
sys.path.append('/home/hp/git/ocean-wave')
import buoys
import waveproc
import wavegroup
import wavespread
import waveplot
reload(buoys)
reload(waveproc)
reload(wavegroup)
reload(wavespread)
reload(waveplot)
plt.close('all')

if __name__ == "__main__":

    pth_raw = './data/raw/'
    pth_out = './data/proc/'

    N = 1024
    Fs = 1.0
    t = np.arange(0, N, Fs)

    #carrega arquivos .mat
    hvmat = loadmat(pth_raw + 'heave.mat')
    ptmat = loadmat(pth_raw + 'pitch.mat')
    rlmat = loadmat(pth_raw + 'roll.mat')
    cpmat = loadmat(pth_raw + 'compass.mat')

    #data de todos os arquivos com datetime
    #  0    1    2    3     4    5  
    # ano, mes, dia, hora, min, seg
    data_all = hvmat['heave'][:, [0, 1, 2, 3, 4, 5]]
    datat_all = [datetime(int(data_all[i,0]),int(data_all[i,1]),int(data_all[i,2]),
        int(data_all[i,3])) for i in range(len(data_all))]
    datat1 = np.array(datat_all)

    df_heave = pd.DataFrame(hvmat['heave'][:, 6:], index=datat1)
    df_pitch = pd.DataFrame(ptmat['pitch'][:, 6:], index=datat1)
    df_roll = pd.DataFrame(rlmat['roll'][:, 6:], index=datat1)
    df_compass = pd.DataFrame(cpmat['compass'][:, 6:], index=datat1)

    NFFTs = [
             N,         # 2
             int(N/2),  # 4
             int(N/4),  # 8
             int(N/8),  # 16
             int(N/16), # 32
             int(N/32), # 64
             ]

    for NFFT in NFFTs:

        gl = int(N/NFFT) * 2

        datet = []
        param = pd.DataFrame()
        # for i in range(len(df_pitch)):
        for i in df_heave.index:
        # for i in df_heave.loc['2014-08-01 00:00:00':'2014-08-31 23:00:00'].index:

            datet.append(pd.to_datetime(i))

            print (i)

            n1 = df_heave.loc[i]

            cc, pp, tt = waveproc.waveproc(t=t, s1=n1.values, s2=[], s3=[], Fs=Fs, NFFT=NFFT)

            # concatena os paramertros
            param = pd.concat((param, pp))

        param.index = datet
        param.index.name = 'date'
        param.to_csv(pth_out + '/param_siodoc_{:02d}.csv'.format(gl),
                     float_format='%.4f', index_label='date')