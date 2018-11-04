import os
import json
import IBO_main
import numpy as np
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import simpledialog
import matplotlib as mpl
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
#from multiprocessing import Process
import time
neurons, trajectories, basedir = IBO_main.loadthedata()


#%%
class IBO_mainwindow:
    def __init__(self,master,neurons,trajectories,basedir):
        self.master=master
        self.neurons=neurons
        self.trajectories=trajectories
        self.basedir=basedir
        self.logdir=basedir + '/Logs/'
        self.ID = tk.StringVar()
        self.answer_cellgroups = [False, False, False, False]
        self.answer_1 = tk.StringVar()
        self.answer_2 = tk.StringVar()
        self.answer_3 = tk.StringVar()
        self.IDlabel = tk.Label(master,text = 'ID:')
        self.IDlabel.grid(row=0, column=0,sticky = 'E')
        self.IDentry = tk.Entry(master,textvariable = self.ID,width = 10)
        self.IDentry.grid(row=0, column=1,columnspan=3)
        self.IDsubmit = tk.Button(master,text = 'Submit \nname!',command=self.checkID)
        self.IDsubmit.grid(row=0,column=7)
        
        self.exp1_startbutton = tk.Button(master, text = 'Start \nexperiment!',command = self.startexperiment, state='disabled')
        self.exp1_startbutton.grid(row=1,column=0)
        answerentrywidth=2
        vcmd = (master.register(self.validate_answer))
        self.answer_1_entry = tk.Entry(master,textvariable = self.answer_1, width = answerentrywidth, state='disabled', validate='all', validatecommand=(vcmd, '%P'))
        self.answer_1_entry.grid(row=1, column=1)
        self.answer_2_entry = tk.Entry(master,textvariable = self.answer_2, width = answerentrywidth, state='disabled', validate='all', validatecommand=(vcmd, '%P'))
        self.answer_2_entry.grid(row=1, column=2)
        self.answer_3_entry = tk.Entry(master,textvariable = self.answer_3, width = answerentrywidth, state='disabled', validate='all', validatecommand=(vcmd, '%P'))
        self.answer_3_entry.grid(row=1, column=3)
        self.answer_submit = tk.Button(master, text = 'Submit \nanswer!', command = self.submit_answer, state = 'disabled')
        self.answer_submit.grid(row=1, column=7)
        self.unusedanswers=tk.IntVar()
        self.unusedanswers.set(10)
        self.unusedanswercounter = tk.Label(master, text = '', state = 'disabled')
        self.unusedanswercounter.grid(row=4, column=1,columnspan=3)
        self.update_answer_counter()
        self.cellgroup_label_1 = tk.Label(master, text = 'Group 1 - ???', state = 'disabled')
        self.cellgroup_label_1.grid(row=5, column=0,columnspan=8)
        self.cellgroup_label_2 = tk.Label(master, text = 'Group 2 - ???', state = 'disabled')
        self.cellgroup_label_2.grid(row=6, column=0,columnspan=8)
        self.cellgroup_label_3 = tk.Label(master, text = 'Group 3 - ???', state = 'disabled')
        self.cellgroup_label_3.grid(row=7, column=0,columnspan=8)
        self.cellgroup_label_4 = tk.Label(master, text = 'Group 4 - ???', state = 'disabled')
        self.cellgroup_label_4.grid(row=8, column=0,columnspan=8)
        self.skip_exp_1_button = tk.Button(master, text = 'Skip this part!',bg = "red", command = self.skip_exp1, state = 'disabled')
        self.skip_exp_1_button.grid(row=9, column=0,columnspan=8)
        self.exp1_startbutton_2 = tk.Button(master, text = 'Start\nexperiment\nagain!',command = self.startexperiment_2, state='disabled')
        self.exp1_startbutton_2.grid(row=10,column=0,columnspan=8)
        self.exp1_disabled = False
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
                    
    def skip_exp1(self):
        answer = messagebox.askyesno('!!WARNING!!','Are you sure? Do you really want to skip this task? You will lose your remaining chances and there is no way back!')
        if answer:
            self.disable_exp1()
    def disable_exp1(self):   
        self.exp1_disabled = True
        self.exp1_startbutton.config(state='disabled')
        self.answer_1_entry.config(state='disabled')
        self.answer_2_entry.config(state='disabled')
        self.answer_3_entry.config(state='disabled')
        self.answer_submit.config(state='disabled')
        self.unusedanswercounter.config(state='disabled')
        self.cellgroup_label_1.config(state='disabled')
        self.cellgroup_label_2.config(state='disabled')
        self.cellgroup_label_3.config(state='disabled')
        self.cellgroup_label_4.config(state='disabled')
        self.skip_exp_1_button.config(state='disabled')
        self.exp1_startbutton_2.config(state='normal')
        self.updatelog()
    def checkID(self):
        
        logfiles=os.listdir(self.logdir)
        ID=self.ID.get().lower()
        isfilepresent = logfiles.count(ID + '.json')
        canproceed = False
        if len(ID)>3:
            if isfilepresent == 1:
                answer = simpledialog.askstring("Password needed to load the data.", "Enter password:")
                if answer == 'mehet':
                    canproceed = True
            else:
                canproceed = True
        if canproceed:
            self.IDentry.config(state='disabled')
            self.IDsubmit.config(state='disabled')
            self.exp1_startbutton.config(state='normal')
            self.answer_1_entry.config(state='normal')
            self.answer_2_entry.config(state='normal')
            self.answer_3_entry.config(state='normal')
            self.answer_submit.config(state='normal')
            self.unusedanswercounter.config(state='normal')
            self.cellgroup_label_1.config(state='normal')
            self.cellgroup_label_2.config(state='normal')
            self.cellgroup_label_3.config(state='normal')
            self.cellgroup_label_4.config(state='normal')
            self.skip_exp_1_button.config(state='normal')
            if isfilepresent == 1: # loading the data and updating the GUI
                with open(self.logdir + ID + '.json', 'r') as f_obj: storeddata = json.load(f_obj)
                self.unusedanswers.set(storeddata['unusedanswers'])
                self.ID.set(storeddata['ID'])
                self.answer_cellgroups = storeddata['answer_cellgroups']
                self.exp1_disabled = storeddata['exp1_disabled']
                if self.answer_cellgroups[0] == True:
                    self.cellgroup_label_1.config(text = 'Group 1 - speed modulated cells' )
                if self.answer_cellgroups[1] == True:
                    self.cellgroup_label_1.config(text = 'Group 2 - head direction cells' )
                if self.answer_cellgroups[2] == True:
                    self.cellgroup_label_1.config(text = 'Group 3 - border cells' )
                if self.answer_cellgroups[3] == True:
                    self.cellgroup_label_1.config(text = 'Group 4 - grid cells' )
                self.update_answer_counter()
                if self.exp1_disabled == True:
                    self.disable_exp1()
            else:
                self.updatelog()
                #generating json file
    def updatelog(self):
        ID=self.ID.get().lower()
        datatostore = dict()
        datatostore['unusedanswers'] = self.unusedanswers.get()
        datatostore['ID'] = ID
        datatostore['answer_cellgroups'] = self.answer_cellgroups
        datatostore['exp1_disabled'] = self.exp1_disabled
        with open(self.logdir + ID + '.json', 'w') as f_obj: json.dump(datatostore, f_obj)
        
        cellnums=list()
        cellnums.append(self.answer_1.get())
        cellnums.append(self.answer_2.get())
        cellnums.append(self.answer_3.get())
        cellnums_str=str()
        answer_str=str()
        for cellnum in cellnums:
            cellnums_str += str(cellnum) + ', '
        for answer in self.answer_cellgroups:
            answer_str += str(answer) + ', '
        with open(self.logdir + ID + '.log', 'a') as file_object:
            file_object.write(time.strftime('%Y.%m.%d. - %H:%M:%S'))
            file_object.write('   selected cells: ' + cellnums_str)
            file_object.write('   answers so far: ' + answer_str)
            file_object.write('   tries left: ' + str(self.unusedanswers.get()))
            file_object.write('   exp1 disabled: ' + str(self.exp1_disabled) + '\n')
            
        
    def startexperiment(self):
        neurons[0].smalldots = 60
        trajectories[0].timeback = 60
        self.newWindow = tk.Toplevel(self.master)
        self.app = IBO_runnungrat_GUI(self.newWindow,self.neurons,self.trajectories)
    
    def startexperiment_2(self):
        neurons[0].smalldots = np.inf
        trajectories[0].timeback = np.inf
        self.newWindow = tk.Toplevel(self.master)
        self.app = IBO_runnungrat_GUI(self.newWindow,self.neurons,self.trajectories)
    
    def update_answer_counter(self):
        self.unusedanswercounter.config(text = 'You have\n' + str(self.unusedanswers.get()) + '\ntries left.')
        
        
class IBO_runnungrat_GUI():
    def __init__(self, master,neurons,trajectories):
        self.neurons=neurons
        self.trajectories=trajectories
        self.exp1_handles=dict()
        self.exp1_handles['w']=550
        self.exp1_handles['h']=550
        figsize_big=(11, 11)
        dpi_big=60
        rect_big=[0.07, 0.22, .75, .75]
        self.exp1_handles['w_small']=320
        self.exp1_handles['h_small']=180
        smallfigsize=(4.2,2.8)
        smalldpi=60
        smallrect=[.22,.20, .75, .65]
        
        
        self.exp1_handles['window'] = master
        self.exp1_handles['window'].title("Experiment 1")
        
        self.exp1_handles['timenow'] = tk.DoubleVar()
        self.exp1_handles['timenow'].set(0)
        
        self.exp1_handles['cellnum'] = tk.IntVar()
        self.exp1_handles['cellnum'].set(1)
        
        self.exp1_handles['runnum'] = tk.IntVar()
        self.exp1_handles['runnum'].set(1)
        
        self.exp1_handles['onlinehist'] = tk.BooleanVar()
        self.exp1_handles['onlinehist'].set(False)
        
        self.exp1_handles['replayspeed'] = 1 
        self.exp1_handles['replayinterval_base'] = 0.05
        self.exp1_handles['steptime'] = [np.nan, np.nan, np.nan, np.nan, np.nan]
        
        
        self.exp1_handles['replayspeed_str'] = tk.StringVar()
        self.exp1_handles['replayspeed_str'].set(str(self.exp1_handles['replayspeed'])+'X')
        
        tk.Label(self.exp1_handles['window'],text = 'Neuron:').grid(row=0, column=0,sticky='E')
        tk.Label(self.exp1_handles['window'],text = 'Run:').grid(row=0, column=2,sticky='E')
        
        self.exp1_handles['cellselector'] = tk.OptionMenu(self.exp1_handles['window'], self.exp1_handles['cellnum'], *list(range(1, len(self.neurons)+1)), command=self.steppingrat ) 
        self.exp1_handles['cellselector'].grid(row=0, column=1, sticky='W')
        
        self.exp1_handles['runselector'] = tk.OptionMenu(self.exp1_handles['window'], self.exp1_handles['runnum'], *list(range(1, len(self.trajectories)+1)), command=self.steppingrat ) 
        self.exp1_handles['runselector'].grid(row=0, column=3, sticky='W')
        
        self.exp1_handles['online_analysis_selector_ON'] = tk.Radiobutton(self.exp1_handles['window'], text="Online analysis", variable=self.exp1_handles['onlinehist'], value=True, command=self.steppingrat)
        self.exp1_handles['online_analysis_selector_ON'].grid(row=0, column=7, sticky='W')
        self.exp1_handles['online_analysis_selector_OFF'] = tk.Radiobutton(self.exp1_handles['window'], text="Final analysis", variable=self.exp1_handles['onlinehist'], value=False, command=self.steppingrat)
        self.exp1_handles['online_analysis_selector_OFF'].grid(row=0, column=8, sticky='W')
        
        
        self.exp1_handles['TimeScale'] = tk.Scale(self.exp1_handles['window'], orient = 'horizontal', length = 600, variable = self.exp1_handles['timenow'], from_ = 0, to = self.trajectories[self.trajectories[0].runnum].data['locationtime'][-1], command = self.runningrat)
        #self.exp1_handles['TimeScale'].pack()
        self.exp1_handles['TimeScale'].grid(row=8,column=1, sticky='W',columnspan = 5)
        tk.Label(self.exp1_handles['window'],text = 'Time (s)').grid(row=9,column=1,columnspan = 5)
        
        self.exp1_handles['PlayButton'] = tk.Button(self.exp1_handles['window'], text ="Play", command = self.start_stop_runningrat )
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
        
        
        self.exp1_handles['canvas1'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['w'], height=self.exp1_handles['h'])
        self.exp1_handles['canvas1'].grid(row=2, column=1,columnspan=5,rowspan=3)
        self.exp1_handles['fig1'] = mpl.figure.Figure(figsize=figsize_big,dpi=dpi_big)
        self.exp1_handles['ax1'] = self.exp1_handles['fig1'].add_axes(rect_big)
        self.exp1_handles['ax1'].set_xlim(0,200)
        self.exp1_handles['ax1'].set_ylim(0,200)
        self.exp1_handles['ax1'].set_xlabel('X side (cm)')
        self.exp1_handles['ax1'].set_ylabel('Y side (cm)')
        self.exp1_handles['line'] =self.exp1_handles['ax1'].plot(0, 0,linewidth=3,zorder = 1)
        self.exp1_handles['dots_small'] =self.exp1_handles['ax1'].scatter(100,100,edgecolors='k',facecolor='r',linewidths=1,s=20,zorder = 2)
        self.exp1_handles['dots_big'] =self.exp1_handles['ax1'].scatter(50,50,edgecolors='k',facecolor='r',linewidths=1,s=150,zorder = 3)
        
        self.exp1_handles['arrow'] = self.exp1_handles['ax1'].arrow(10,10,10,10,width=5)
        self.exp1_handles['fig_photo_ax1'] = self.draw_figure(self.exp1_handles['canvas1'], self.exp1_handles['fig1'], loc=(0, 0))
        
        
        
        self.exp1_handles['canvas2'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['w_small'], height=self.exp1_handles['h_small'])
        self.exp1_handles['canvas2'].grid(row=1, column=7,rowspan=2,columnspan=2)
        self.exp1_handles['fig2'] = mpl.figure.Figure(figsize=smallfigsize,dpi=smalldpi)
        self.exp1_handles['ax2'] = self.exp1_handles['fig2'].add_axes(smallrect)
        self.exp1_handles['ax2'].set_xlim(0,200)
        self.exp1_handles['ax2'].set_ylim(0,200)
        self.exp1_handles['ax2'].set_xlabel('X location (cm)')
        self.exp1_handles['ax2'].set_ylabel('Average\nfiring frequency (Hz)')
        #self.exp1_handles['ax2_hist'] =self.exp1_handles['ax2'].plot(0, 0,linewidth=3)
        self.exp1_handles['ax2_hist'] =self.exp1_handles['ax2'].bar(0, 0)
        self.exp1_handles['ax2_line'] =self.exp1_handles['ax2'].plot(0, 0,linewidth=5,color='black')
        self.exp1_handles['fig_photo_ax2'] = self.draw_figure(self.exp1_handles['canvas2'], self.exp1_handles['fig2'], loc=(0, 0))
        
        self.exp1_handles['canvas3'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['w_small'], height=self.exp1_handles['h_small'])
        self.exp1_handles['canvas3'].grid(row=3, column=7,rowspan=1,columnspan=2,sticky='N')
        self.exp1_handles['fig3'] = mpl.figure.Figure(figsize=smallfigsize,dpi=smalldpi)
        self.exp1_handles['ax3'] = self.exp1_handles['fig3'].add_axes(smallrect)
        self.exp1_handles['ax3'].set_xlim(0,200)
        self.exp1_handles['ax3'].set_ylim(0,200)
        self.exp1_handles['ax3'].set_xlabel('Y location (cm)')
        self.exp1_handles['ax3'].set_ylabel('Average\nfiring frequency (Hz)')
        #self.exp1_handles['ax3_hist'] =self.exp1_handles['ax3'].plot(0, 0,linewidth=3)
        self.exp1_handles['ax3_hist'] =self.exp1_handles['ax3'].bar(0, 0)
        self.exp1_handles['ax3_line'] =self.exp1_handles['ax3'].plot(0, 0,linewidth=5,color='black')
        self.exp1_handles['fig_photo_ax3'] = self.draw_figure(self.exp1_handles['canvas3'], self.exp1_handles['fig3'], loc=(0, 0))
        
        self.exp1_handles['canvas4'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['w_small'], height=self.exp1_handles['h_small'])
        self.exp1_handles['canvas4'].grid(row=4, column=7,rowspan=1,columnspan=2,sticky='N')
        self.exp1_handles['fig4'] = mpl.figure.Figure(figsize=smallfigsize,dpi=smalldpi)
        self.exp1_handles['ax4'] = self.exp1_handles['fig4'].add_axes(smallrect)
        self.exp1_handles['ax4'].set_xlim(0,70)
        self.exp1_handles['ax4'].set_ylim(0,70)
        self.exp1_handles['ax4'].set_xlabel('Speed (cm/s)')
        self.exp1_handles['ax4'].set_ylabel('Average\nfiring frequency (Hz)')
        #self.exp1_handles['ax4_hist'] =self.exp1_handles['ax4'].plot(0, 0,linewidth=3)
        self.exp1_handles['ax4_hist'] =self.exp1_handles['ax4'].bar(0, 0)
        self.exp1_handles['ax4_line'] =self.exp1_handles['ax4'].plot(0, 0,linewidth=5,color='black')
        self.exp1_handles['fig_photo_ax4'] = self.draw_figure(self.exp1_handles['canvas4'], self.exp1_handles['fig4'], loc=(0, 0))
        
        self.exp1_handles['canvas5'] = tk.Canvas(self.exp1_handles['window'], width=self.exp1_handles['w_small'], height=self.exp1_handles['h_small'])
        self.exp1_handles['canvas5'].grid(row=5, column=7,rowspan=6,columnspan=2,sticky='N')
        self.exp1_handles['fig5'] = mpl.figure.Figure(figsize=smallfigsize,dpi=smalldpi)
        self.exp1_handles['ax5'] = self.exp1_handles['fig5'].add_axes(smallrect, projection = 'polar')
        self.exp1_handles['ax5'].set_theta_zero_location("W")
        self.exp1_handles['ax5'].set_rmin(0)
        #self.exp1_handles['ax5'].set_title('Head direction '+u'\N{DEGREE SIGN}')
        self.exp1_handles['ax5_polar'] =self.exp1_handles['ax5'].plot(0, 0,color='black')
        self.exp1_handles['ax5_polar_bar'] =self.exp1_handles['ax5'].bar(0, 0,color='black')
        self.exp1_handles['ax5_direction'] =self.exp1_handles['ax5'].plot(0, 1,color='black')
        self.exp1_handles['fig_photo_ax5'] = self.draw_figure(self.exp1_handles['canvas5'], self.exp1_handles['fig5'], loc=(0, 0))
        
        self.steppingrat()
        tk.Label(self.exp1_handles['window'],text = '       ').grid(row=0, column=6)
        tk.Label(self.exp1_handles['window'],text = 'Head direction '+u'\N{DEGREE SIGN}').grid(row=4, column=7,rowspan=1,columnspan=2,sticky='S')
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
    def draw_ax1(self):
        cellnum=self.neurons[0].cellnum
        runnum=self.neurons[0].runnum
        self.exp1_handles['line'][0].set_data(self.trajectories[runnum].trajectory_coordinates()[0],self.trajectories[runnum].trajectory_coordinates()[1])
        self.exp1_handles['dots_small'].set_offsets(np.c_[self.neurons[cellnum].APcoordinates_small()])
        self.exp1_handles['dots_big'].set_offsets(np.c_[self.neurons[cellnum].APcoordinates_big()])
        arrowcoords=self.trajectories[runnum].arrow_coordinates();
        self.exp1_handles['arrow'].remove()
        self.exp1_handles['arrow'] = self.exp1_handles['ax1'].arrow(arrowcoords[0],arrowcoords[1],arrowcoords[2],arrowcoords[3],width=3,zorder=4)
        self.exp1_handles['fig_photo_ax1'] = self.draw_figure(self.exp1_handles['canvas1'], self.exp1_handles['fig1'], loc=(0, 0)) # draw ax1
    
    def draw_ax2(self):
        cellnum=self.neurons[0].cellnum
        runnum=self.neurons[0].runnum
        timespent=self.trajectories[runnum].time_spent_in_X()
        apnum=self.neurons[cellnum].APnum_in_X()
        yvals=apnum[0]/timespent[0]
        yvals[np.isnan(yvals)]=0
        yvals[np.isinf(yvals)]=0
        #    self.exp1_handles['ax2_hist'][0].set_data(apnum[1],yvals)
        self.exp1_handles['ax2_hist'].remove()
        self.exp1_handles['ax2_hist'] =self.exp1_handles['ax2'].bar(apnum[1],yvals,8,color='blue')
        maxval=np.nanmax(yvals)
        if maxval==np.nan or maxval==0:
            maxval=1
        self.exp1_handles['ax2'].set_ylim(0,maxval)
        if neurons[0].timenow == 10**10:
            xloc = 0
        else:
            xloc = self.trajectories[runnum].arrow_coordinates()[0]
        self.exp1_handles['ax2_line'][0].set_data([xloc,xloc],[0,maxval])
        self.exp1_handles['fig_photo_ax2'] = self.draw_figure(self.exp1_handles['canvas2'], self.exp1_handles['fig2'], loc=(0, 0)) # draw ax2
    
    def draw_ax3(self):
        cellnum=self.neurons[0].cellnum
        runnum=self.neurons[0].runnum
        timespent=self.trajectories[runnum].time_spent_in_Y()
        apnum=self.neurons[cellnum].APnum_in_Y()
        yvals=apnum[0]/timespent[0]
        yvals[np.isnan(yvals)]=0
        yvals[np.isinf(yvals)]=0
        #    self.exp1_handles['ax3_hist'][0].set_data(apnum[1],yvals)
        self.exp1_handles['ax3_hist'].remove()
        self.exp1_handles['ax3_hist'] =self.exp1_handles['ax3'].bar(apnum[1],yvals,8,color='blue')
        maxval=np.nanmax(yvals)
        if maxval==np.nan or maxval==0:
            maxval=1
        self.exp1_handles['ax3'].set_ylim(0,maxval)
        if neurons[0].timenow == 10**10:
            yloc = 0
        else:
            yloc=self.trajectories[runnum].arrow_coordinates()[1]
        self.exp1_handles['ax3_line'][0].set_data([yloc,yloc],[0,maxval])
        self.exp1_handles['fig_photo_ax3'] = self.draw_figure(self.exp1_handles['canvas3'], self.exp1_handles['fig3'], loc=(0, 0)) # draw ax3
        
    def draw_ax4(self):
        cellnum=self.neurons[0].cellnum
        runnum=self.neurons[0].runnum
        timespent=self.trajectories[runnum].time_spent_in_speed()
        apnum=self.neurons[cellnum].APnum_in_speed()
        yvals=apnum[0]/timespent[0]
        yvals[np.isnan(yvals)]=0
        yvals[np.isinf(yvals)]=0
        #    self.exp1_handles['ax4_hist'][0].set_data(apnum[1],yvals)
        self.exp1_handles['ax4_hist'].remove()
        self.exp1_handles['ax4_hist'] =self.exp1_handles['ax4'].bar(apnum[1],yvals,3,color='blue')
        maxval=np.nanmax(yvals)
        if maxval==np.nan or maxval==0:
            maxval=1
        self.exp1_handles['ax4'].set_ylim(0,maxval)
        if neurons[0].timenow == 10**10:
            speed = 0
        else:
            speed = self.trajectories[runnum].speed_now()
        self.exp1_handles['ax4_line'][0].set_data([speed,speed],[0,maxval])
        self.exp1_handles['fig_photo_ax4'] = self.draw_figure(self.exp1_handles['canvas4'], self.exp1_handles['fig4'], loc=(0, 0)) # draw ax4
    
    def draw_ax5(self):
        cellnum=self.neurons[0].cellnum
        runnum=self.neurons[0].runnum
        timespent=self.trajectories[runnum].time_spent_in_headdirection()
        apnum=self.neurons[cellnum].APnum_in_headdirection()
        yvals=apnum[0]/timespent[0]
        yvals[np.isnan(yvals)]=0
        yvals[np.isinf(yvals)]=0
        xvals=np.deg2rad(apnum[1])#np.pi/
        xvals=np.append(xvals,xvals[0])
        yvals=np.append(yvals,yvals[0])
        
        maxval=np.nanmax(yvals)
        if maxval==np.nan or maxval==0:
            maxval=1
        #self.exp1_handles['ax5_polar'][0].set_data(xvals,yvals)
        self.exp1_handles['ax5_polar_bar'].remove()
        self.exp1_handles['ax5_polar_bar'] =self.exp1_handles['ax5'].bar(xvals,yvals,.25,color='blue')
        self.exp1_handles['ax5'].set_rmax(maxval)
        
        if neurons[0].timenow == 10**10:
            headdirection = 0
        else:
            headdirection  = np.deg2rad(self.trajectories[runnum].headdirection_now())

        self.exp1_handles['ax5_direction'][0].set_data([headdirection,headdirection],[0,maxval])
        
        self.exp1_handles['fig_photo_ax5'] = self.draw_figure(self.exp1_handles['canvas5'], self.exp1_handles['fig5'], loc=(0, 0)) # draw ax5
        
    
        
    def start_stop_runningrat(self):
        if self.exp1_handles['PlayButton']['text'] == 'Play':
            self.exp1_handles['PlayButton']['text'] = 'Pause' 
            self.exp1_handles['steptime'] = [np.nan, np.nan, np.nan, np.nan, np.nan]
            self.runningrat()
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
    
    def steppingrat(self,value=0):
        self.runningrat(self.neurons[0].timenow)
        if self.exp1_handles['onlinehist'].get()==False:
            timenow=self.neurons[0].timenow
            self.neurons[0].timenow= 10**10
            self.trajectories[0].timenow= 10**10
            self.draw_ax2()
            self.draw_ax3()
            self.draw_ax4()
            self.draw_ax5()
            self.neurons[0].timenow=timenow
            self.trajectories[0].timenow=timenow
    
    def runningrat(self,settime=-1):
        if settime==-1:
            self.exp1_handles['steptime'][1:]=self.exp1_handles['steptime'][:-1]
            self.exp1_handles['steptime'][0]=time.time()
            if any(np.isnan(self.exp1_handles['steptime'])):
                self.exp1_handles['replayinterval_base'] = 0.05
            else:
                self.exp1_handles['replayinterval_base'] =np.abs(np.mean(np.diff(self.exp1_handles['steptime'])))
                
            self.neurons[0].timenow += self.exp1_handles['replayspeed'] * self.exp1_handles['replayinterval_base']
            self.exp1_handles['timenow'].set(self.neurons[0].timenow)
        else:
            self.neurons[0].timenow = float(settime)
        
        self.trajectories[0].timenow = self.neurons[0].timenow
        if self.exp1_handles['cellnum'].get() != self.neurons[0].cellnum + 1:
            self.neurons[0].cellnum = self.exp1_handles['cellnum'].get() - 1
        if self.exp1_handles['runnum'].get() != self.neurons[0].runnum + 1:
            self.neurons[0].runnum = self.exp1_handles['runnum'].get() - 1
            self.trajectories[0].runnum = self.exp1_handles['runnum'].get() - 1
            self.exp1_handles['TimeScale'].configure(to=self.trajectories[self.trajectories[0].runnum].data['locationtime'][-1])
        self.draw_ax1()
        #    runInParallel(self.draw_ax2(), draw_ax3(), draw_ax4(), draw_ax5())
        if self.exp1_handles['onlinehist'].get() == True:
            self.draw_ax2()
            self.draw_ax3()
            self.draw_ax4()
            self.draw_ax5()
#        print(self.exp1_handles['replayinterval_base'])
        if self.exp1_handles['PlayButton']['text'] == 'Pause' and settime==-1:
            if self.exp1_handles['replayinterval_base']<.030:
                delay = 30
            else:
                delay = 1
            self.exp1_handles['window'].after(delay, self.runningrat)



root = tk.Tk()
root.title('Virtual navigation')
app = IBO_mainwindow(root,neurons, trajectories, basedir)
root.mainloop()
