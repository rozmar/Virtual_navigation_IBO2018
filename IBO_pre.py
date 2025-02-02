import os
from scipy.io import loadmat
import numpy as np
import random

def loadthedata():
    basedir=os.path.dirname(__file__)
    files=os.listdir(basedir+'/Data/')
    data=list()
    for filename in files:
        data.append(loadmat(basedir+'/Data/'+filename))
    APwaves = data[files.index('APwaveforms.mat')]['APwaves']
    si = data[files.index('APwaveforms.mat')]['si'][0][0]
    
    timestart = -.05
    timeend = .1
    sweeplength = timeend - timestart
    sweepnum  = 1000
    binsize = .002
    binnum = round((sweeplength)/binsize)
    totaltime = sweepnum * sweeplength
    totalbintime = binsize * sweepnum
    basefiringrate_mu = 20
    basefiringrate_sigma = 5
    excitedcellnum = 5
    excitedcell_delay_mu = .030
    excitedcell_delay_sigma = .001
    excitedcell_firingratechange_distrtibution_sigma = .004 
    excitedcell_firingratechange_mu = 40
    excitedcell_firingratechange_sigma = 5
    inhibitedcellnum = 5
    inhibitedcell_delay_mu = .035
    inhibitedcell_delay_sigma = .01
    inhibitedcell_firingratechange_distrtibution_sigma = .005
    inhibitedcell_firingratechange_mu = 20
    inhibitedcell_firingratechange_sigma = 5
    bulkcellnum = 5
    APtime_maxrandvalue = .0005 # to randomize the timing of the APs
    
    celltypes=list()
    for celli in range(0,excitedcellnum):
        celltypes.append('excited')
    for celli in range(0,inhibitedcellnum):
        celltypes.append('inhibited')
    for celli in range(0,bulkcellnum):
        celltypes.append('bulk')
    np.random.shuffle(celltypes)
    cells = list()
    for celltype in celltypes:
        data=dict()
        data['celltype'] = celltype
        data['APwaveform'] = APwaves[:,round(np.random.uniform()*(APwaves.shape[1]-1))]
        data['si'] = si
        basefiringrate = np.random.normal(basefiringrate_mu,basefiringrate_sigma)
        baseAPineachbin=round(basefiringrate*totalbintime)
        if celltype == 'excited':
            firingratechange = np.random.normal(excitedcell_firingratechange_mu,excitedcell_firingratechange_sigma)
            apnumchange = round(firingratechange * excitedcell_firingratechange_distrtibution_sigma * sweepnum * 3)
            realdelay = np.random.normal(excitedcell_delay_mu,excitedcell_delay_sigma) 
            aptimes = np.random.normal(realdelay,excitedcell_firingratechange_distrtibution_sigma,apnumchange) 
            aphist, binedges =np.histogram(aptimes,binnum,(timestart,timeend))
        elif celltype == 'inhibited':
            firingratechange = np.random.normal(inhibitedcell_firingratechange_mu,inhibitedcell_firingratechange_sigma)
            apnumchange = round(firingratechange * inhibitedcell_firingratechange_distrtibution_sigma * sweepnum * 3)
            realdelay = np.random.normal(inhibitedcell_delay_mu,inhibitedcell_delay_sigma) 
            aptimes = np.random.normal(realdelay,inhibitedcell_firingratechange_distrtibution_sigma,apnumchange) 
            aphist , binedges =np.histogram(aptimes,binnum,(timestart,timeend))
            aphist =aphist*-1
        else:
            aptimes=[];
            aphist,binedges=np.histogram(aptimes,binnum,(timestart,timeend))
        aphist += baseAPineachbin
        aphist[aphist<0]=0
        aptime = list()
        apsweep = list()
        idx = -1
        
        for timenow in np.linspace(timestart,timeend,binnum):
            idx += 1
#            sweepnums = np.random.uniform(1,sweepnum,aphist[idx]).round()
            sweepnums= random.sample(range(1,sweepnum),aphist[idx])
            times = np.ones(aphist[idx]) * timenow
            apsweep.extend(sweepnums)
            aptime.extend(times)
        aptime += np.random.uniform(-APtime_maxrandvalue, APtime_maxrandvalue, len(aptime))
        randtime_sweep = np.random.uniform(-APtime_maxrandvalue*2, APtime_maxrandvalue*2,sweepnum)
        for i, sw in enumerate(apsweep): 
            aptime[i] += randtime_sweep[int(sw-1)]
        realaptime=list()
        realapsweep=list()
        for i, aptime_now in enumerate(aptime):
            if aptime_now <= timeend and aptime_now >=timestart:
                realaptime.append(aptime_now)
                realapsweep.append(apsweep[i])

        data['APsweep'] = realapsweep
        data['APtime'] = realaptime
        cells.append(data)
    return cells

