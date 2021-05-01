%Tratamento de dados de onda
%onda_freq / onda_tempo / daat

clear, clc, close all

hv = load('heave.txt');
pt = load('pitch_corr.txt');
rl = load('roll_corr.txt');
wind = load('wind.txt');
siodoc = load('siodoc.txt');

ws = wind(:,1);
wd = wind(:,2);
hm0s = siodoc(:,1);
tps = siodoc(:,8);
dps = siodoc(:,7);

dmag = -22;

%parametros para o calculo do espectro
nfft = 128; %tamanho do segmento para a fft
fs = 1; %frequencia de amostragem

%profundidade
h=200;

[l,c] = size(hv);

dt = 1/fs; %intervalo de amostragem

for zz=1:c
    
    n1 = hv(:,zz);
    n3 = pt(:,zz);
    n2 = rl(:,zz);

    %chama subrotina de processamento de onda no dominio da frequencia (dir,hm0..)
    [f,an,anx,any,a1,b1,diraz,dirm,dp,fp,tp,hm0]=ondaf(n1,n2,n3,nfft,fs,h,dmag);

    %chama subrotina de processamento de onda no dominio do tempo (Tza, Hs..)
    [hs,h10,hmax,thmax,tmed]=ondat(n1,fs,h);

    %salva os parametros de onda em uma matriz
    %      linha = 1   2   3     4    5    6   7 8
    matonda(zz,:)=[hs,h10,hmax,thmax,tmed,hm0,tp,dp]';

    bb(:,zz)=an;

end

%matonda(:,8) = matonda(:,8) - 180;
%ind = find(matonda(:,8) < 0);
%matonda(ind,8) = matonda(ind,8) + 360;

figure
plot(wd,'b*'), hold all
plot(matonda(:,8),'ro')
plot(dps-22,'ko'), hold off
ylim([0,360])

