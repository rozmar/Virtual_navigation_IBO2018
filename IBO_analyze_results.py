from tkinter import filedialog
import tkinter as tk
import os
import json
import matplotlib as mpl
import numpy as np

class Competitor():
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name
        with open(self.directory+'/'+self.name+'.json', 'r') as f_obj: self.data = json.load(f_obj)
    def unusedanswers(self):
        return self.data['unusedanswers']
    def answer_1_correct(self):
        return self.data['answer_cellgroups'][0]
    def answer_2_correct(self):
        return self.data['answer_cellgroups'][1]
    def answer_3_correct(self):
        return self.data['answer_cellgroups'][2]
    def answer_4_correct(self):
        return self.data['answer_cellgroups'][3]
    def isfinalized(self):
        return self.data['exp1_disabled']
    def answers(self):
        return self.data['answer_cellgroups']
    def point(self):
        pointpercelltype = 8
        basepoint = self.data['answer_cellgroups'].count(True) * pointpercelltype
        
        multipliertable = dict()
        multipliertable[0] = .7
        multipliertable[1] = .75
        multipliertable[2] = .8
        multipliertable[3] = .85
        multipliertable[4] = .9
        multipliertable[5] = .95
        multipliertable[6] = 1
        multipliertable[7] = 1
        multipliertable[8] = 1
        multipliertable[9] = 1
        multipliertable[10] = 1
        multiplier = multipliertable[self.data['unusedanswers']]
        
        point = basepoint * multiplier
        return point
    
root=tk.Tk()
dirname = filedialog.askdirectory(initialdir='/home/rozmar/Data/TAR/ANALYSISdata/marci/IBO_prac_placecell/Logs_SZTE_2018/',title = "Select the directory where the log files are located.",)
root.destroy()
#%%
filenames=os.listdir(dirname)
extensions=list()
names=list()
for filename in filenames:
    dotidx = filename.rfind('.')
    extensions.append(filename[dotidx+1:])
    names.append(filename[:dotidx])
    uniquenames=sorted(list(set(names)))
competitors=list()
for i,name in enumerate(uniquenames):
    competitors.append(Competitor(dirname,name))

points =list ()

for competitor in competitors:
    points.append(competitor.point())

percentiles = np.array(np.linspace(0,100,101))
perc = np.percentile(points, percentiles)
mpl.pyplot.plot(perc,percentiles)

ponthatar = 10
nevsor = list()
for competitor in competitors:
    if competitor.point() > ponthatar:
        nevsor.append(competitor.name)

for competitor in competitors:
    print(competitor.name  + '  ' + str(competitor.point()))
    
