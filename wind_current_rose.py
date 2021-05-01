# Processamento dos dados de corrente e vento do SIODOC


import os
import numpy as np
import pandas as pd
# import windrose
# from windrose import WindroseAxes
from matplotlib import pyplot as plt
from windrose import WindroseAxes
plt.close('all')

def waverose(inte, dire, figsz, nsector, radsize, xsize, leg, bbx):

    def new_axes():
        fig = plt.figure(figsize=figsz, dpi=80, frameon=False)
        rect = [0.1, 0.1, 0.6, 0.8]
        ax = WindroseAxes(fig, rect, axisbg='w')
        fig.add_axes(ax)
        return ax, fig

    ax, fig = new_axes()

    def set_legend(ax, bbx):
        l = ax.legend(loc="center right", borderaxespad=bbx)
        # l.get_frame().set_fill(False) #transparent legend
        plt.setp(l.get_texts(), fontsize=20, weight='normal')

    ax.bar(dire, inte, normed=True, bins=5, opening=0.8,
           edgecolor='white', nsector=nsector)
    ax.grid(True, linewidth=1.5, linestyle='dotted')

    ax.set_radii_angle(fontsize=radsize)
    ax.set_xticklabels(ax.theta_labels, fontsize=xsize)
    ax.set_radii_angle(fontsize=radsize)
    ax.set_xticklabels(ax.theta_labels, fontsize=xsize)

    if leg == 'on':
        set_legend(ax, bbx)

    return ax, fig


if __name__ == '__main__':

    pathname = os.environ['HOME'] + '/gdrive/siodoc/data/proc/'

    dateparse = lambda x: pd.datetime.strptime(x, '%d %m %Y %H %M %S')

    df = pd.read_csv(pathname + 'janis_data.dat', sep='\s+', parse_dates=[[0,1,2,3,4,5]],
                       header=None, date_parser=dateparse, index_col=['0_1_2_3_4_5'])

    df['cs1'] = df[18] / 100 * 1.94 # para nos
    df['cd1'] = df[9] - 23.4
    df['ws'] = df[68] * 1.94 #(para nós)
    df['wd'] = df[66] - 23.4

    df['cd1'].loc[df.cd1 < 0] = df['cd1'].loc[df.cd1 < 0] + 360
    df['wd'].loc[df.cd1 < 0] = df['wd'].loc[df.cd1 < 0] + 360

    # df['cd1'] = 0

    fig = plt.figure(figsize=(1, 1), dpi=None, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect).from_ax()
    ax.bar(df.wd, df.ws, normed=True, opening=0.8, edgecolor='white', bins=np.arange(0, df.ws.max(), 5), blowto=False)
    ax.set_yticks(np.arange(5, 30, step=5))
    ax.set_legend(title='Nós', fontsize=20)
    ax.set_title('Vento', fontsize=20)
    # ax.set_radii_angle(fontsize=radsize)
    # ax.set_xticklabels(ax.theta_labels, fontsize=xsize)
    ax.set_radii_angle(fontsize='x-large')
    ax.set_xticklabels(ax.theta_labels, fontsize='x-large')
    ax.set_yticklabels(['{} %'.format(x) for x in np.arange(5, 30, step=5)], fontsize='x-large')
    plt.savefig('vento.png', transparent=False)
    # plt.savefig('vento.png', dpi=None, facecolor='w', edgecolor='w', orientation='portrait', format='png', transparent=True, pad_inches=0.1, bbox_inches='tight')

    fig = plt.figure(figsize=(1, 1), dpi=None, frameon=False)
    rect = [0.1, 0.1, 0.6, 0.8]
    ax = WindroseAxes(fig, rect).from_ax()
    ax.bar(df.cd1, df.cs1, normed=True, opening=0.8, edgecolor='white', bins=np.arange(0, 2.5, .5), blowto=False)
    ax.set_yticks(np.arange(5, 30, step=5))
    ax.set_legend(title='Nós',fontsize=20)
    ax.set_title('Corrente', fontsize=20)
    # ax.set_radii_angle(fontsize=radsize)
    # ax.set_xticklabels(ax.theta_labels, fontsize=xsize)
    ax.set_radii_angle(fontsize='x-large')
    ax.set_xticklabels(ax.theta_labels, fontsize='x-large')
    ax.set_yticklabels(['{} %'.format(x) for x in np.arange(5, 30, step=5)], fontsize='x-large')
    plt.savefig('corrente.png', transparent=False)

    # ax = WindroseAxes.from_ax()
    # ax.bar(df.cd1, df.cs1, normed=True, opening=0.8, edgecolor='white', bins=np.arange(0, 150, 25), blowto=False)
    # ax.set_yticks(np.arange(5, 30, step=5))
    # ax.set_yticklabels(np.arange(5, 30, step=5))
    # ax.set_legend()
    # ax.set_title('Corrente')

    # # plt.savefig('corrente.png', dpi=None, facecolor='w', edgecolor='w', orientation='portrait', format='png', transparent=True, pad_inches=0.1, bbox_inches='tight')
    # plt.savefig('corrente.png', transparent=True)

    plt.show()
# ax1, fig1 = waverose(inte=rig.hm0, dire=rig.dp, figsz=(8.5, 6),
#                      nsector=16, radsize=20, xsize='x-large', leg='off', bbx=-10.8)

