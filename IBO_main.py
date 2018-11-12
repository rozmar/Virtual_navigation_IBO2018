import os
from scipy.io import loadmat
import numpy as np
import fast_histogram
#import pandas

#class RatTrajectory():
    

class Neuron():
    _runnum = 0 #trajectory index
    _cellnum = 0 #cell index
    _timenow = 0 #in seconds
    _bigdots = 10 #in seconds
    _smalldots = 60 #np.inf #in seconds
    
    def __init__(self, data):
        self.data=data

    @property
    def runnum(self):
        return self.__class__._runnum
    @runnum.setter
    def runnum(self, value):
        self.__class__._runnum = value

    @property
    def cellnum(self):
        return self.__class__._cellnum
    @cellnum.setter
    def cellnum(self, value):
        self.__class__._cellnum = value
     
    @property
    def timenow(self):
        return self.__class__._timenow
    @timenow.setter
    def timenow(self, value):
        self.__class__._timenow = value
    
    @property
    def bigdots(self):
        return self.__class__._bigdots
    @bigdots.setter
    def bigdots(self, value):
        self.__class__._bigdots = value
        
    @property
    def smalldots(self):
        return self.__class__._smalldots
    @smalldots.setter
    def smalldots(self, value):
        self.__class__._smalldots = value
        
    
    def APcoordinates_big(self):
        runnum = self.__class__._runnum
        timenow = self.__class__._timenow
        timeback = self.__class__._bigdots
        APidxes_start = abs(self.data[runnum]['APtimes']-timenow + timeback).argmin()
        APidxes_end = abs(self.data[runnum]['APtimes']-timenow).argmin()
        idxes=range(APidxes_start,APidxes_end)
        x = self.data[runnum]['X'][idxes]
        y = self.data[runnum]['Y'][idxes]
        return x, y
    
    def APcoordinates_small(self):
        runnum = self.__class__._runnum
        timenow = self.__class__._timenow
        timeback = self.__class__._smalldots
        APidxes_start = abs(self.data[runnum]['APtimes']-timenow + timeback).argmin()
        APidxes_end = abs(self.data[runnum]['APtimes']-timenow).argmin()
        idxes=range(APidxes_start,APidxes_end)
        x = self.data[runnum]['X'][idxes]
        y = self.data[runnum]['Y'][idxes]
        return x, y
    
    def APnum_in_X(self,binnum=20):
        runnum = self.__class__._runnum
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data[runnum]['APtimes']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data[runnum]['X'][idxes],binnum,(0,200))
        hist=fast_histogram.histogram1d(self.data[runnum]['X'][idxes],binnum,(0,200))
        bin_centers=np.arange(0,200,200/binnum) + 200/binnum/2
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers
    
    def APnum_in_Y(self,binnum=20):
        runnum = self.__class__._runnum
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data[runnum]['APtimes']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data[runnum]['Y'][idxes],binnum,(0,200))
        hist=fast_histogram.histogram1d(self.data[runnum]['Y'][idxes],binnum,(0,200))
        bin_centers=np.arange(0,200,200/binnum)+ 200/binnum/2
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers
    
    def APnum_in_speed(self,binnum=20):
        runnum = self.__class__._runnum
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data[runnum]['APtimes']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data[runnum]['speed'][idxes],binnum,(0,200))
        hist=fast_histogram.histogram1d(self.data[runnum]['speed'][idxes],binnum,(0,80))
        bin_centers=np.arange(0,80,80/binnum)+ 80/binnum/2
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers
    
    def APnum_in_headdirection(self,binnum=20):
        runnum = self.__class__._runnum
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data[runnum]['APtimes']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data[runnum]['headdir'][idxes],binnum,(0,360))
        hist=fast_histogram.histogram1d(self.data[runnum]['headdir'][idxes],binnum,(0,360))
        bin_centers=np.arange(0,360,360/binnum) + 360/binnum/2
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers

class RatTrajectory():
    _runnum = 0 #trajectory index
    _timenow = 0 #in seconds
    _timeback = 60 #np.inf #in seconds - the length of the line after the animal
    
    def __init__(self, data):
        self.data=data
    
    @property
    def runnum(self):
        return self.__class__._runnum
    @runnum.setter
    def runnum(self, value):
        self.__class__._runnum = value
    
    @property
    def timenow(self):
        return self.__class__._timenow
    @timenow.setter
    def timenow(self, value):
        self.__class__._timenow = value
        
    @property
    def timeback(self):
        return self.__class__._timeback
    @timeback.setter
    def timeback(self, value):
        self.__class__._timeback = value
    
    def trajectory_coordinates(self):
        #runnum = self.__class__._runnum
        timenow = self.__class__._timenow 
        timeback = self.__class__._timeback
        idx_start = abs(self.data['locationtime']-timenow+timeback).argmin()
        idx_end = abs(self.data['locationtime']-timenow).argmin()
        idxes = range(idx_start,idx_end)
        x1 = self.data['location'][idxes,0]
        y1 = self.data['location'][idxes,1]
        x2 = self.data['location'][idxes,2]
        y2 = self.data['location'][idxes,3]
        return x1,y1,x2,y2
    
    def arrow_coordinates(self):
        #runnum = self.__class__._runnum
        timenow = self.__class__._timenow 
        idxes = abs(self.data['locationtime']-timenow).argmin()
        x1 = self.data['location'][idxes,0]
        y1 = self.data['location'][idxes,1]
        x2 = self.data['location'][idxes,2]
        y2 = self.data['location'][idxes,3]
        return x2, y2, x1-x2, y1-y2
    
    def speed_now(self):
        timenow = self.__class__._timenow
        idx = abs(self.data['locationtime']-timenow).argmin()
        return self.data['speed'][idx,0]
    
    def headdirection_now(self):
        timenow = self.__class__._timenow
        idx = abs(self.data['locationtime']-timenow).argmin()
        return self.data['headdirection'][idx]

    
    def time_spent_in_X(self,binnum=20):
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data['locationtime']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data['location'][idxes,0],bins=binnum,range=(0,200))
        
        hist=fast_histogram.histogram1d(self.data['location'][idxes,0],binnum,(0,200))
        bin_centers=np.arange(0,200,200/binnum)+ 200/binnum/2
        
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers
    
    def time_spent_in_Y(self,binnum=20):
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data['locationtime']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data['location'][idxes,1],binnum,(0,200))
        hist=fast_histogram.histogram1d(self.data['location'][idxes,1],binnum,(0,200))
        bin_centers=np.arange(0,200,200/binnum)+ 200/binnum/2
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers
    
    def time_spent_in_speed(self,binnum=20):
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data['locationtime']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data['speed'][idxes],binnum,(0,200))
        hist=fast_histogram.histogram1d(self.data['speed'][idxes,0],binnum,(0,80))
        bin_centers=np.arange(0,80,80/binnum)+ 80/binnum/2
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers
    
    def time_spent_in_headdirection(self,binnum=20):
        timenow = self.__class__._timenow
        idxes = range(0,abs(self.data['locationtime']-timenow).argmin())
#        hist, bin_edges = np.histogram(self.data['headdirection'][idxes],binnum,(0,360))
        hist=fast_histogram.histogram1d(self.data['headdirection'][idxes],binnum,(0,360))
        bin_centers=np.arange(0,360,360/binnum)+ 360/binnum/2
#        bin_centers=np.convolve(bin_edges,[0.5,0.5],mode='valid')
        return hist, bin_centers
    
def extractstruct(olddata): 
    if olddata.dtype.names==None:
        temp=olddata.T
        temp2=list();
        for i in temp:
            while type(i)==np.ndarray and len(i)==1:
                i=i[0]
            if type(i)==np.ndarray:
                i=i/1000
            temp2.append(i)
        newdata=temp2
    else:
        fieldnames=olddata.dtype.names
        print(type(fieldnames))
        #newdata=pandas.DataFrame(columns=fieldnames);
        newdata=dict()
        for fieldname in fieldnames:
            temp=olddata[fieldname].T
            temp2=list();
            for i in temp:
                while type(i)==np.ndarray and len(i)==1:
                    i=i[0]
                if type(i)==np.ndarray:
                    i=i/1000
                    i=np.concatenate(i)
                temp2.append(i)
            newdata[fieldname]=temp2
    return newdata

#%% loading the data
def loadthedata():
    basedir=os.path.dirname(__file__)
    files=os.listdir(basedir+'/Data/')
    data=list()
    for filename in files:
        data.append(loadmat(basedir+'/Data/'+filename))
    
    datanow=data[files.index('experiment1.mat')]
    cells=extractstruct(datanow['cells'])
    rattrajectory=extractstruct(datanow['rattrajectory'])
    newlocation=list()
    for i in rattrajectory['location']:
        newlocation.append(i.reshape(int(i.size/4),4))
    rattrajectory['location']=newlocation
    newspeed=list()
    for i in rattrajectory['speed']:
        newspeed.append(i.reshape(int(i.size/2),2))
    rattrajectory['speed']=newspeed
    
    uniquecells=extractstruct(datanow['uniquecells'])
    
    neurons=list()
    for cellID in uniquecells:
        data=list()
        for idx in range(0,len(cells['cellID'])):
            if cellID==cells['cellID'][idx]:
                datanow=dict()
                for fieldname in cells.keys():
                    datanow[fieldname]=cells[fieldname][idx]
                data.append(datanow)
        neurons.append(Neuron(data))

    trajectories=list()
    for idx in range(0, len(rattrajectory['location'])):
        data=dict()
        for fieldname in rattrajectory.keys():
            data[fieldname]=rattrajectory[fieldname][idx]
        trajectories.append(RatTrajectory(data))
    return neurons, trajectories, basedir


def printneurontypes(neurons):
    for i,neuron in enumerate(neurons):
        celltype = neuron.data[0]['celltype']
        isspeedcell = neuron.data[0]['itsaspeedcell']
        print(str(i) + ' - ' + celltype, ' - is it a speed cell:', isspeedcell)
