import numpy as np
import tkinter as tk
import tkinter.messagebox as messagebox
import matplotlib as mpl
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
#from multiprocessing import Process
import time
#neurons, trajectories, basedir = IBO_main.loadthedata()
neurons=list(range(1,10));

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
        self.cellgroup_label_1 = tk.Label(master, text = 'Group 1 - ???', state = 'disabled')
        self.cellgroup_label_1.grid(row=5, column=0,columnspan=8)
        self.cellgroup_label_2 = tk.Label(master, text = 'Group 2 - ???', state = 'disabled')
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
                celltypes.append(neurons[int(num)-1].data[neurons[int(num)-1].runnum]['celltype'])
            if celltypes.count(celltypes[0]) == len(celltypes) and celltypes[0] != 'bulk':
                if celltypes[0] == 'speed':
                    if self.answer_cellgroups[0] == True:
                        messagebox.showinfo("Hey!", "You have found the speed modulated neurons... again.. look for something else!")
                    else:
                        self.answer_cellgroups[0] = True
                        self.cellgroup_label_1.config(text = 'Group 1 - speed modulated cells' )
                        messagebox.showinfo("Congratulations!", "You have found the speed modulated neurons!")
                elif celltypes[0] == 'HD':
                    if self.answer_cellgroups[1] == True:
                        messagebox.showinfo("Hey!", "You have found the head direction cells... again.. look for something else!")
                    else:
                        self.answer_cellgroups[1] = True
                        self.cellgroup_label_1.config(text = 'Group 2 - head direction cells' )
                        messagebox.showinfo("Congratulations!", "You have found the head direction cells!")
                elif celltypes[0] == 'border':
                    if self.answer_cellgroups[2] == True:
                        messagebox.showinfo("Hey!", "You have found the border cells... again.. look for something else!")
                    else:
                        self.answer_cellgroups[2] = True
                        self.cellgroup_label_1.config(text = 'Group 3 - border cells' )
                        messagebox.showinfo("Congratulations!", "You have found the border cells!")
                elif celltypes[0] == 'grid':
                    if self.answer_cellgroups[3] == True:
                        messagebox.showinfo("Hey!", "You have found the grid cells... again.. look for something else!")
                    else:
                        self.answer_cellgroups[3] = True
                        self.cellgroup_label_1.config(text = 'Group 4 - grid cells' )
                        messagebox.showinfo("Congratulations!", "You have found the grid cells!")
            self.unusedanswers.set(self.unusedanswers.get()-1)
            self.update_answer_counter()
            if self.unusedanswers.get()<1 or self.answer_cellgroups.count(True) == 4:
                self.disable_exp1()
            self.updatelog()
                    
    def startexperiment(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = IBO_touchtherat_GUI(self.newWindow,self.neurons)
    
    def update_answer_counter(self):
        self.unusedanswercounter.config(text = 'You have\n' + str(self.unusedanswers.get()) + '\ntries left.')

class IBO_touchtherat_GUI():
    def __init__(self, master,neurons):
        self.neurons=neurons
        dpi=60
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
        self.exp1_handles['replayinterval_base'] = 0.05
        self.exp1_handles['steptime'] = [np.nan, np.nan, np.nan, np.nan, np.nan]
        
        
        self.exp1_handles['replayspeed_str'] = tk.StringVar()
        self.exp1_handles['replayspeed_str'].set(str(self.exp1_handles['replayspeed'])+'X')
        
        tk.Label(self.exp1_handles['window'],text = 'Neuron:').grid(row=0, column=0,sticky='E')
        self.exp1_handles['cellselector'] = tk.OptionMenu(self.exp1_handles['window'], self.exp1_handles['cellnum'], *list(range(1, len(self.neurons)+1)), command=self.stimulate ) 
        self.exp1_handles['cellselector'].grid(row=0, column=1, sticky='W')
        
        self.exp1_handles['TimeScale'] = tk.Scale(self.exp1_handles['window'], orient = 'horizontal', length = 1000, variable = self.exp1_handles['timenow'], from_ = 0, to = 1000, command = self.stimulate_once)
        #self.exp1_handles['TimeScale'].pack()
        self.exp1_handles['TimeScale'].grid(row=8,column=1, sticky='W',columnspan = 5)
        tk.Label(self.exp1_handles['window'],text = 'Stimulus number').grid(row=9,column=1,columnspan = 5)
        
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
        self.exp1_handles['trace_fig'] = mpl.figure.Figure(figsize=figsize_trace,dpi=dpi)
        self.exp1_handles['trace_ax'] = self.exp1_handles['trace_fig'].add_axes(rect_trace)
        self.exp1_handles['trace_ax'].set_xlim(-50,150)
        self.exp1_handles['trace_ax'].set_ylim(-100,100)
        self.exp1_handles['trace_ax'].set_xlabel('Time relative to touch (ms)')
        self.exp1_handles['trace_ax'].set_ylabel('Voltage (\microV)')
        self.exp1_handles['trace_fig_photo'] = self.draw_figure(self.exp1_handles['trace_canvas'], self.exp1_handles['trace_fig'], loc=(0, 0))
        
        self.exp1_handles['dots_canvas'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['dots_w'], height=self.exp1_handles['dots_h'])
        self.exp1_handles['dots_canvas'].grid(row=3, column=1,columnspan=5,rowspan=1)
        self.exp1_handles['dots_fig'] = mpl.figure.Figure(figsize=figsize_dots,dpi=dpi)
        self.exp1_handles['dots_ax'] = self.exp1_handles['dots_fig'].add_axes(rect_dots)
        self.exp1_handles['dots_ax'].set_xlim(-50,150)
        self.exp1_handles['dots_ax'].set_ylim(0,1000)
        self.exp1_handles['dots_ax'].set_xlabel('Time relative to touch (ms)')
        self.exp1_handles['dots_ax'].set_ylabel('Trial number')
        self.exp1_handles['dots_fig_photo'] = self.draw_figure(self.exp1_handles['dots_canvas'], self.exp1_handles['dots_fig'], loc=(0, 0))
        
        self.exp1_handles['hist_canvas'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['hist_w'], height=self.exp1_handles['hist_h'])
        self.exp1_handles['hist_canvas'].grid(row=4, column=1,columnspan=5,rowspan=1)
        self.exp1_handles['hist_fig'] = mpl.figure.Figure(figsize=figsize_hist,dpi=dpi)
        self.exp1_handles['hist_ax'] = self.exp1_handles['hist_fig'].add_axes(rect_hist)
        self.exp1_handles['hist_ax'].set_xlim(-50,150)
        self.exp1_handles['hist_ax'].set_ylim(0,100)
        self.exp1_handles['hist_ax'].set_xlabel('Time relative to touch (ms)')
        self.exp1_handles['hist_ax'].set_ylabel('AP number')
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
    def stimulate_once(self,value=0):
        currenttime=0
        self.stimulate(currenttime)
    
    def stimulate(self,settime=-1):
        print('stimulus')
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
