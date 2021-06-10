

%clear 
%close all
%clc

samplingrate = 100;

fftlength = 10000;

%sig = csvread('grafana.csv',1,1);
%sig = readmatrix('new.csv');
%disp(class(sig));
%disp(sig(1,3));
%plot(sig)

%[a,b,c]=xlsread('grafana(new).csv')

%d= c((2,1):(2,1000))
%num=[];
%num2=[];
i=1;
%d=cell2mat(c(1,3));
%disp(d);
%disp(length(c));
%disp(size('NaN'));
%while i<=187353
  %num = [num, c(i,3)];
 % num2 = [num2, c(i,2)];
  %disp(num);
  %i=i+1;
%end

d=string(num2);
%disp(length(num));
%f=char(num);
%e=cell2mat(num);
%disp("Hi");
%disp(e);
%disp(c(2,2));
%disp(c(2,3));
%disp(c(2,4));
%sig = sig(2000:5000);
%c(3)
%sig_bp = bandpass(sig-mean(sig),[0.7 8],samplingrate);
del= ["T","-04:00"]
newStr = erase(d,del)
%plot(sig_bp);
%disp(newStr)
%writematrix(sig_bp,'M.csv')
%writematrix(d,'test3.csv');
%dlmwrite('test3.csv',e,'delimiter',',','-append');
%writematrix(e,'test1.csv');
%disp("Done");
%csvwrite('test21.csv',e(:))
%disp(e);
writematrix(newStr(:),'test.csv');
%writematrix(e(:),'data.csv')
%dlmwrite('test223.csv',e(:),'delimiter',',','-append');
%sig1 = readmatrix('test11.csv');
%sig2 = fopen('test10.csv','rt');
%disp(sig1);
%disp(length(sig2));
