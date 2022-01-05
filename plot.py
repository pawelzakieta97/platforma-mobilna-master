from matplotlib import pyplot as plt
import csv

values = []
ts = []
with open('output1.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            ts.append(float(row[0]))
            values.append(float(row[1]))
        except:
            pass

ts2 = []
values2 = []

t_min = 1
t_max = 3
t_min += ts[0]
t_max += ts[0]
prev_v = None
impulse_start = None
impulse_lens = []

for t, v in zip(ts, values):
    if v == 1 and prev_v == 0:
        impulse_start = t
    if v == 0 and prev_v == 1 and impulse_start is not None:
        impulse_lens.append(t - impulse_start)
    prev_v = v
    if t_min < t < t_max:
        ts2.append(t)
        values2.append(v)
#plt.plot(ts2, values2)
plt.plot(impulse_lens[1:])
plt.show()