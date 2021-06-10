import matplotlib.pyplot as plt
import csv
import heartpy as hp

x=[]
y=[]

with open('grafana.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    #print(plots)
    for row in plots:
        x.append(str(row[1]))
        y.append(int(row[2]))

#print (x)
plt.plot(x,y)

plt.title('Data from the CSV File')

plt.xlabel('Amp')
plt.ylabel('Time')

plt.show()

