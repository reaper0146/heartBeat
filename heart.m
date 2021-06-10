samplingrate = 100;

fftlength = 10000;

sig = csvread('data.csv');



%sig = sig(2000:11000);

sig_bp = bandpass(sig-mean(sig),[0.7 8],samplingrate);

disp(sig_bp);
plot(sig_bp)
dlmwrite('test.csv',sig_bp,'delimiter',',','-append');
%writematrix(sig_bp(:),'databpf.csv')

