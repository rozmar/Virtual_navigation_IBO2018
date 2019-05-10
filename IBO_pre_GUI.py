import numpy as np
import tkinter as tk
import tkinter.messagebox as messagebox
#import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
import IBO_pre

neurons = IBO_pre.loadthedata()

#%%
class IBO_pre_mainwindow:
    def __init__(self,master,neurons):
        self.master=master
        self.neurons=neurons
        self.ID = tk.StringVar()
        self.answer_cellgroups = [False, False]
        self.answer_1 = tk.StringVar()
        self.answer_2 = tk.StringVar()
        self.answer_3 = tk.StringVar()
        
        self.exp1_startbutton = tk.Button(master, text = 'Start \nexperiment!',command = self.startexperiment)
        self.exp1_startbutton.grid(row=1,column=0)
        answerentrywidth=2
        vcmd = (master.register(self.validate_answer))
        self.answer_1_entry = tk.Entry(master,textvariable = self.answer_1, width = answerentrywidth, validate='all', validatecommand=(vcmd, '%P'))
        self.answer_1_entry.grid(row=1, column=1)
        self.answer_2_entry = tk.Entry(master,textvariable = self.answer_2, width = answerentrywidth, validate='all', validatecommand=(vcmd, '%P'))
        self.answer_2_entry.grid(row=1, column=2)
        self.answer_3_entry = tk.Entry(master,textvariable = self.answer_3, width = answerentrywidth, validate='all', validatecommand=(vcmd, '%P'))
        self.answer_3_entry.grid(row=1, column=3)
        self.answer_submit = tk.Button(master, text = 'Submit \nanswer!', command = self.submit_answer)
        self.answer_submit.grid(row=1, column=7)
        self.unusedanswers=tk.IntVar()
        self.unusedanswers.set(10)
        self.unusedanswercounter = tk.Label(master, text = '')
        self.unusedanswercounter.grid(row=4, column=1,columnspan=3)
        self.update_answer_counter()
        self.cellgroup_label_1 = tk.Label(master, text = 'Group 1 - ???')
        self.cellgroup_label_1.grid(row=5, column=0,columnspan=8)
        self.cellgroup_label_2 = tk.Label(master, text = 'Group 2 - ???')
        self.cellgroup_label_2.grid(row=6, column=0,columnspan=8)
        
    def validate_answer(self, P):
        if (str.isdigit(P) and float(P)<=len(self.neurons) and float(P)>0) or P == "":
            return True
        else:
            return False

    def submit_answer(self):
        cellnums=list()
        cellnums.append(self.answer_1.get())
        cellnums.append(self.answer_2.get())
        cellnums.append(self.answer_3.get())
        if cellnums[0].isdigit and cellnums[1].isdigit and cellnums[2].isdigit and cellnums.count(cellnums[0])==1 and cellnums.count(cellnums[1]) == 1 and cellnums.count(cellnums[2]) == 1:
            celltypes = list()
            for num in cellnums:
                celltypes.append(neurons[int(num)-1]['celltype'])
            print(celltypes)
            if celltypes.count(celltypes[0]) == len(celltypes) and celltypes[0] != 'bulk':
                if celltypes[0] == 'excited':
                    if self.answer_cellgroups[0] == True:
                        messagebox.showinfo("Hey!", "You have found the excited neurons... again.. look for something else!")
                    else:
                        self.answer_cellgroups[0] = True
                        self.cellgroup_label_1.config(text = 'Group 1 - excited neurons' )
                        messagebox.showinfo("Congratulations!", "You have found the excited neurons!")
                elif celltypes[0] == 'inhibited':
                    if self.answer_cellgroups[1] == True:
                        messagebox.showinfo("Hey!", "You have found the inhibited cells... again.. look for something else!")
                    else:
                        self.answer_cellgroups[1] = True
                        self.cellgroup_label_2.config(text = 'Group 2 - inhibited neurons' )
                        messagebox.showinfo("Congratulations!", "You have found the inhibited cells!")
            self.unusedanswers.set(self.unusedanswers.get()-1)
            self.update_answer_counter()
            
                    
    def startexperiment(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = IBO_touchtherat_GUI(self.newWindow,self.neurons)
    
    def update_answer_counter(self):
        self.unusedanswercounter.config(text = 'You have\n' + str(self.unusedanswers.get()) + '\ntries left.')

class IBO_touchtherat_GUI():
    def __init__(self, master,neurons):
        self.neurons=neurons
        dpi=60
        self.sweepend = 100
        self.sweepstart = -50
        self.exp1_handles=dict()
        self.exp1_handles['trace_w']=1000
        self.exp1_handles['trace_h']=120
        figsize_trace=(17, 2)
        rect_trace=[.07,.22,.9,.75]
        
        self.exp1_handles['dots_w']=self.exp1_handles['trace_w']
        self.exp1_handles['dots_h']=300
        figsize_dots=(17,5)
        rect_dots=[.07,.2,.9,.75]
        
        self.exp1_handles['hist_w']=self.exp1_handles['trace_w']
        self.exp1_handles['hist_h']=self.exp1_handles['trace_h']
        figsize_hist=figsize_trace
        rect_hist=rect_trace
        
        
        self.exp1_handles['window'] = master
        self.exp1_handles['window'].title("Experiment 1")
        
        self.exp1_handles['timenow'] = tk.DoubleVar()
        self.exp1_handles['timenow'].set(0)
        
        self.exp1_handles['cellnum'] = tk.IntVar()
        self.exp1_handles['cellnum'].set(1)

        self.exp1_handles['replayspeed'] = 1 
        self.exp1_handles['replayinterval_base'] = 1
        self.exp1_handles['steptime'] = [np.nan, np.nan, np.nan, np.nan, np.nan]
        
        
        self.exp1_handles['replayspeed_str'] = tk.StringVar()
        self.exp1_handles['replayspeed_str'].set(str(self.exp1_handles['replayspeed'])+'X')
        
        tk.Label(self.exp1_handles['window'],text = 'Neuron:').grid(row=0, column=0,sticky='E')
        self.exp1_handles['cellselector'] = tk.OptionMenu(self.exp1_handles['window'], self.exp1_handles['cellnum'], *list(range(1, len(self.neurons)+1)), command=self.stimulate_once ) 
        self.exp1_handles['cellselector'].grid(row=0, column=1, sticky='W')
        
        self.exp1_handles['TimeScale'] = tk.Scale(self.exp1_handles['window'], orient = 'horizontal', length = 1000, variable = self.exp1_handles['timenow'], from_ = 1, to = 1000, command = self.stimulate_once)
        #self.exp1_handles['TimeScale'].pack()
        self.exp1_handles['TimeScale'].grid(row=8,column=1, sticky='W',columnspan = 5)
        tk.Label(self.exp1_handles['window'],text = 'Trial number').grid(row=9,column=1,columnspan = 5)
        
        self.exp1_handles['PlayButton'] = tk.Button(self.exp1_handles['window'], text ="Play", command = self.start_stop_stimulation )
        #self.exp1_handles['PlayButton'].pack()
        self.exp1_handles['PlayButton'].grid(row=7,column=1, sticky='W')
        
        self.exp1_handles['SlowDownButton'] = tk.Button(self.exp1_handles['window'], text ="Slow down", command = self.slowdowntherun )
        #self.exp1_handles['PlayButton'].pack()
        self.exp1_handles['SlowDownButton'].grid(row=7,column=2, sticky='W')
        
        self.exp1_handles['SpeedUpButton'] = tk.Button(self.exp1_handles['window'], text ="Speed up", command = self.speeduptherun )
        #self.exp1_handles['PlayButton'].pack()
        self.exp1_handles['SpeedUpButton'].grid(row=7,column=3, sticky='W')
        
        tk.Label(self.exp1_handles['window'],text = 'Replay speed:').grid(row=7, column=4, sticky='E')
        tk.Label(self.exp1_handles['window'],textvariable = self.exp1_handles['replayspeed_str']).grid(row=7, column=5, sticky='W')
        
        self.exp1_handles['trace_canvas'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['trace_w'], height=self.exp1_handles['trace_h'])
        self.exp1_handles['trace_canvas'].grid(row=2, column=1,columnspan=5,rowspan=1)
        self.exp1_handles['trace_fig'] = plt.Figure(figsize=figsize_trace,dpi=dpi)
        self.exp1_handles['trace_ax'] = self.exp1_handles['trace_fig'].add_axes(rect_trace)
        self.exp1_handles['trace_ax'].set_xlim(self.sweepstart,self.sweepend)
        self.exp1_handles['trace_ax'].set_ylim(-1,5)
        self.exp1_handles['trace_ax'].set_xlabel('Time relative to touch (ms)')
        self.exp1_handles['trace_ax'].set_ylabel('Voltage (mV)')
        self.exp1_handles['trace_line'] =self.exp1_handles['trace_ax'].plot(0, 0,linewidth=3,zorder = 1)
        self.exp1_handles['trace_arrow'] = self.exp1_handles['trace_ax'].arrow(0,5,0,-1,width=1)
        self.exp1_handles['trace_fig_photo'] = self.draw_figure(self.exp1_handles['trace_canvas'], self.exp1_handles['trace_fig'], loc=(0, 0))
        
        self.exp1_handles['dots_canvas'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['dots_w'], height=self.exp1_handles['dots_h'])
        self.exp1_handles['dots_canvas'].grid(row=3, column=1,columnspan=5,rowspan=1)
        self.exp1_handles['dots_fig'] = plt.Figure(figsize=figsize_dots,dpi=dpi)
        self.exp1_handles['dots_ax'] = self.exp1_handles['dots_fig'].add_axes(rect_dots)
        self.exp1_handles['dots_ax'].set_xlim(self.sweepstart,self.sweepend)
        self.exp1_handles['dots_ax'].set_ylim(0,1000)
        self.exp1_handles['dots_ax'].set_xlabel('Time relative to touch (ms)')
        self.exp1_handles['dots_ax'].set_ylabel('Trial number')
        self.exp1_handles['dots_plot'] = self.exp1_handles['dots_ax'].scatter(-100,-50,edgecolors='k',facecolor='r',linewidths=1,s=100,zorder = 3)
        self.exp1_handles['dots_fig_photo'] = self.draw_figure(self.exp1_handles['dots_canvas'], self.exp1_handles['dots_fig'], loc=(0, 0))
        
        self.exp1_handles['hist_canvas'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['hist_w'], height=self.exp1_handles['hist_h'])
        self.exp1_handles['hist_canvas'].grid(row=4, column=1,columnspan=5,rowspan=1)
        self.exp1_handles['hist_fig'] = plt.Figure(figsize=figsize_hist,dpi=dpi)
        self.exp1_handles['hist_ax'] = self.exp1_handles['hist_fig'].add_axes(rect_hist)
        self.exp1_handles['hist_ax'].set_xlim(self.sweepstart,self.sweepend)
        self.exp1_handles['hist_ax'].set_ylim(0,100)
        self.exp1_handles['hist_ax'].set_xlabel('Time relative to touch (ms)')
        self.exp1_handles['hist_ax'].set_ylabel('AP number')
        self.exp1_handles['hist_plot'] =self.exp1_handles['hist_ax'].bar(0, 0)
        self.exp1_handles['hist_fig_photo'] = self.draw_figure(self.exp1_handles['hist_canvas'], self.exp1_handles['hist_fig'], loc=(0, 0))
        
    def draw_figure(self, canvas, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas
    
        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
        # Position: convert from top-left anchor to center anchor
        canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
    
        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        #    print('plottolok')
        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo    
    def update_plots(self):
        cellnum = self.exp1_handles['cellnum'].get() - 1
        sweepnum = self.exp1_handles['timenow'].get()
        si = self.neurons[cellnum]['si']

        sweepidxes = [i for i, x in enumerate(self.neurons[cellnum]['APsweep']) if x == sweepnum]
        if len(sweepidxes) > 0:
            apidxes = [int((self.neurons[cellnum]['APtime'][i] - self.sweepstart/1000)/si) for i in sweepidxes]
        else:
            apidxes=list()
        
        sweeplength= (self.sweepend - self.sweepstart) / si / 1000
        sweeptime = np.linspace(self.sweepstart,self.sweepend,sweeplength)
        y = sweeptime * 0
        for i in apidxes: y[i-1]=1
        y=np.convolve(y,self.neurons[cellnum]['APwaveform'],mode='same')
        y += np.random.normal(0,.1,len(y))
        self.exp1_handles['trace_line'][0].set_data(sweeptime,y)
        #self.exp1_handles['trace_ax'].set_ylim(min(self.neurons[cellnum]['APwaveform'])*2,max(self.neurons[cellnum]['APwaveform'])*2)
        self.exp1_handles['trace_fig_photo'] = self.draw_figure(self.exp1_handles['trace_canvas'], self.exp1_handles['trace_fig'], loc=(0, 0))
        
        self.exp1_handles['dots_plot'].set_offsets(np.c_[[i * 1000 for i in self.neurons[cellnum]['APtime']],self.neurons[cellnum]['APsweep']])
        self.exp1_handles['dots_ax'].set_ylim(0.5,sweepnum+.5)
        self.exp1_handles['dots_fig_photo'] = self.draw_figure(self.exp1_handles['dots_canvas'], self.exp1_handles['dots_fig'], loc=(0, 0))
        
        idxes = [i for i, x in enumerate(self.neurons[cellnum]['APsweep']) if x <= sweepnum]
        aptimes = [self.neurons[cellnum]['APtime'][x]*1000 for i,x in enumerate(idxes)]
        if len(aptimes)>0:
            hist_vals,bin_edges = np.histogram(aptimes,bins=20)
            bin_centers= (bin_edges[:-1] + bin_edges[1:]) / 2
            binwidth = (bin_edges[2] - bin_edges[1])
        else:
            hist_vals=0
            bin_centers=0
            binwidth=0
        #freq_hist_vals=hist_vals[:]
        #for i,val in enumerate(apidxes): freq_hist_vals[i]=val / (binwidth * sweepnum)
        self.exp1_handles['hist_plot'].remove()
        self.exp1_handles['hist_plot'] =self.exp1_handles['hist_ax'].bar(bin_centers,hist_vals,binwidth*.9,color='blue')
        self.exp1_handles['hist_ax'].set_ylim(0,max(hist_vals))
        self.exp1_handles['hist_fig_photo'] = self.draw_figure(self.exp1_handles['hist_canvas'], self.exp1_handles['hist_fig'], loc=(0, 0))
    def stimulate_once(self,value=0):
        self.stimulate(self.exp1_handles['timenow'].get())
    
    def stimulate(self,settime=-1):
        if settime==-1:
            timenow = self.exp1_handles['timenow'].get()
            self.exp1_handles['timenow'].set(timenow + 1)
        else:
            self.exp1_handles['timenow'].set(settime)
        self.update_plots()
        
        if self.exp1_handles['PlayButton']['text'] == 'Pause' and settime==-1:
            if self.exp1_handles['replayinterval_base']<.030:
                delay = 30
            else:
                delay = 1
                
            delay = int(1000/self.exp1_handles['replayspeed'])
            self.exp1_handles['window'].after(delay, self.stimulate)
        # ez az ami plottol és újraindítja magát . runningrat
    
    def start_stop_stimulation(self):
        if self.exp1_handles['PlayButton']['text'] == 'Play':
            self.exp1_handles['PlayButton']['text'] = 'Pause' 
            self.exp1_handles['steptime'] = [np.nan, np.nan, np.nan, np.nan, np.nan]
            self.stimulate()
        else:
            self.exp1_handles['PlayButton']['text'] = 'Play'    
    def speeduptherun(self):
        if self.exp1_handles['replayspeed'] < 32:
            self.exp1_handles['replayspeed'] *= 2
            self.exp1_handles['replayspeed_str'].set(str(self.exp1_handles['replayspeed'])+'X')
            
    def slowdowntherun(self):
        if self.exp1_handles['replayspeed'] > .5:
            self.exp1_handles['replayspeed'] /= 2
            self.exp1_handles['replayspeed_str'].set(str(self.exp1_handles['replayspeed'])+'X')
root = tk.Tk()
root.title('Virtual touch sensation')
app = IBO_pre_mainwindow(root,neurons,)
root.mainloop()
