#! /usr/bin/env python
from __future__ import division
import os, sys
import logging
from threading import Thread
import time
from numpy import *
import decimal
from collections import *

import paramiko
paramiko.util.log_to_file('/tmp/paramiko.log')

#----------------------------------
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from pylab import *
from itertools import cycle

import VerticalScrolledFrame as VSF
import Tooltip
import ViewLog as VL

import ParamsDict as PrDt
import MakefileDict as MkDt
import TooltipDict as TtDt

import subprocess, shlex

import ttk
import tkFileDialog, Tkconstants

if sys.version_info[0] < 3:
    from Tkinter import *
    from Tkinter import _setit
else:
    from tkinter import *
    from tkinter import _setit

from CosmoSuite import *

#----------------------------------
def destroy(e): sys.exit()

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    return proc_stdout

class IODirector(object):
    def __init__(self, text_area):
        self.text_area = text_area

class StdoutDirector(IODirector):
    def write(self, msg):
        self.text_area.insert(END, msg)
        self.text_area.see(END)
    
    def flush(self):
        pass

#----------------------------------
class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("CosmoSuite v.1")
        
        #---------------------------------------
        for r in range(6):
            self.master.rowconfigure(r, weight=2)
        for c in range(5):
            self.master.columnconfigure(c, weight=2)
        #---------------------------------------
        self.master.rowconfigure(0, weight=0)
        #self.master.columnconfigure(0, weight=0)

        #---------------------------------------
        self.initialize()
        self.Toolbar(self.Frame_1); self.MainFrame(self.Frame_2)
        self.PlotPan(self.Frame_3); self.Terminal_infoPan(self.Frame_4)
        
    def initialize(self):
        
        style = ttk.Style()
        style.layout('TNotebook.Tab', [])
        
        # Status Bar :-----
        self.statusVariable = StringVar()
        self.status = Label(self.master, textvariable = self.statusVariable, anchor = "w", fg = "yellow", bg = "blue")
        self.status.grid(column = 0, row = 7,columnspan = 5, sticky = 'EWS')
        self.statusVariable.set(u"Welcome to CosmoSuite")

        # Frame 1 :------------------------------------------------------
        self.Frame_1 = PanedWindow(self.master, bg="white smoke")
        self.Frame_1.grid(row = 0, column = 0, rowspan = 1, columnspan = 5, sticky = W+E+N+S)
        
        # Frame 2 :-----------------------------------------------------
        self.Frame_2 = Frame(self.master, bg="white", bd= 1, relief= RIDGE)
        self.Frame_2.grid(row = 1, column = 0, rowspan = 5, columnspan = 2, sticky = W+E+N+S)

        # Frame 3 :-----------------------------------------------------
        self.Frame_3 = Frame(self.master, bg="white", bd= 3, relief= GROOVE)
        self.Frame_3.grid(row = 1, column = 2, rowspan = 3, columnspan = 3, sticky = W+E+N+S)

        # Frame 4 :------------------------------------------------------
        self.Frame_4 = Frame(self.master, bg="white smoke", bd= 5, relief= RIDGE)
        self.Frame_4.grid(row = 4, column = 2, rowspan = 2, columnspan = 3, sticky = W+E+N+S)
    
    def Toolbar(self, frame):
        Quit_photo = PhotoImage(file="label_photos/quit.gif")
        Quit = Button(frame, text=u"Quit", image = Quit_photo, command=sys.exit)
        Quit.photo = Quit_photo
        Quit.grid(column=6, row=0, sticky= W+E+N+S, pady = 5)
        Quit.pack(side="right")
    
        Label(frame, text = "", bg='white smoke', height = 2).pack(side="right")
        
        help_photo = PhotoImage(file="label_photos/Info.gif")
        self.help = Button(frame, text = u"Help", image = help_photo, fg='blue', command = self.callback_info)
        self.help.photo = help_photo
        self.help.grid(column = 0, row = 0, sticky = W+E+N+S, pady = 5)
        self.help.pack(side="right")
        
        Label(frame, text = "", bg='white smoke', height = 2).pack(side="right")
        
        log_photo = PhotoImage(file="label_photos/log.gif")
        self.log = Button(frame, text = u"Help", image = log_photo, fg='blue', command = self.callback_log)
        self.log.photo = log_photo
        self.log.grid(column = 0, row = 0, sticky = W+E+N+S, pady = 5)
        self.log.pack(side="right")
        
        terminal_photo = PhotoImage(file="label_photos/terminal.gif")
        self.terminal = Button(frame, text = u"Help", image = terminal_photo, fg='blue', command = self.callback_terminal)
        self.terminal.photo = terminal_photo
        self.terminal.grid(column = 0, row = 0, sticky = W+E+N+S, pady = 5)
        self.terminal.pack(side="right")
        
        Label(frame, text = "", bg='white smoke', height = 2).pack(side="right")
        
        self.run_mode_local_photo = PhotoImage(file="label_photos/local.gif")
        self.run_mode_network_photo = PhotoImage(file="label_photos/networking.gif")
        self.run_mode = Button(frame, text = u"Run Mode", fg='blue', image = self.run_mode_local_photo)
        self.run_mode.photo = self.run_mode_local_photo
        self.run_mode.grid(column = 1, row = 0, sticky = W+E+N+S, pady = 5)
        self.run_mode.pack(side="left")
        self.run_mode.bind("<ButtonPress-1>", self.callback_run_network_mode)
        self.run_mode_logic = "local"
        Tooltip.ToolTip(self.run_mode, follow_mouse = 1, text = "Local/Remote Toggle. Right click to retrive.")
        
        Label(frame, text = "", bg='white smoke', height = 2).pack(side="left")
        
        new_photo = PhotoImage(file="label_photos/Add.gif")
        self.new = Button(frame, text = u"Home", fg='blue', image = new_photo, command = self.callback_new_run)
        self.new.photo = new_photo
        self.new.grid(column = 1, row = 0, sticky = W+E+N+S, pady = 5)
        self.new.pack(side="left")
        
        run_photo = PhotoImage(file="label_photos/run.gif")
        self.run = Button(frame, text = u"Home", fg='blue', image = run_photo, command = self.callback_RunSpicf)
        self.run.photo = run_photo
        self.run.grid(column = 1, row = 0, sticky = W+E+N+S, pady = 5)
        self.run.pack(side="left")
        
        self.run = (u'Perturbative Cosmology', u'N-Body Simulation')
        self.runVar = StringVar()
        self.runOpt = OptionMenu(frame, self.runVar, *self.run,  command = self.runfunc)
        self.runOpt.grid(column = 0, row = 0, columnspan = 2, pady = 5, sticky= W+E+N+S)
        self.runOpt.pack(side="left")
        self.runOpt.config(width=20)
        self.runVar.set(u'Perturbative Cosmology')
        
        Label(frame, text = "", bg='white smoke', height = 2).pack(side="left")
        
        system_performance_photo = PhotoImage(file="label_photos/performance.gif")
        self.system_performance = Button(frame, text = u"System Performance", fg='blue', image = system_performance_photo, command = self.callback_sysPerf)
        self.system_performance.photo = system_performance_photo
        self.system_performance.grid(column = 1, row = 0, sticky = W+E+N+S, pady = 5)
        self.system_performance.pack(side="right")
        
        analysis_photo = PhotoImage(file="label_photos/Toolbox.gif")
        self.analysis = Button(frame, text = u"Home", fg='blue', image = analysis_photo, command = self.callback_Toolbox)
        self.analysis.photo = analysis_photo
        self.analysis.grid(column = 1, row = 0, sticky = W+E+N+S, pady = 5)
        self.analysis.pack(side="left")
        
        codes_photo = PhotoImage(file="label_photos/code.gif")
        self.codes_compilation = Button(frame, text = u"Codes Compilation", fg='blue', image = codes_photo, command = self.callback_codes)
        self.codes_compilation.photo = codes_photo
        self.codes_compilation.grid(column = 1, row = 0, sticky = W+E+N+S, pady = 5)
        self.codes_compilation.pack(side="left")
        
        self.Codes = (u'CAMB', u'N-GenIC', u'Gadget2',u'AHF', u'POWMS')
        self.CodesVar = StringVar()
        self.CodesOpt = OptionMenu(frame, self.CodesVar, *self.Codes,  command = self.func)
        self.CodesOpt.grid(column = 0, row = 0, columnspan = 2, pady = 5, sticky= W+E+N+S)
        self.CodesOpt.pack(side="left")
        self.CodesOpt.config(width=10)
        self.CodesVar.set(u'CAMB')
        
        code_compile_photo = PhotoImage(file="label_photos/compile.gif")
        self.Code_Compile_button = Button(frame, text = u"Compile", foreground = 'red',image = code_compile_photo, command = self.Code_Compile)
        self.Code_Compile_button.image = code_compile_photo
        self.Code_Compile_button.grid(column = 1, row = 0, pady = 5, sticky= W+E+N+S)
        self.Code_Compile_button.pack(side="left")
        
        Label(frame, text = "", bg='white smoke', height = 2).pack(side="left")
        
        results_photo = PhotoImage(file="label_photos/results.gif")
        self.results = Button(frame, text = u"Home", fg='blue', image = results_photo, command = self.callback_Home)
        self.results.photo = results_photo
        self.results.grid(column = 1, row = 0, sticky = W+E+N+S, pady = 5)
        self.results.pack(side="left")

    def PlotPan(self, frame):
        self.f, (ax1, ax2) = subplots(2, sharex=True)
        gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
        self.ax1 = subplot(gs[0]); self.ax2 = subplot(gs[1])
        self.ax3 = axes([.16, .35, .3, .3])
        self.f.subplots_adjust(hspace=0)
        self.canvas = FigureCanvasTkAgg(self.f, master = frame)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, frame)
        self.canvas.get_tk_widget().grid(column = 0, row = 0, pady = 5)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def Terminal_infoPan(self, frame):
        self.TermInfo_nb = ttk.Notebook(frame, padding = -5)
        self.Info_page = ttk.Frame(self.TermInfo_nb); self.Term_page = ttk.Frame(self.TermInfo_nb)
        
        #------------------------
        self.TermInfo_nb.add(self.Info_page, text='Logger & info', sticky = W+E+N+S)
        self.TermInfo_nb.add(self.Term_page, text='Terminal', sticky = W+E+N+S)
        self.TermInfo_nb.pack(side="top", fill="both", expand=True)
        
        #----- logger !!
        readme = open('readme.txt')
        self.Welcome_str = readme.read()
        self.text_area = Text(self.Info_page, height=15, width=90, bg='light cyan')
        self.text_area.pack(side="top", fill="both", expand=True)
        self.text_area.insert(END, self.Welcome_str)
        #self.text_area.config(state=DISABLED)
        
        #----- Terminal !!
#        self.Terminal_area = Canvas(self.Term_page, width=600)
#        self.Terminal_area.pack(fill="both", expand=True)
#        Term_wid = self.Terminal_area.winfo_id()
#        os.system('xterm -into %d -aw -geometry 100x12 -sb -bg black -fg white -rightbar -mk_width &' %Term_wid)

    def MainFrame(self, frame):
        self.main_nb = ttk.Notebook(frame, padding = -5)
        self.Main_page = ttk.Frame(self.main_nb); self.Anals_page = ttk.Frame(self.main_nb);  self.SysPerf_page = ttk.Frame(self.main_nb)
            
        #------------------------
        self.main_nb.add(self.Main_page, text='Main')
        self.main_nb.add(self.Anals_page, text='Analysis & Results')
        self.main_nb.add(self.SysPerf_page, text='System Preferences')
        self.main_nb.pack(side="top", fill="both", expand=True)
    
        #------------------------
        self.MainPage(self.Main_page); self.SysPerfPage(self.SysPerf_page); self.AnalysResultsPage(self.Anals_page)
    
    def AnalysResultsPage(self, page):
    
        for r in range(5):
            page.rowconfigure(r, weight=2)
        
        for x in range(2):
            page.columnconfigure(x, weight=2)
        
        #------------------------
        self.Datafile_Frame = Frame(page, bg="white", bd= 1, relief= RIDGE)
        self.Datafile_Frame.grid(row = 0, column = 0, rowspan = 4, columnspan = 2, sticky = W+E+N+S)

        #------------------------
        self.Plot_Frame = Frame(page, bg="white smoke", bd= 1, relief= RIDGE)
        self.Plot_Frame.grid(row = 4, column = 0, rowspan = 1, columnspan = 2, sticky = W+E+N+S)
            
        self.Plot_List_group = LabelFrame(self.Plot_Frame, text = "Data Plots")
        self.Plot_List_group.grid(row = 0, column = 0, rowspan = 2, columnspan = 1, sticky = W+E+N+S)
        for i in range(2):
            Grid.columnconfigure(self.Plot_List_group, i, weight=2); Grid.rowconfigure(self.Jobs_List_group, i, weight=2)
        
        self.Plot_List_Lb = Listbox(self.Plot_List_group, selectmode = EXTENDED, bg = "white smoke")
        self.Plot_List_Lb.grid(row = 0, column = 0, sticky = W+E+N+S)
            
        self.PlotOpts_group = LabelFrame(self.Plot_Frame, text = "Plot Options")
        self.PlotOpts_group.grid(row = 0, column = 1, rowspan = 2, columnspan = 1, sticky = W+E+N+S)
        
        for i in range(6):
            Grid.columnconfigure(self.PlotOpts_group, i, weight=2)
        
        #----------------------
        Label(self.PlotOpts_group, text = 'Plot Type').grid(row = 0, column = 0, sticky = W)
        self.PlotOpts_list = ['plot', 'semilogx', 'semilogy','loglog']
        self.PlotOpts_Var = StringVar()
        self.PlotOpt = OptionMenu(self.PlotOpts_group, self.PlotOpts_Var, *self.PlotOpts_list)
        self.PlotOpt.grid(row = 0, column = 1, columnspan = 2, pady = 5, sticky = W+E+N+S)
        self.PlotOpt.config(width=12)
        self.PlotOpts_Var.set(u'plot')
        
        Label(self.PlotOpts_group, text = 'x-axis').grid(row = 1, column = 0, sticky = W)

        Label(self.PlotOpts_group, text = 'y-axis').grid(row = 1, column = 2, sticky = W)
        
        self.log10x_axis_Var = StringVar()
        self.log10x_axis_ChkBtt = Checkbutton(self.PlotOpts_group, text = 'log10(x-axis)', variable = self.log10x_axis_Var , onvalue = "T", offvalue = "F")
        self.log10x_axis_ChkBtt.grid(row = 1, column = 4, sticky = W)

        self.log10y_axis_Var = StringVar()
        self.log10y_axis_ChkBtt = Checkbutton(self.PlotOpts_group, text = 'log10(y-axis)', variable = self.log10y_axis_Var , onvalue = "T", offvalue = "F")
        self.log10y_axis_ChkBtt.grid(row = 1, column = 5, sticky = W)
    
        Label(self.PlotOpts_group, text = 'x-label').grid(row = 2, column = 0, sticky = W)
        self.xlabel_Var = StringVar()
        self.xlabel_Entry = Entry(self.PlotOpts_group, textvariable=self.xlabel_Var, width = 8)
        self.xlabel_Entry.grid(row=2, column=1, sticky= W+E+N+S)

        Label(self.PlotOpts_group, text = 'y-label').grid(row = 2, column = 2, sticky = W)
        self.ylabel_Var = StringVar()
        self.ylabel_Entry = Entry(self.PlotOpts_group, textvariable=self.ylabel_Var, width = 8)
        self.ylabel_Entry.grid(row=2, column=3, sticky= W+E+N+S)

        Label(self.PlotOpts_group, text = 'x-range').grid(row = 1, column = 3, sticky = W)
#
#        Label(self.PlotOpts_group, text = 'y-range').grid(row = 2, column = 0, sticky = W)
#
#        Label(self.PlotOpts_group, text = 'line color').grid(row = 2, column = 1, sticky = W)
#    
#        Label(self.PlotOpts_group, text = 'line style').grid(row = 2, column = 2, sticky = W)
#        
#        Label(self.PlotOpts_group, text = 'line thickness').grid(row = 2, column = 3, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'maker color').grid(row = 3, column = 0, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'maker style').grid(row = 3, column = 1, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'x ticks').grid(row = 3, column = 2, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'y ticks').grid(row = 3, column = 3, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'maker size').grid(row = 4, column = 0, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'plot label').grid(row = 4, column = 1, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'show legend').grid(row = 4, column = 2, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'legend options').grid(row = 4, column = 3, sticky = W)
#        
#        Label(self.PlotOpts_group, text = 'show resuidual').grid(row = 5, column = 0, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'resuidual y-label').grid(row = 5, column = 1, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'resuidual x-range').grid(row = 5, column = 2, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'resuidual y-range').grid(row = 5, column = 3, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'show magnify plot').grid(row = 6, column = 0, sticky = W)
#            
#        Label(self.PlotOpts_group, text = 'magnify x-range').grid(row = 6, column = 1, sticky = W)
#    
#        Label(self.PlotOpts_group, text = 'magnify y-range').grid(row = 6, column = 2, sticky = W)

    #def plot_func(self)
    

    def SysPerfPage(self, page):
        self.SysPerf_frame =  VSF.VerticalScrolledFrame(page)
        self.SysPerf_frame.pack(side="top", fill="both", expand=True)
        
        for x in range(6):
            Grid.columnconfigure(self.SysPerf_frame.interior, x, weight=2)

        self.ssh_setting = LabelFrame(self.SysPerf_frame.interior, text = "SSH Remote Server Setting")
        self.ssh_setting.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        Label(self.ssh_setting, text="Host Server").grid(row=0, column=0, sticky= W)
        self.Host_Server_Var = StringVar()
        self.Host_Server = Entry(self.ssh_setting, textvariable=self.Host_Server_Var, width = 30)
        self.Host_Server.grid(row=0, column=1, sticky= W+E+N+S)
        self.Host_Server_Var.set("login6.sciama.icg.port.ac.uk")
    
        Label(self.ssh_setting, text="Port").grid(row=0, column=2, sticky= W)
        self.Host_Port_Var = IntVar()
        self.Host_Port = Entry(self.ssh_setting, textvariable=self.Host_Port_Var)
        self.Host_Port.grid(row=0, column=3, sticky= W+E+N+S)
    
        Label(self.ssh_setting, text="User Name").grid(row=1, column=0, sticky= W)
        self.UserName_Var = StringVar()
        self.UserName = Entry(self.ssh_setting, textvariable=self.UserName_Var)
        self.UserName.grid(row=1, column=1, sticky= W+E+N+S)
    
        Label(self.ssh_setting, text="Password").grid(row=1, column=2, sticky= W)
        self.PassWord_Var = StringVar()
        self.PassWord = Entry(self.ssh_setting, textvariable=self.PassWord_Var, show="*")
        self.PassWord.grid(row=1, column=3, sticky= W+E+N+S)
        
        self.PBS_setting = LabelFrame(self.SysPerf_frame.interior, text = "PBS Job Script Setting")
        self.PBS_setting.grid(row = 1, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        Label(self.PBS_setting, text = "Email").grid(row=0, column=0, sticky= W)
        self.Email_Var = StringVar()
        self.Email_Entry = Entry(self.PBS_setting, textvariable=self.Email_Var)
        self.Email_Entry.grid(row=0, column=1, columnspan = 4, sticky= W+E+N+S)
        
        Label(self.PBS_setting, text = "N-GenIC").grid(row=1, column=1, sticky= W)
        
        Label(self.PBS_setting, text = "Gadget 2").grid(row=1, column=2, sticky= W)
        Label(self.PBS_setting, text = "AHF").grid(row=1, column=3, sticky= W)
        Label(self.PBS_setting, text = "POWMS").grid(row=1, column=4, sticky= W)
        
        
        Label(self.PBS_setting, text = "Nodes").grid(row=2, column=0, sticky= W)
        Label(self.PBS_setting, text = "PPN").grid(row=3, column=0, sticky= W)
        
        
        # N-GenIC :-------------
        self.NGenIC_nc_Var = IntVar()
        self.NGenIC_nc_Entry = Entry(self.PBS_setting, textvariable = self.NGenIC_nc_Var, width = 8)
        self.NGenIC_nc_Entry.grid(row=2, column=1, sticky= W)
        
        self.NGenIC_np_Var = IntVar()
        self.NGenIC_np_Entry = Entry(self.PBS_setting, textvariable = self.NGenIC_np_Var, width = 8)
        self.NGenIC_np_Entry.grid(row=3, column=1, sticky= W)
        
        # Gadget 2 :------------
        self.Gadget2_nc_Var = IntVar()
        self.Gadget2_nc_Entry = Entry(self.PBS_setting, textvariable = self.Gadget2_nc_Var, width = 8)
        self.Gadget2_nc_Entry.grid(row=2, column=2, sticky= W)
        
        self.Gadget2_np_Var = IntVar()
        self.Gadget2_np_Entry = Entry(self.PBS_setting, textvariable = self.Gadget2_np_Var, width = 8)
        self.Gadget2_np_Entry.grid(row=3, column=2, sticky= W)
        
        # AHF :------------------
        self.AHF_nc_Var = IntVar()
        self.AHF_nc_Entry = Entry(self.PBS_setting, textvariable = self.AHF_nc_Var, width = 8)
        self.AHF_nc_Entry.grid(row=2, column=3, sticky= W)
        
        self.AHF_np_Var = IntVar()
        self.AHF_np_Entry = Entry(self.PBS_setting, textvariable = self.AHF_np_Var, width = 8)
        self.AHF_np_Entry.grid(row=3, column=3, sticky= W)
        
        # POWMS :------------------
        self.POWMS_nc_Var = IntVar()
        self.POWMS_nc_Entry = Entry(self.PBS_setting, textvariable = self.POWMS_nc_Var, width = 8)
        self.POWMS_nc_Entry.grid(row=2, column=4, sticky= W)
        
        self.POWMS_np_Var = IntVar()
        self.POWMS_np_Entry = Entry(self.PBS_setting, textvariable = self.POWMS_np_Var, width = 8)
        self.POWMS_np_Entry.grid(row=3, column=4, sticky= W)
        
        #-----------------------------
        self.Libs_Include_Dirct = LabelFrame(self.SysPerf_frame.interior, text = "N-GenIC/Gadget 2 C-Compilor Setting")
        self.Libs_Include_Dirct.grid(row = 2, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        #-------------
        self.SysType_list = ['Local', 'Sciama', 'MPA','OpteronMPA' ,'Regatta', 'OPA_Cluster32', 'OPA_Cluster64', 'Mako', 'RZG_LinuxCluster', 'RZG_LinuxCluster_gcc']
        self.SysType_Var = StringVar()
        self.SysTypeOpt = OptionMenu(self.Libs_Include_Dirct, self.SysType_Var, *self.SysType_list, command = self.SysType_Select)
        self.SysTypeOpt.grid(column = 0, row = 0, pady = 5, columnspan = 1, sticky = W+E+N+S)
        self.SysTypeOpt.config(width=15)
        self.SysType_Var.set(u'Local')
        
        self.InclLib_listVar = OrderedDict([]); self.InclLib_Entry = OrderedDict([])
        for i in range(len(MkDt.LibIncls_dict)):
            self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]] = MkDt.LibIncls_dict.keys()[i] + '_Var'
            self.InclLib_Entry[MkDt.LibIncls_dict.keys()[i]] = MkDt.LibIncls_dict.keys()[i] + '_Entry'
        
        for i in range(len(MkDt.LibIncls_dict)):
            self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]] = StringVar()
            Label(self.Libs_Include_Dirct, text = MkDt.LibIncls_dict.keys()[i]).grid(column = 0, row = i+1, pady = 5, sticky = W)
            self.InclLib_Entry[MkDt.LibIncls_dict.keys()[i]] = Entry(self.Libs_Include_Dirct, textvariable=self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]], width=50)

            self.InclLib_Entry[MkDt.LibIncls_dict.keys()[i]].grid(column = 1, row = i+1, pady = 5, sticky = W+E+N+S)
            self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_dict.values()[i])

    def MainPage(self, page):

        for r in range(5):
            page.rowconfigure(r, weight=2)

        for x in range(2):
            page.columnconfigure(x, weight=2)

        #------------------------
        self.Entry_Frame = Frame(page, bg="white", bd= 1, relief= RIDGE)
        self.Entry_Frame.grid(row = 0, column = 0, rowspan = 4, sticky = W+E+N+S)
        
        self.NewRun_nb = ttk.Notebook(self.Entry_Frame,  padding = -5)
        self.NewRun_page = ttk.Frame(self.NewRun_nb); self.Codes_Compile_page = ttk.Frame(self.NewRun_nb); self.Run_Specif_page = ttk.Frame(self.NewRun_nb)
        
        self.NewRun_nb.add(self.NewRun_page, text='New Run')
        self.NewRun_nb.add(self.Codes_Compile_page, text='Codes Compilation')
        self.NewRun_nb.add(self.Run_Specif_page, text='Run Specifics')
        
        self.NewRun_nb.pack(side="top", fill="both", expand=True)
        
        #--------------------------------------
        for x in range(13):
            Grid.columnconfigure(self.NewRun_page, x, weight=2)
        
        for y in range(4):
            Grid.rowconfigure(self.NewRun_page, y, weight=2)
        
        self.Name_Dict_group = LabelFrame(self.NewRun_page, text = "Run Name & Directory")
        self.Name_Dict_group.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        Grid.rowconfigure(self.NewRun_page, 0, weight=0)
        
        for x in range(2):
            Grid.columnconfigure(self.Name_Dict_group, x, weight=2)
        for y in range(2):
            Grid.rowconfigure(self.Name_Dict_group, y, weight=2)
        
        Label(self.Name_Dict_group, text="Local Directory", width=15).grid(row=0, column=0, sticky= W)
        self.dirtext = 'Click to Select Working Directory'
        self.DirtVar = StringVar()
        self.DirtVar.trace("w", self.callback_NBodyTrace)
        self.SourcDirct = Entry(self.Name_Dict_group, textvariable=self.DirtVar, foreground= 'red', width=30)
        self.SourcDirct.grid(row=0, column=1, sticky= W+E+N+S)
        #self.SourcDirct.insert(0, self.dirtext)
        Tooltip.ToolTip(self.SourcDirct, follow_mouse = 1, text = self.dirtext)
        self.SourcDirct.bind("<Button-1>", self.openDirectory)
        
        Label(self.Name_Dict_group, text="Run Name").grid(row=0, column=2, sticky= W)
        self.Run_nameVar = StringVar()
        self.Run_nameVar.trace("w", self.callback_NBodyTrace)
        self.Run_name = Entry(self.Name_Dict_group, textvariable = self.Run_nameVar)
        self.Run_name.grid(row=0, column=3, sticky= W+E+N+S)
        
        self.run_mode_logic = "local"
        self.RemoteDirt_label = Label(self.Name_Dict_group, text="Remote Directory", fg = 'red', width=15)
        self.Remote_DirtVar = StringVar()
        self.Remote_DirtVar.trace("w", self.callback_NBodyTrace)
        self.RemoteDirct = Entry(self.Name_Dict_group, textvariable=self.Remote_DirtVar, foreground= 'red', width=30)
        
        self.Cosmo_Parms_group = LabelFrame(self.NewRun_page, text = "Cosmological Parameters")
        self.Cosmo_Parms_group.grid(row = 1, column = 0, columnspan = 6, sticky = W+E+N+S)
        Grid.rowconfigure(self.NewRun_page, 1, weight=0)
        
        for x in range(13):
            Grid.columnconfigure(self.Cosmo_Parms_group, x, weight=2)
        
        for y in range(4):
            Grid.rowconfigure(self.Cosmo_Parms_group, y, weight=2)
        
        self.Cosmology_Data = ['Planck', 'WMAP9', 'WMAP7', 'WMAP5', 'WMAP3', 'WMAP1', 'WALLABY', 'GIGGLEZ', 'Custom']
        self.Cosmology_Var = StringVar()
        self.CosmologyOpt = OptionMenu(self.Cosmo_Parms_group, self.Cosmology_Var, *self.Cosmology_Data, command = self.CosmoParm_Select)
        self.CosmologyOpt.grid(column = 0, row = 0, pady = 5, columnspan = 2, sticky = W+E+N+S)
        self.CosmologyOpt.config(width=15)
        self.Cosmology_Var.set(u'Select')
        
        Omega_b_photo = PhotoImage(file="label_photos/Omega_b.gif")
        Omega_m_photo = PhotoImage(file="label_photos/Omega_m.gif")
        Omega_Lambda_photo = PhotoImage(file="label_photos/Omega_lambda.gif")
        H_0_Photo = PhotoImage(file="label_photos/H_0.gif")
        sigma_8_photo = PhotoImage(file="label_photos/sigma_8.gif")
        n_s_photo = PhotoImage(file="label_photos/n_s.gif")
        Gamma_photo = PhotoImage(file="label_photos/Gamma.gif")
        phi_0_photo = PhotoImage(file="label_photos/phi_0.gif")
        w_x_photo = PhotoImage(file="label_photos/w_x.gif")
        self.w_Lambda_photo = PhotoImage(file="label_photos/w_Lambda.gif")
        cs2_photo = PhotoImage(file="label_photos/cs2.gif")
        zi_photo = PhotoImage(file="label_photos/zi.gif")
        zf_photo = PhotoImage(file="label_photos/zf.gif")
        zcalc_photo = PhotoImage(file="label_photos/zcalc.gif")
        f_NL_photo = PhotoImage(file="label_photos/f_NL.gif")
        
        Omega_Lambda_label = Label(self.Cosmo_Parms_group, text="Omega_Lambda", image = Omega_Lambda_photo)
        Omega_Lambda_label.photo = Omega_Lambda_photo
        Omega_Lambda_label.grid(row=1, column=0, sticky= W+E+N+S, pady = 5)
        
        self.Omega_l_Var= DoubleVar()
        self.Omega_l_Var.trace("w", self.callback_NBodyTrace)
        self.Omega_l= Entry(self.Cosmo_Parms_group, textvariable=self.Omega_l_Var, width=10)
        self.Omega_l.grid(row=1, column=1, sticky= W+E+N+S, pady = 5)
        
        
        Omega_m_label = Label(self.Cosmo_Parms_group, text="Omega_m", image = Omega_m_photo)
        Omega_m_label.photo = Omega_m_photo
        Omega_m_label.grid(row=1, column=2, sticky= W+E+N+S, pady = 5)
        
        self.Omega_m_Var= DoubleVar()
        self.Omega_m_Var.trace("w", self.callback_NBodyTrace)
        self.Omega_m= Entry(self.Cosmo_Parms_group, textvariable=self.Omega_m_Var, width=10)
        self.Omega_m.grid(row=1, column=3, sticky= W+E+N+S, pady = 5)
        
        Omega_b_label = Label(self.Cosmo_Parms_group, text = "Oemga_b", image = Omega_b_photo)
        Omega_b_label.photo = Omega_b_photo
        Omega_b_label.grid(row=1, column=4, sticky= W+E+N+S, pady = 5)
        
        self.Omega_bVar= DoubleVar()
        self.Omega_bVar.trace("w", self.callback_NBodyTrace)
        self.Omega_b= Entry(self.Cosmo_Parms_group, textvariable=self.Omega_bVar, width=10)
        self.Omega_b.grid(row=1, column=5, sticky= W+E+N+S, pady = 5)
        
        H_0_label = Label(self.Cosmo_Parms_group, text="H_0", image = H_0_Photo)
        H_0_label.photo = H_0_Photo
        H_0_label.grid(row=2, column=0, sticky= W+E+N+S, pady = 5)
        
        self.H_0Var= DoubleVar()
        self.H_0Var.trace("w", self.callback_NBodyTrace)
        self.H_0= Entry(self.Cosmo_Parms_group, textvariable=self.H_0Var, width=10)
        self.H_0.grid(row=2, column=1, sticky= W+E+N+S, pady = 5)
        
        sigma_8_label = Label(self.Cosmo_Parms_group, text="sigma_8", image = sigma_8_photo)
        sigma_8_label.photo = sigma_8_photo
        sigma_8_label.grid(row=2, column=2, sticky= W+E+N+S, pady = 5)
        
        self.sigma_8Var= DoubleVar()
        self.sigma_8Var.trace("w", self.callback_NBodyTrace)
        self.sigma_8= Entry(self.Cosmo_Parms_group, textvariable=self.sigma_8Var, width=10)
        self.sigma_8.grid(row=2, column=3, sticky= W+E+N+S, pady = 5)
        
        n_s_label = Label(self.Cosmo_Parms_group, text="n_s", image = n_s_photo)
        n_s_label.photo = n_s_photo
        n_s_label.grid(row=2, column=4, sticky= W+E+N+S, pady = 5)
        
        self.n_sVar= DoubleVar()
        self.n_sVar.trace("w", self.callback_NBodyTrace)
        self.n_s = Entry(self.Cosmo_Parms_group, textvariable=self.n_sVar, width=10)
        self.n_s.grid(row=2, column=5, sticky= W+E+N+S, pady = 5)

        #------------------------------
        self.RunSeting_group = LabelFrame(self.NewRun_page, text = "Run Setting")
        self.RunSeting_group.grid(row = 2, column = 0, columnspan = 6, sticky = W+E+N+S)
        Grid.rowconfigure(self.NewRun_page, 2, weight=0)
        

        for x in range(13):
            Grid.columnconfigure(self.RunSeting_group, x, weight=2)

        for y in range(4):
            Grid.rowconfigure(self.RunSeting_group, y, weight=2)
        
        self.Start_Redshift_label = Label(self.RunSeting_group, text=u"Start Redshift", image = zi_photo)
        self.Start_Redshift_label.photo = zi_photo
        self.Start_Redshift_label.grid(row=0, column=0, sticky= W)
        
        self.Strt_Redshift_Var = DoubleVar()
        self.Strt_Redshift_Var.trace("w", self.Calc_Redshift)
        #self.Strt_Redshift_Var.trace("w", self.callback_NBodyTrace)
        self.Strt_Redshift = Entry(self.RunSeting_group, textvariable=self.Strt_Redshift_Var, width=10)
        self.Strt_Redshift.grid(row=0, column=1, sticky= W)
        
        self.End_Redshift_label = Label(self.RunSeting_group, text=u"End Redshift", image = zf_photo)
        self.End_Redshift_label.photo = zf_photo
        self.End_Redshift_label.grid(row=0, column=2, sticky= W)

        self.End_RedshiftVar = DoubleVar()
        self.End_RedshiftVar.trace("w", self.Calc_Redshift)
        self.End_Redshift = Entry(self.RunSeting_group, textvariable=self.End_RedshiftVar, width=10)
        self.End_Redshift.grid(row=0, column=3, sticky= W)
        
        Label(self.RunSeting_group, text=u"Snaps Number").grid(row=0, column=4, sticky= W)
        self.Snaps_NumVar = IntVar()
        self.Snaps_NumVar.trace("w", self.Calc_Redshift)
        self.Snaps_Num = Entry(self.RunSeting_group, textvariable=self.Snaps_NumVar, width=10)
        self.Snaps_Num.grid(row=0, column=5, sticky= W)
        
        self.Calc_Redshift_label = Label(self.RunSeting_group, text=u"Calculate Redshift", image = zcalc_photo)
        self.Calc_Redshift_label.photo = zcalc_photo
        self.Calc_Redshift_label.grid(row=0, column=6, sticky= W)

        self.Redshift_list = ('-')
        self.Redshift_listVar = DoubleVar()
        self.Redshift_listVar.trace("w", self.callback_NBodyTrace)
        self.Redshift_listOpt = OptionMenu(self.RunSeting_group, self.Redshift_listVar, *self.Redshift_list)
        self.Redshift_listOpt.grid(row = 0, column = 7, pady = 5)
        self.Redshift_listVar.set(u'Select')

        #--------------------------------------
        self.Model_Selct_group = LabelFrame(self.NewRun_page, text = "Model Selection")
        self.Model_Selct_group.grid(row = 3, column = 0, columnspan = 6, sticky = W+E+N+S)

        for x in range(13):
            Grid.columnconfigure(self.Model_Selct_group, x, weight=2)
#        for y in range(4):
#            Grid.rowconfigure(self.Model_Selct_group, y, weight=2)

        self.Cosmo_Models = ['LCDM', 'LCDM + f_NL', 'wCDM', 'qCDM', 'Gamma wCDM', 'Gamma qCDM', 'f(R)']
        self.Model_Params_Var = StringVar()
        self.ModelOpt = OptionMenu(self.Model_Selct_group, self.Model_Params_Var, *self.Cosmo_Models, command = self.CosmoModelParm_Select)
        self.ModelOpt.grid(column = 0, row = 0, pady = 5, columnspan = 2, sticky = W+E+N+S)
        self.ModelOpt.config(width=15)
        self.Model_Params_Var.set(u'Select')
        
        self.w_x_label = Label(self.Model_Selct_group, text="w_x", image = w_x_photo)
        self.w_x_label.photo = w_x_photo
        self.w_x_label.grid(row=1, column=0, sticky= W+E+N+S)
        
        self.w_x_Var= DoubleVar()
        self.w_x_Var.trace("w", self.Calc_Redshift)
        self.w_x = Entry(self.Model_Selct_group, textvariable=self.w_x_Var, width=10)
        self.w_x.grid(row=1, column=1, sticky= W+E+N+S)
        
        self.cs2_label = Label(self.Model_Selct_group, text="cs2", image = cs2_photo)
        self.cs2_label.photo = cs2_photo
        self.cs2_label.grid(row=1, column=2, sticky= W+E+N+S)
        
        self.cs2_Var= DoubleVar()
        self.cs2_Var.trace("w", self.Calc_Redshift)
        self.cs2 = Entry(self.Model_Selct_group, textvariable=self.cs2_Var, width=10)
        self.cs2.grid(row=1, column=3, sticky= W+E+N+S)

        self.phi_0_label = Label(self.Model_Selct_group, text="phi_0", image = phi_0_photo)
        self.phi_0_label.photo = phi_0_photo
        self.phi_0_label.grid(row=1, column=4, sticky= W+E+N+S)
        
        self.phi_0_Var= DoubleVar()
        self.phi_0 = Entry(self.Model_Selct_group, textvariable = self.phi_0_Var, width=10)
        self.phi_0.grid(row=1, column=5, sticky= W+E+N+S)

        self.Gamma_label = Label(self.Model_Selct_group, text="Gamma", image = Gamma_photo)
        self.Gamma_label.photo = Gamma_photo
        self.Gamma_label.grid(row=1, column=6, sticky= W+E+N+S)
        
        self.GammaVar= DoubleVar()
        self.Gamma= Entry(self.Model_Selct_group, textvariable=self.GammaVar, width=10)
        self.Gamma.grid(row=1, column=7, sticky= W+E+N+S)
        
        
        self.f_NL_label = Label(self.Model_Selct_group, text="f_NL", image = f_NL_photo)
        self.f_NL_label.photo = f_NL_photo
        self.f_NL_label.grid(row=2, column=0, sticky= W+E+N+S)
        
        self.f_NL_Var= DoubleVar()
        self.f_NL_Var.trace("w", self.callback_NBodyTrace)
        self.f_NL= Entry(self.Model_Selct_group, textvariable=self.f_NL_Var, width=10)
        self.f_NL.grid(row=2, column=1, sticky= W+E+N+S)


        #--------------------------------------
        self.Codes_Compile_nb = ttk.Notebook(self.Codes_Compile_page,  padding = -5)
        self.CAMB_page = ttk.Frame(self.Codes_Compile_nb); self.NGenIC_page = ttk.Frame(self.Codes_Compile_nb)
        self.Gadget2_page = ttk.Frame(self.Codes_Compile_nb)
        self.AHF_page = ttk.Frame(self.Codes_Compile_nb); self.POWMS_page = ttk.Frame(self.Codes_Compile_nb)
        #------------------------
        self.Codes_Compile_nb.add(self.CAMB_page, text='CAMB')
        
        self.Codes_Compile_nb.add(self.NGenIC_page, text='N-GenIC')
        self.Codes_Compile_nb.add(self.Gadget2_page, text='Gadget 2')
        
        self.Codes_Compile_nb.add(self.AHF_page, text='AHF')
        self.Codes_Compile_nb.add(self.POWMS_page, text='POWMS')
        
        self.Codes_Compile_nb.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S, pady = 1)
        self.Codes_Compile_nb.pack(side="top", fill="both", expand=True)
        
        # CAMB Make Options:-----------
        self.CAMB_MakeOptions_frame =  VSF.VerticalScrolledFrame(self.CAMB_page)
        self.CAMB_MakeOptions_frame.pack(side="top", fill="both", expand=True)
        
        for x in range(6):
            Grid.columnconfigure(self.CAMB_MakeOptions_frame.interior, x, weight=2)
        
        self.CAMB_SourceCode_Dirct = LabelFrame(self.CAMB_MakeOptions_frame.interior, text = "Source Code Directory")
        self.CAMB_SourceCode_Dirct.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        Label(self.CAMB_SourceCode_Dirct, text="Choose").grid(row=0, column=0, sticky= W+E+N+S)
        self.CAMB_Dirct_Var = StringVar()
        self.CAMB_Dirct= Entry(self.CAMB_SourceCode_Dirct, textvariable=self.CAMB_Dirct_Var, width = 60)
        self.CAMB_Dirct.grid(row=0, column=1, sticky= W)
        self.CAMB_Dirct.bind("<Button-1>", self.CAMB_Directory)
        
        # N-GenIC Make Options:-----------
        self.N_GenIC_MakeOptions_frame =  VSF.VerticalScrolledFrame(self.NGenIC_page)
        self.N_GenIC_MakeOptions_frame.pack(side="top", fill="both", expand=True)
        
        for x in range(6):
            Grid.columnconfigure(self.N_GenIC_MakeOptions_frame.interior, x, weight=2)
        
        self.NGenIC_SourceCode_Dirct = LabelFrame(self.N_GenIC_MakeOptions_frame.interior, text = "Source Code Directory")
        self.NGenIC_SourceCode_Dirct.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        Label(self.NGenIC_SourceCode_Dirct, text="Choose").grid(row=0, column=0, sticky= W+E+N+S)
        self.NGenIC_Dirct_Var = StringVar()
        self.NGenIC_Dirct= Entry(self.NGenIC_SourceCode_Dirct, textvariable=self.NGenIC_Dirct_Var, width = 60)
        self.NGenIC_Dirct.grid(row=0, column=1, sticky= W)
        self.NGenIC_Dirct.bind("<Button-1>", self.N_GenIC_Directory)

        self.N_GenIC_MakeOptions_group = LabelFrame(self.N_GenIC_MakeOptions_frame.interior,  text = "N-GenIC MakeOptions")
        self.N_GenIC_MakeOptions_group.grid(row = 1, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        #-------------
        self.N_GenIC_MakeOptions_listVar = [MkDt.N_GenIC_MakeOptions.values()[i] + '_Var' for i in range(len(MkDt.N_GenIC_MakeOptions))]
        self.N_GenIC_MakeOptions_CheckButton = [MkDt.N_GenIC_MakeOptions.values()[i] + '_Entry' for i in range(len(MkDt.N_GenIC_MakeOptions))]
        for i in range(len(MkDt.N_GenIC_MakeOptions)):
            self.N_GenIC_MakeOptions_listVar[i] = StringVar()
            self.N_GenIC_MakeOptions_CheckButton[i] = Checkbutton(self.N_GenIC_MakeOptions_group, text= MkDt.N_GenIC_MakeOptions.values()[i], variable = self.N_GenIC_MakeOptions_listVar[i], onvalue = MkDt.N_GenIC_MakeOptions.values()[i], offvalue = "")
            self.N_GenIC_MakeOptions_CheckButton[i].grid(row=i,  column=0, sticky= W)
            Tooltip.ToolTip(self.N_GenIC_MakeOptions_CheckButton[i], follow_mouse = 1, text = TtDt.N_GenIC_make_tooltip.values()[i], wraplength = 500)


        # Gadget 2 Make Options:-----------
        self.Gadget2_MakeOptions_frame =  VSF.VerticalScrolledFrame(self.Gadget2_page)
        self.Gadget2_MakeOptions_frame.pack(side="top", fill="both", expand=True)
        
        for x in range(6):
            Grid.columnconfigure(self.Gadget2_MakeOptions_frame.interior, x, weight=2)
        
        self.Gadget2_SourceCode_Dirct = LabelFrame(self.Gadget2_MakeOptions_frame.interior, text = "Source Code Directory")
        self.Gadget2_SourceCode_Dirct.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        Label(self.Gadget2_SourceCode_Dirct, text="Choose").grid(row=0, column=0, sticky= W+E+N+S)
        self.Gadget2_Dirct_Var = StringVar()
        self.Gadget2_Dirct= Entry(self.Gadget2_SourceCode_Dirct, textvariable=self.Gadget2_Dirct_Var, width = 60)
        self.Gadget2_Dirct.grid(row=0, column=1, sticky= W)
        self.Gadget2_Dirct.bind("<Button-1>", self.Gadget2_Directory)
        
        self.Gadget2_MakeOptions_group = LabelFrame(self.Gadget2_MakeOptions_frame.interior,  text = "Gadget2 MakeOptions")
        self.Gadget2_MakeOptions_group.grid(row = 1, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        #-------------
        self.Gadget_MakeOptions_listVar = [MkDt.Gadget_MakeOptions.values()[i] + '_Var' for i in range(len(MkDt.Gadget_MakeOptions))]
        self.Gadget_MakeOptions_CheckButton = [MkDt.Gadget_MakeOptions.values()[i] + '_Entry' for i in range(len(MkDt.Gadget_MakeOptions))]
        for i in range(len(MkDt.Gadget_MakeOptions)):
            self.Gadget_MakeOptions_listVar[i] = StringVar()
            self.Gadget_MakeOptions_CheckButton[i] = Checkbutton(self.Gadget2_MakeOptions_group, text= MkDt.Gadget_MakeOptions.values()[i], variable = self.Gadget_MakeOptions_listVar[i], onvalue = MkDt.Gadget_MakeOptions.values()[i], offvalue = "")
            self.Gadget_MakeOptions_CheckButton[i].grid(row=i,  column=0, sticky= W)
            Tooltip.ToolTip(self.Gadget_MakeOptions_CheckButton[i], follow_mouse = 1, text = TtDt.gadget_make_tooltip.values()[i], wraplength = 500)
        
        # AHF Make Options:-----------
        self.AHF_MakeOptions_frame =  VSF.VerticalScrolledFrame(self.AHF_page)
        self.AHF_MakeOptions_frame.pack(side="top", fill="both", expand=True)

        for x in range(6):
            Grid.columnconfigure(self.AHF_MakeOptions_frame.interior, x, weight=2)
        
        self.AHF_SourceCode_Dirct = LabelFrame(self.AHF_MakeOptions_frame.interior, text = "Source Code Directory")
        self.AHF_SourceCode_Dirct.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        Label(self.AHF_SourceCode_Dirct, text="Choose").grid(row=0, column=0, sticky= W+E+N+S)
        self.AHF_Dirct_Var = StringVar()
        self.AHF_Dirct= Entry(self.AHF_SourceCode_Dirct, textvariable=self.AHF_Dirct_Var, width = 60)
        self.AHF_Dirct.grid(row=0, column=1, sticky= W)
        self.AHF_Dirct.bind("<Button-1>", self.AHF_Directory)
        
        self.AHF_MakeOptions_group = LabelFrame(self.AHF_MakeOptions_frame.interior,  text = "AHF MakeOptions")
        self.AHF_MakeOptions_group.grid(row = 1, column = 0, columnspan = 6 , sticky = W+E+N+S)
        
        #-------------
        self.AHF_MakeOptions_listVar = [MkDt.AHF_MakeOptions.values()[i] + '_Var' for i in range(len(MkDt.AHF_MakeOptions))]
        self.AHF_MakeOptions_CheckButton = [MkDt.AHF_MakeOptions.values()[i] + '_Entry' for i in range(len(MkDt.AHF_MakeOptions))]
        for i in range(len(MkDt.AHF_MakeOptions)):
            self.AHF_MakeOptions_listVar[i] = StringVar()
            self.AHF_MakeOptions_CheckButton[i] = Checkbutton(self.AHF_MakeOptions_group, text= MkDt.AHF_MakeOptions.values()[i], variable = self.AHF_MakeOptions_listVar[i], onvalue = MkDt.AHF_MakeOptions.values()[i], offvalue = "")
            self.AHF_MakeOptions_CheckButton[i].grid(row=i,  column=0, sticky= W)
            #Tooltip.ToolTip(self.AHF_MakeOptions_CheckButton[i], follow_mouse = 1, text = TtDt.AHF_make_tooltip.values()[i], wraplength = 500)
        
        # POWMS Make Options:-----------
        self.POWMS_MakeOptions_frame =  VSF.VerticalScrolledFrame(self.POWMS_page)
        self.POWMS_MakeOptions_frame.pack(side="top", fill="both", expand=True)
        
        for x in range(6):
            Grid.columnconfigure(self.POWMS_MakeOptions_frame.interior, x, weight=2)
        
        self.POWMS_SourceCode_Dirct = LabelFrame(self.POWMS_MakeOptions_frame.interior, text = "Source Code Directory")
        self.POWMS_SourceCode_Dirct.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        Label(self.POWMS_SourceCode_Dirct, text="Choose").grid(row=0, column=0, sticky= W+E+N+S)
        self.POWMS_Dirct_Var = StringVar()
        self.POWMS_Dirct= Entry(self.POWMS_SourceCode_Dirct, textvariable=self.POWMS_Dirct_Var, width = 60)
        self.POWMS_Dirct.grid(row=0, column=1, sticky= W)
        self.POWMS_Dirct.bind("<Button-1>", self.POWMS_Directory)
        
        
        #--------------------------------------
        self.Run_Specif_nb = ttk.Notebook(self.Run_Specif_page,  padding = -5)
        self.PertCosm_page = ttk.Frame(self.Run_Specif_nb); self.NBody_page = ttk.Frame(self.Run_Specif_nb); self.toolbox_page = ttk.Frame(self.Run_Specif_nb)
        #------------------------
        self.Run_Specif_nb.add(self.PertCosm_page, text='Perturbative Cosmology (linear)')
        self.Run_Specif_nb.add(self.NBody_page, text='N-Body Simulation (non-linear)')
        self.Run_Specif_nb.add(self.toolbox_page, text='Toolbox & Analysis')
        
        self.Run_Specif_nb.pack(side="top", fill="both", expand=True)

        # Perturbative Cosmology  Page :--------
        self.PertCosm_frame =  VSF.VerticalScrolledFrame(self.PertCosm_page)
        self.PertCosm_frame.pack(side="top", fill="both", expand=True)
        
        for x in range(6):
            Grid.columnconfigure(self.PertCosm_frame.interior, x, weight=2)
        # CAMB :----------
        self.CAMB_Parms_group = LabelFrame(self.PertCosm_frame.interior, text = "CAMB", width = 50)
        self.CAMB_Parms_group.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        self.CAMB_Parms_listVar = OrderedDict([]); self.CAMB_Parms_Entry = OrderedDict([])
        for i in range(len(PrDt.CAMB_Parms_dict)):
            self.CAMB_Parms_listVar[PrDt.CAMB_Parms_dict.keys()[i]] = PrDt.CAMB_Parms_dict.keys()[i] + '_Var'
            self.CAMB_Parms_Entry[PrDt.CAMB_Parms_dict.keys()[i]] = PrDt.CAMB_Parms_dict.keys()[i] + '_Entry'
        
        for i in range(len(PrDt.CAMB_Parms_dict)):
            self.CAMB_Parms_listVar[PrDt.CAMB_Parms_dict.keys()[i]] = StringVar()
            Label(self.CAMB_Parms_group, text = PrDt.CAMB_Parms_dict.keys()[i]).grid(column = 0, row = i, pady = 5, sticky = W)
            self.CAMB_Parms_Entry[PrDt.CAMB_Parms_dict.keys()[i]] = Entry(self.CAMB_Parms_group, textvariable=self.CAMB_Parms_listVar[PrDt.CAMB_Parms_dict.keys()[i]], width=30)
            self.CAMB_Parms_Entry[PrDt.CAMB_Parms_dict.keys()[i]].grid(column = 1, row = i, pady = 5, sticky = W+E+N+S)
            self.CAMB_Parms_listVar[PrDt.CAMB_Parms_dict.keys()[i]].set(PrDt.CAMB_Parms_dict.values()[i])


        # N-Body Page :-------------------------
        for x in range(13):
            Grid.columnconfigure(self.NBody_page, x, weight=2)
        for y in range(4):
            Grid.rowconfigure(self.NBody_page, y, weight=2)
        
        self.NBodyParms_group = LabelFrame(self.NBody_page, text = "N-Body Parameters")
        self.NBodyParms_group.grid(row = 0, column = 0, columnspan =13 ,sticky = W+E+N+S)

        for x in range(8):
            Grid.columnconfigure(self.NBodyParms_group, x, weight=2)
        
        # N-Body Simulation Parameters :------- !!
        Label(self.NBodyParms_group, text="Box Size").grid(row=0, column=0, sticky= W)
        self.Box_SizeVar =  IntVar()
        self.Box_SizeVar.trace("w", self.callback_NBodyTrace)
        self.Box_Size = Entry(self.NBodyParms_group, textvariable=self.Box_SizeVar, width=10)
        self.Box_Size.grid(row = 0, column = 1, sticky = W+E+N+S)
        self.Box_Size.bind("<Return>", self.callback_Update_Entry)
        Tooltip.ToolTip(self.Box_Size, follow_mouse = 1, text = "Please Enter Box Size in Mpc units")

        Label(self.NBodyParms_group, text="N_part").grid(row=0, column=2, sticky= W)
        self.N_partVar= IntVar()
        self.N_partVar.trace("w", self.callback_NBodyTrace)
        self.N_partVar.trace("w", self.callback_MakeOptionsTrace)
        self.N_part= Entry(self.NBodyParms_group, textvariable=self.N_partVar, width=10)
        self.N_part.grid(row=0, column=3, sticky= W+E+N+S)
        Tooltip.ToolTip(self.N_part, follow_mouse=1, text="Please Enter Number of Particles^1/3")
        
        Label(self.NBodyParms_group, text="epsilon").grid(row=0, column=4, sticky= W)
        self.epsilonVar = DoubleVar()
        self.epsilonVar.trace("w", self.callback_NBodyTrace)
        self.epsilon= Entry(self.NBodyParms_group, textvariable=self.epsilonVar, width=10)
        self.epsilon.grid(row=0, column=5, sticky= W+E+N+S)
        self.epsilon.bind("<Button-1>", self.softining_length)
        Tooltip.ToolTip(self.epsilon, follow_mouse=1, text="Please Enter the Linkining length in Mpc units.")
        
        Label(self.NBodyParms_group, text="eta").grid(row=1, column=0, sticky= W)
        self.etaVar= DoubleVar()
        self.etaVar.trace("w", self.callback_NBodyTrace)
        self.eta= Entry(self.NBodyParms_group, textvariable=self.etaVar, width=10)
        self.eta.grid(row=1, column=1, sticky= W+E+N+S)

        self.Initial_Redshift_label = Label(self.NBodyParms_group, text=u"Initial Redshift")
        self.Initial_Redshift_label.grid(row=1, column=2, sticky= W)
        self.Init_Redshift_Var = DoubleVar()
        self.Init_Redshift_Var.trace("w", self.callback_NBodyTrace)
        self.Init_Redshift = Entry(self.NBodyParms_group, textvariable=self.Init_Redshift_Var, width=10)
        self.Init_Redshift.grid(row=1, column=3, sticky= W)
        
        self.Final_Redshift_label = Label(self.NBodyParms_group, text=u"Final Redshift")
        self.Final_Redshift_label.grid(row=1, column=4, sticky= W)
        self.Finl_RedshiftVar = DoubleVar()
        self.Finl_RedshiftVar.trace("w", self.callback_NBodyTrace)
        self.Finl_Redshift = Entry(self.NBodyParms_group, textvariable=self.Finl_RedshiftVar, width=10)
        self.Finl_Redshift.grid(row=1, column=5, sticky= W)

        #----------------------
        self.AdvancedParms_group = LabelFrame(self.NBody_page, text = "Advanced Parameter Settings")
        self.AdvancedParms_group.grid(row = 1, column = 0, rowspan = 10, columnspan =13, sticky = W+E+N+S)

        for x in range(8):
            Grid.columnconfigure(self.AdvancedParms_group, x, weight=2)
        
        self.AdvancedParms_frame =  VSF.VerticalScrolledFrame(self.AdvancedParms_group)
        self.AdvancedParms_frame.pack(side="top", fill="both", expand=True)

        # N-GenIC :----------
        self.NGenIC_group = LabelFrame(self.AdvancedParms_frame.interior, text = "N-GenIC", fg = 'red', width = 50)
        self.NGenIC_group.grid(row = 0, column = 0, sticky = W+E+N+S)
        
        self.NGenIC_listVar = OrderedDict([]); self.NGenIC_Entry = OrderedDict([])
        for i in range(len(PrDt.NGenIC_dict)):
            self.NGenIC_listVar[PrDt.Gadget2_dict.keys()[i]] = PrDt.NGenIC_dict.keys()[i] + '_Var'
            self.NGenIC_Entry[PrDt.NGenIC_dict.keys()[i]] = PrDt.NGenIC_dict.keys()[i] + '_Entry'

        for i in range(len(PrDt.NGenIC_dict)):
            self.NGenIC_listVar[PrDt.NGenIC_dict.keys()[i]] = StringVar()
            Label(self.NGenIC_group, text = PrDt.NGenIC_dict.keys()[i]).grid(column = 0, row = i, pady = 5, sticky = W)
            self.NGenIC_Entry[PrDt.NGenIC_dict.keys()[i]] = Entry(self.NGenIC_group, textvariable=self.NGenIC_listVar[PrDt.NGenIC_dict.keys()[i]], width=30)
            self.NGenIC_Entry[PrDt.NGenIC_dict.keys()[i]].grid(column = 1, row = i, pady = 5, sticky = W+E+N+S)
            self.NGenIC_listVar[PrDt.NGenIC_dict.keys()[i]].set(PrDt.NGenIC_dict.values()[i])

        # Gadget2 :----------
        self.Gadget2_group = LabelFrame(self.AdvancedParms_frame.interior, text = "Gadget 2", fg = 'red', width = 50)
        self.Gadget2_group.grid(row = 1, column = 0, sticky = W+E+N+S)
        
        self.Gadget2_listVar = OrderedDict([]); self.Gadget2_Entry = OrderedDict([])
        for i in range(len(PrDt.Gadget2_dict)):
            self.Gadget2_listVar[PrDt.Gadget2_dict.keys()[i]] = PrDt.Gadget2_dict.keys()[i] + '_Var'
            self.Gadget2_Entry[PrDt.Gadget2_dict.keys()[i]] = PrDt.Gadget2_dict.keys()[i] + '_Entry'

        for i in range(len(PrDt.Gadget2_dict)):
            self.Gadget2_listVar[PrDt.Gadget2_dict.keys()[i]] = StringVar()
            Label(self.Gadget2_group, text = PrDt.Gadget2_dict.keys()[i]).grid(column = 0, row = i, pady = 5, sticky = W)
            self.Gadget2_Entry[PrDt.Gadget2_dict.keys()[i]] = Entry(self.Gadget2_group, textvariable=self.Gadget2_listVar[PrDt.Gadget2_dict.keys()[i]], width=30)
            self.Gadget2_Entry[PrDt.Gadget2_dict.keys()[i]].grid(column = 1, row = i, pady = 5, sticky = W+E+N+S)
            self.Gadget2_listVar[PrDt.Gadget2_dict.keys()[i]].set(PrDt.Gadget2_dict.values()[i])

        # Toolbox page :-----------------------
        self.Toolbox_frame =  VSF.VerticalScrolledFrame(self.toolbox_page)
        self.Toolbox_frame.pack(side="top", fill="both", expand=True)

        for x in range(6):
                Grid.columnconfigure(self.Toolbox_frame.interior, x, weight=2)
        # AHF :----------
        self.AHF_group = LabelFrame(self.Toolbox_frame.interior, text = "AHF", fg = 'red', width = 50)
        self.AHF_group.grid(row = 0, column = 0, columnspan = 6, sticky = W+E+N+S)

        self.AHF_listVar = OrderedDict([]); self.AHF_Entry = OrderedDict([])
        for i in range(len(PrDt.AHF_dict)):
            self.AHF_listVar[PrDt.AHF_dict.keys()[i]] = PrDt.AHF_dict.keys()[i] + '_Var'
            self.AHF_Entry[PrDt.AHF_dict.keys()[i]] = PrDt.AHF_dict.keys()[i] + '_Entry'
        
        for i in range(len(PrDt.AHF_dict)):
            self.AHF_listVar[PrDt.AHF_dict.keys()[i]] = StringVar()
            Label(self.AHF_group, text = PrDt.AHF_dict.keys()[i]).grid(column = 0, row = i, pady = 5, sticky = W)
            self.AHF_Entry[PrDt.AHF_dict.keys()[i]] = Entry(self.AHF_group, textvariable=self.AHF_listVar[PrDt.AHF_dict.keys()[i]], width=30)
            self.AHF_Entry[PrDt.AHF_dict.keys()[i]].grid(column = 1, row = i, pady = 5, sticky = W+E+N+S)
            self.AHF_listVar[PrDt.AHF_dict.keys()[i]].set(PrDt.AHF_dict.values()[i])

        self.AHF_Entry['[AHF] #'].grid_forget(); self.AHF_Entry['[GADGET] #'].grid_forget()
        self.AHF_Entry['[TIPSY] #'].grid_forget(); self.AHF_Entry['[ART] #'].grid_forget()

        # POWMS :----------
        self.POWMS_group = LabelFrame(self.Toolbox_frame.interior, text = "POWMS", fg = 'red', width = 50)
        self.POWMS_group.grid(row = 1, column = 0, columnspan = 6, sticky = W+E+N+S)
        
        self.POWMS_listVar = OrderedDict([]); self.POWMS_Entry = OrderedDict([])
        for i in range(len(PrDt.POWMS_dict)):
            self.POWMS_listVar[PrDt.POWMS_dict.keys()[i]] = PrDt.POWMS_dict.keys()[i] + '_Var'
            self.POWMS_Entry[PrDt.POWMS_dict.keys()[i]] = PrDt.POWMS_dict.keys()[i] + '_Entry'
        
        for i in range(len(PrDt.POWMS_dict)):
            self.POWMS_listVar[PrDt.POWMS_dict.keys()[i]] = StringVar()
            Label(self.POWMS_group, text = PrDt.POWMS_dict.keys()[i]).grid(column = 0, row = i, pady = 5, sticky = W)
            self.POWMS_Entry[PrDt.POWMS_dict.keys()[i]] = Entry(self.POWMS_group, textvariable=self.POWMS_listVar[PrDt.POWMS_dict.keys()[i]], width=30)
            self.POWMS_Entry[PrDt.POWMS_dict.keys()[i]].grid(column = 1, row = i, pady = 5, sticky = W+E+N+S)
            self.POWMS_listVar[PrDt.POWMS_dict.keys()[i]].set(PrDt.POWMS_dict.values()[i])

        self.POWMS_Entry['&input !'].grid_forget(); self.POWMS_Entry['/ !'].grid_forget()
        #------------------------
        self.Control_Frame = Frame(page, bg="white smoke", bd= 1, relief= RIDGE)
        self.Control_Frame.grid(row = 4, column = 0, rowspan = 1, sticky = W+E+N+S)

        for x in range(4):
            Grid.columnconfigure(self.Control_Frame, x, weight=2)
        for y in range(2):
            Grid.rowconfigure(self.Control_Frame, y, weight=2)

        self.Simulation_Run = Button(self.Control_Frame, text = u"QSub", foreground = 'red', command = self.QSub_Run)
        self.Simulation_Run.grid(column = 1, row = 0, pady = 5, sticky= W+E+N+S)

        self.QStat = Button(self.Control_Frame, text = u"QStat", command =self.callback_QStat)
        self.QStat.grid(column = 2, row = 0, sticky= W+E+N+S, pady = 5)

        self.clear_button = Button(self.Control_Frame, text="QDel", command= self.callback_QDel)
        self.clear_button.grid(column = 3, row = 0, sticky = W+E+N+S, pady = 5)

        self.QJob_Var = StringVar()
        self.QJob_Entry = Entry(self.Control_Frame, textvariable = self.QJob_Var, foreground = 'red')
        self.QJob_Entry.grid(column = 4, row = 0, sticky = W+E+N+S, pady = 5)

        #-----------------------------------
        self.Jobs_List_group = LabelFrame(self.Control_Frame, text = "Jobs List")
        self.Jobs_List_group.grid(row = 0, column = 0, rowspan = 2, columnspan = 1, sticky = W+E+N+S)
        Grid.columnconfigure(self.Jobs_List_group, 0, weight=2);Grid.rowconfigure(self.Jobs_List_group, 0, weight=2)

        self.Jobs_List_Lb = Listbox(self.Jobs_List_group, selectmode = EXTENDED, bg = "white smoke")
        self.Jobs_List_Lb.grid(row = 0, column = 0, sticky = W+E+N+S)

        self.list = OrderedDict([("N-Body Simulation", ['CAMB', 'N-GenIC', 'Gadget2']), ("+AHF", None), ("+POWMS", None) ])
        
        for i in range(len(self.list)):
            self.Jobs_List_Lb.insert(END, self.list.keys()[i])

        self.Jobs_List_Lb.itemconfig(0, {'fg':'red'})
        self.Jobs_List_Lb.itemconfig(1, {'fg':'blue'})
        self.Jobs_List_Lb.itemconfig(2, {'fg':'blue'})

        self.Running_Jobs_group = LabelFrame(self.Control_Frame, text = "Runing Jobs")
        self.Running_Jobs_group.grid(row = 1, column = 1, rowspan = 1, columnspan = 8, sticky = W+E+N+S)
        Grid.columnconfigure(self.Running_Jobs_group, 0, weight=2);Grid.rowconfigure(self.Running_Jobs_group, 0, weight=2)

        self.Running_Jobs_Lb = Listbox(self.Running_Jobs_group, selectmode = EXTENDED, bg = "white smoke")
        self.Running_Jobs_Lb.grid(row = 0, column = 0, sticky = W+E+N+S, columnspan = 8)
        
        def Job_add(event, test):
            w = event.widget
            index = int(w.curselection()[0])
            self.Running_Jobs_Lb.insert(END, test[test.keys()[index]])
            for i in range(len(test[test.keys()[index]])):
                self.Run_Creat(test[test.keys()[index]][i])

        def Job_remove(event, test):
            w = event.widget
            index = int(w.curselection()[0])
            self.Running_Jobs_Lb.delete(ANCHOR)
            for i in range(len(test[test.keys()[index]])):
                self.Run_Delete(test[test.keys()[index]][i])

        self.Jobs_List_Lb.bind('<Double-Button-1>', lambda event: Job_add(event, self.list))
        self.Running_Jobs_Lb.bind('<Double-Button-1>', lambda event: Job_remove(event, self.list))
            
    #----------------------------------------------------------
    def callback_codes(self):
        self.main_nb.select(self.Main_page); self.NewRun_nb.select(self.Codes_Compile_page)
    
    def func(self, value):
        pages = {'CAMB': self.CAMB_page, 'N-GenIC': self.NGenIC_page, 'Gadget2': self.Gadget2_page, 'AHF': self.AHF_page, 'POWMS': self.POWMS_page}
        self.Codes_Compile_nb.select(pages[value])
    
    def callback_new_run(self):
        self.main_nb.select(self.Main_page); self.NewRun_nb.select(self.NewRun_page)
    
    def callback_RunSpicf(self):
        self.main_nb.select(self.Main_page); self.NewRun_nb.select(self.Run_Specif_page)

    def runfunc(self, value):
        pages = {'Perturbative Cosmology': self.PertCosm_page, 'N-Body Simulation': self.NBody_page}
        self.Run_Specif_nb.select(pages[value])

    def callback_Toolbox(self):
        self.main_nb.select(self.Main_page); self.NewRun_nb.select(self.Run_Specif_page); self.Run_Specif_nb.select(self.toolbox_page)
    
    def callback_sysPerf(self):
        self.main_nb.select(self.SysPerf_page)
    
    def callback_Home(self):
        self.main_nb.select(self.Anals_page)
    
    def callback_terminal(self):
        self.TermInfo_nb.select(self.Term_page)
    
    def callback_info(self):
        self.TermInfo_nb.select(self.Info_page)
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, self.Welcome_str)
    
    def callback_log(self):
        self.TermInfo_nb.select(self.Info_page)
        self.text_area.delete(1.0, END)
    
    def callback_run_network_mode(self,event):
        if self.run_mode_logic == "local":
            self.run_mode.configure(image=self.run_mode_network_photo)
            self.RemoteDirt_label.grid(row=1, column=0, sticky= W); self.RemoteDirct.grid(row=1, column=1, sticky= W+E+N+S)
            
            # SSH :---------
            self.transport = paramiko.Transport((str(self.Host_Server_Var.get()), self.Host_Port_Var.get()))
            self.client = paramiko.SSHClient()
            self.transport.connect(username = str(self.UserName_Var.get()), password = str(self.PassWord_Var.get()))
            self.client.load_system_host_keys()
            self.client.connect(str(self.Host_Server_Var.get()), username = str(self.UserName_Var.get()), password = str(self.PassWord_Var.get()))
            # sftp :---------
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            # Directory defination :-----
            self.remote_dirct = self.client.exec_command('pwd')[1].read().strip()
            self.Remote_DirtVar.set(self.remote_dirct)
            self.run_mode_logic = "network"

        elif self.run_mode_logic == "network":
            self.run_mode.configure(image=self.run_mode_local_photo)
            self.RemoteDirt_label.grid_forget(); self.RemoteDirct.grid_forget()
            
            # Close ssh :--------
            self.sftp.close()
            self.transport.close()
            self.client.close()
            self.run_mode_logic = "local"

    def callback_QStat(self):
        stdin, stdout, stderr = self.client.exec_command('qstat -u ' + self.UserName_Var.get())
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, stdout.read())
    
    def callback_QDel(self):
        stdin, stdout, stderr = self.client.exec_command('qdel ' + self.QJob_Var.get())
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, stdout.read())
        self.callback_QStat()


    #-----------------------------------------------------------
    def openDirectory(self, event):
        self.dirname = tkFileDialog.askdirectory(parent=root, initialdir='/Users/mahmoud/', title=self.dirtext)
        self.DirtVar.set(self.dirname)
    
    def CAMB_Directory(self, event):
        if self.run_mode_logic == "local":
            self.CAMB_dirname = tkFileDialog.askdirectory(parent=root, initialdir='/Users/mahmoud/', title=self.dirtext)
            self.CAMB_Dirct_Var.set(self.CAMB_dirname)
        else:
            self.CAMB_Dirct_Var.set(self.remote_dirct)
    
    def N_GenIC_Directory(self, event):
        if self.run_mode_logic == "local":
            self.N_GenIC_dirname = tkFileDialog.askdirectory(parent=root, initialdir='/Users/mahmoud/', title=self.dirtext)
            self.NGenIC_Dirct_Var.set(self.N_GenIC_dirname)
        else:
            self.NGenIC_Dirct_Var.set(self.remote_dirct)

    def Gadget2_Directory(self, event):
        if self.run_mode_logic == "local":
            self.gadget2_dirname = tkFileDialog.askdirectory(parent=root, initialdir='/Users/mahmoud/', title=self.dirtext)
            self.Gadget2_Dirct_Var.set(self.gadget2_dirname)
        else:
            self.Gadget2_Dirct_Var.set(self.remote_dirct)

    def AHF_Directory(self, event):
        if self.run_mode_logic == "local":
            self.AHF_dirname = tkFileDialog.askdirectory(parent=root, initialdir='/Users/mahmoud/', title=self.dirtext)
            self.AHF_Dirct_Var.set(self.AHF_dirname)
        else:
            self.AHF_Dirct_Var.set(self.remote_dirct)

    def POWMS_Directory(self, event):
        if self.run_mode_logic == "local":
            self.POWMS_dirname = tkFileDialog.askdirectory(parent=root, initialdir='/Users/mahmoud/', title=self.dirtext)
            self.POWMS_Dirct_Var.set(self.POWMS_dirname)
        else:
            self.POWMS_Dirct_Var.set(self.remote_dirct)

    def callback_Update_Entry(self, event):
        self.NGenIC_listVar[2].set(self.Box_SizeVar.get())

    def Update_Param_Dicts(self):
        CAMB_Params_Dict_update = OrderedDict([]); NGenIC_Params_Dict_update = OrderedDict([]); Gadget2_Params_Dict_update = OrderedDict([])
        AHF_Params_Dict_update = OrderedDict([]); POWMS_Params_Dict_update = OrderedDict([])
        for i in range(len(PrDt.CAMB_Parms_dict)):
            CAMB_Params_Dict_update[PrDt.CAMB_Parms_dict.keys()[i]] = self.CAMB_Parms_listVar[PrDt.CAMB_Parms_dict.keys()[i]].get()
        for i in range(len(PrDt.NGenIC_dict)):
            NGenIC_Params_Dict_update[PrDt.NGenIC_dict.keys()[i]] = self.NGenIC_listVar[PrDt.NGenIC_dict.keys()[i]].get()
        for i in range(len(PrDt.Gadget2_dict)):
            Gadget2_Params_Dict_update[PrDt.Gadget2_dict.keys()[i]] = self.Gadget2_listVar[PrDt.Gadget2_dict.keys()[i]].get()
        for i in range(len(PrDt.AHF_dict)):
            AHF_Params_Dict_update[PrDt.AHF_dict.keys()[i]] = self.AHF_listVar[PrDt.AHF_dict.keys()[i]].get()
        for i in range(len(PrDt.POWMS_dict)):
            POWMS_Params_Dict_update[PrDt.POWMS_dict.keys()[i]] = self.POWMS_listVar[PrDt.POWMS_dict.keys()[i]].get()

        Parsms_Dict_Dict = OrderedDict([('CAMB', CAMB_Params_Dict_update), ('N-GenIC', NGenIC_Params_Dict_update), ('Gadget2', Gadget2_Params_Dict_update),
                                        ('AHF_%s' %self.Redshift_listVar.get(), AHF_Params_Dict_update), ('POWMS_%s' %self.Redshift_listVar.get(), POWMS_Params_Dict_update)])
                                        
        return Parsms_Dict_Dict

    def Update_MakeOpts_Dicts(self):
    
        N_GenIC_OPT_str = ''; Gadget_OPT_str = ''
        for i in range(len(MkDt.N_GenIC_MakeOptions)):
            N_GenIC_OPT_str += self.N_GenIC_MakeOptions_listVar[i].get() + ' '
        
        for i in range(len(MkDt.Gadget_MakeOptions)):
            Gadget_OPT_str += self.Gadget_MakeOptions_listVar[i].get() + ' '
        
        MkDt.N_GenIC_make_dict['OPT = '] = N_GenIC_OPT_str; MkDt.gadget_make_dict['OPT =  '] = Gadget_OPT_str
        
        x = main(self.DirtVar.get(), self.Run_nameVar.get())
        if self.run_mode_logic != "local":
            xx = main(self.Remote_DirtVar.get(), self.Run_nameVar.get())
            MkDt.N_GenIC_make_dict['EXEC = '] = xx.loc_Exc + 'N-GenIC'
            MkDt.gadget_make_dict['EXEC   =  '] = xx.loc_Exc + 'Gadget2'
        else:
            MkDt.N_GenIC_make_dict['EXEC = '] = x.loc_Exc + 'N-GenIC'
            MkDt.gadget_make_dict['EXEC   =  '] = x.loc_Exc + 'Gadget2'
        
        Sys_keys = ['CC = ', 'OPTIMIZE = ', 'GSL_INCL = ', 'GSL_LIBS = ', 'FFTW_INCL = ', 'FFTW_LIBS = ', 'MPICHLIB = ', 'HDF5INCL = ', 'HDF5LIB = ']
        for i in range(len(Sys_keys)):
            MkDt.gadget_make_dict[Sys_keys[i]] = self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].get()
            MkDt.N_GenIC_make_dict[Sys_keys[i]] = self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].get()
        
        #--- write param.h for AHF !!
        PrDt.param_h_file_dict['#define H0 '] = self.H_0Var.get() * 100; PrDt.param_h_file_dict['#define cH0 '] = 299800.0/(self.H_0Var.get() * 100)

        MakeOpts_Dict_Dict = OrderedDict([('CAMB', MkDt.CAMB_make_dict), ('N-GenIC',MkDt.N_GenIC_make_dict), ('Gadget2', MkDt.gadget_make_dict),
                                        ('AHF', MkDt.AHF_make_dict), ('POWMS', MkDt.POWMS_make_dict)])
        return MakeOpts_Dict_Dict

    #---------------------------------------
    def Run_Creat(self, JobID):
        #-------------
        print JobID.partition('_')[0]
        if JobID.partition('_')[0] == "N-GenIC":
            N_c = self.NGenIC_nc_Var.get(); N_p = self.NGenIC_np_Var.get()
        elif JobID.partition('_')[0] == "Gadget2":
            N_c = self.Gadget2_nc_Var.get(); N_p = self.Gadget2_np_Var.get()
        elif JobID.partition('_')[0] == "AHF":
            N_c = self.AHF_nc_Var.get(); N_p = self.AHF_np_Var.get()
        elif JobID.partition('_')[0] == "POWMS":
            N_c = self.POWMS_nc_Var.get(); N_p = self.POWMS_np_Var.get()
        else:
            N_c = 1; N_p = 1
        #-------------
        x = main(self.DirtVar.get(), self.Run_nameVar.get()); x.create_dirs()
        x.write_param_file(JobID, self.Update_Param_Dicts()[JobID])
        if self.run_mode_logic != "local":
            xx = main(self.Remote_DirtVar.get(), self.Run_nameVar.get())
            x.write_pbs_job(xx.loc_Exc, xx.loc_param, N_c, N_p, JobID, JobID.partition('_')[0], self.Email_Var.get())
            x.grid_make_idl(xx.loc_ICs, self.Box_SizeVar.get(), self.N_partVar.get()); x.camb_to_gadget(xx.loc_ICs)
            x.qsub_task_run(xx.loc_pbs_jobs, self.Running_Jobs_Lb.get(1, END))
        
        x.output_times(self.Strt_Redshift_Var.get(), self.End_RedshiftVar.get(), self.Snaps_NumVar.get())
        subprocess_cmd("cd " + self.DirtVar.get() + " && zip -r -FSr " +  self.Run_nameVar.get() + ".zip " + self.Run_nameVar.get())
        
        if self.run_mode_logic != "local":
            # sftp Upload :---------------------
            filepath = os.path.join(self.Remote_DirtVar.get(), self.Run_name.get()) + ".zip"
            localpath = x.loc_run_name + ".zip"
            self.sftp.put(localpath, filepath)

            self.client.exec_command('unzip -o ' + filepath); self.client.exec_command('rm ' + filepath)
            stdin, stdout, stderr = self.client.exec_command('ls -l -t -R ' + os.path.join(self.Remote_DirtVar.get(), self.Run_name.get()))
            self.text_area.delete(1.0, END)
            self.text_area.insert(END, stdout.read())

    def Run_Delete(self, JobID):
        x = main(self.DirtVar.get(), self.Run_nameVar.get())
        subprocess_cmd("rm -rf " + x.loc_param + JobID)
        subprocess_cmd("rm -rf " + x.loc_pbs_jobs + JobID + '.pbs')
        if self.run_mode_logic != "local":
            xx = main(self.Remote_DirtVar.get(), self.Run_nameVar.get())
            self.client.exec_command("rm -rf " + xx.loc_param + JobID)
            self.client.exec_command("rm -rf " + xx.loc_pbs_jobs + JobID + '.pbs')
            
            stdin, stdout, stderr = self.client.exec_command('ls -l -t -R ' + os.path.join(self.Remote_DirtVar.get(), self.Run_name.get()))
            self.text_area.delete(1.0, END)
            self.text_area.insert(END, stdout.read())

    def Code_Compile(self):
        x = main(self.DirtVar.get(), self.Run_nameVar.get()); x.create_dirs()
        
        job = self.CodesVar.get(); x.write_makefile(job, self.Update_MakeOpts_Dicts()[job])
        subprocess_cmd("cd " + self.DirtVar.get() + " && zip -r -FSr " +  self.Run_nameVar.get() + ".zip " + self.Run_nameVar.get())
        
        if job == "CAMB":
            Dirct_Var_dict = self.CAMB_Dirct_Var.get()
        elif job == "N-GenIC":
            Dirct_Var_dict = self.NGenIC_Dirct_Var.get()
        elif job == "Gadget2":
            Dirct_Var_dict = self.Gadget2_Dirct_Var.get()
        elif job == "AHF":
            Dirct_Var_dict = self.AHF_Dirct_Var.get()
            x.write_makefile('param.h', PrDt.param_h_file_dict)
        elif job == "POWMS":
            Dirct_Var_dict = self.POWMS_Dirct_Var.get()

        #-------------------------------------------
        if self.run_mode_logic == "local":
            x = main(self.DirtVar.get(), self.Run_nameVar.get())
            if job == "AHF":
                subprocess_cmd("mv " + x.loc_makefiles + "param.h " + self.AHF_Dirct_Var.get() + "/src")
            
            clean_cmd = "make clean -C " + Dirct_Var_dict
            make_cmd = "make -C " + Dirct_Var_dict + " -f " + x.loc_makefiles + job

            self.text_area.delete(1.0, END)
            self.text_area.insert(END, subprocess_cmd(clean_cmd))
            self.text_area.insert(END, '\n \n' + subprocess_cmd(make_cmd))
            VL.ViewLog(self.master, subprocess_cmd(make_cmd))
            
            if job != "N-GenIC" and job != "Gadget2":
                subprocess_cmd("mv " + self.CAMB_Dirct_Var.get() + "/camb " +  x.loc_Exc + "CAMB" )
                subprocess_cmd("mv " + self.AHF_Dirct_Var.get() + "/bin/AHF " +  x.loc_Exc + "AHF")
                subprocess_cmd("mv " + self.POWMS_Dirct_Var.get() + "/bin/powmes " +  x.loc_Exc + "POWMS")

        else:
            xx = main(self.Remote_DirtVar.get(), self.Run_nameVar.get())
            
            # sftp Upload :---------------------
            filepath = os.path.join(self.Remote_DirtVar.get(), self.Run_name.get()) + ".zip"
            localpath = x.loc_run_name + ".zip"
            self.sftp.put(localpath, filepath)
            
            self.client.exec_command('unzip -o ' + filepath); self.client.exec_command('rm ' + filepath)
            
            #----------------------------------
            self.client.exec_command('export LANG=C && export LC_ALL=C')
            if job == "AHF":
                self.client.exec_command("mv " + xx.loc_makefiles + "param.h " + self.AHF_Dirct_Var.get() + "/src")

            clean_cmd = "make clean -C " + Dirct_Var_dict
            make_cmd = "make -C " + Dirct_Var_dict + " -f " + xx.loc_makefiles + job

            self.text_area.delete(1.0, END)
            self.text_area.insert(END, self.client.exec_command(clean_cmd)[1].read())
            self.text_area.insert(END, '\n \n' + self.client.exec_command(make_cmd)[1].read())
            VL.ViewLog(self.master, self.client.exec_command(make_cmd)[1].read())

            if job != "N-GenIC" and job != "Gadget2":
                self.client.exec_command("mv " + self.CAMB_Dirct_Var.get() + "/camb " +  xx.loc_Exc + "CAMB" )
                self.client.exec_command("mv " + self.AHF_Dirct_Var.get() + "/bin/AHF " +  xx.loc_Exc + "AHF")
                self.client.exec_command("mv " + self.POWMS_Dirct_Var.get() + "/bin/powmes " +  xx.loc_Exc + "POWMS")

    def QSub_Run(self):
        if self.run_mode_logic != "local":
            x = main(self.Remote_DirtVar.get(), self.Run_nameVar.get())
            self.text_area.delete(1.0, END)
            self.text_area.insert(END, self.client.exec_command('/opt/apps/idl/idl80/bin/idl -e \'.RUN '+ x.loc_param + 'grid.pro\'')[1].read())
            self.text_area.insert(END, '\n \n' + self.client.exec_command(x.loc_Exc + 'CAMB ' + x.loc_param + 'CAMB')[1].read())
            self.text_area.insert(END, '\n \n' + self.client.exec_command('python ' + x.loc_param + 'CAMB2Gadget.py')[1].read())
            self.text_area.insert(END, '\n \n' + self.client.exec_command('sh ' + x.loc_pbs_jobs + 'run.pbs')[1].read())

    #------------------------------------
    def CosmoParm_Select(self, value):
        if value == 'Planck':
            self.Omega_l_Var.set(0.6817); self.Omega_m_Var.set(0.2678); self.Omega_bVar.set(0.049)
            self.n_sVar.set(0.9619);self.sigma_8Var.set(0.8347); self.H_0Var.set(0.6704)
        elif value == 'WMAP9':
            self.Omega_l_Var.set(0.7181); self.Omega_m_Var.set(0.236); self.Omega_bVar.set(0.0461)
            self.n_sVar.set(0.9646);self.sigma_8Var.set(0.817); self.H_0Var.set(0.697)
        elif value == 'WMAP7':
            self.Omega_l_Var.set(0.728); self.Omega_m_Var.set(0.226); self.Omega_bVar.set(0.0455)
            self.n_sVar.set(0.967);self.sigma_8Var.set(0.81); self.H_0Var.set(0.704)
        elif value == 'WMAP5':
            self.Omega_l_Var.set(0.723); self.Omega_m_Var.set(0.231); self.Omega_bVar.set(0.0459)
            self.n_sVar.set(0.962);self.sigma_8Var.set(0.817); self.H_0Var.set(0.702)
        elif value == 'WMAP3':
            self.Omega_l_Var.set(0.732); self.Omega_m_Var.set(0.224); self.Omega_bVar.set(0.044)
            self.n_sVar.set(0.947);self.sigma_8Var.set(0.776); self.H_0Var.set(0.704)
        elif value == 'WMAP1':
            self.Omega_l_Var.set(0.710); self.Omega_m_Var.set(0.243); self.Omega_bVar.set(0.047)
            self.n_sVar.set(0.99);self.sigma_8Var.set(0.9); self.H_0Var.set(0.72)
        elif value == 'WALLABY':
            self.Omega_l_Var.set(0.75); self.Omega_m_Var.set(0.205); self.Omega_bVar.set(0.045)
            self.n_sVar.set(1.0);self.sigma_8Var.set(0.9); self.H_0Var.set(0.73)
        elif value == 'GIGGLEZ':
            self.Omega_l_Var.set(0.726); self.Omega_m_Var.set(0.228); self.Omega_bVar.set(0.0456)
            self.n_sVar.set(0.96);self.sigma_8Var.set(0.812); self.H_0Var.set(0.705)

        elif value == 'Custom':
            self.Omega_l_Var.set(0); self.Omega_m_Var.set(0); self.Omega_bVar.set(0)
            self.n_sVar.set(0);self.sigma_8Var.set(0); self.H_0Var.set(0)
            
        else:
            print "Error Entering Cosmological Parameters !"

    def SysType_Select(self, value):
        if value == 'Local':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_Local_dict.values()[i])
        elif value == 'Sciama':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_Sciama_dict.values()[i])
        elif value == 'MPA':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_MPA_dict.values()[i])
        elif value == 'OpteronMPA':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_OpteronMPA_dict.values()[i])
        elif value == 'OPA_Cluster32':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_OPA_Cluster32_dict.values()[i])
        elif value == 'OPA_Cluster64':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_OPA_Cluster64_dict.values()[i])
        elif value == 'Mako':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_Mako_dict.values()[i])
        elif value == 'Regatta':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_Regatta_dict.values()[i])
        elif value == 'RZG_LinuxCluster':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_RZG_LinuxCluster_dict.values()[i])
        elif value == 'RZG_LinuxCluster_gcc':
            for i in range(len(MkDt.LibIncls_dict)):
                self.InclLib_listVar[MkDt.LibIncls_dict.keys()[i]].set(MkDt.LibIncls_RZG_LinuxCluster_gcc_dict.values()[i])
        else:
            print "Error !!"


    def CosmoModelParm_Select(self,value):
        if value == 'LCDM':
            self.phi_0_label.grid_forget(); self.phi_0.grid_forget(); self.Gamma_label.grid_forget()
            self.Gamma.grid_forget(); self.f_NL_label.grid_forget(); self.f_NL.grid_forget()
            self.w_x_label.configure(image = self.w_Lambda_photo)#; self.w_x_label.photo = self.w_Lambda_photo
            self.w_x_Var.set(-1.0); self.cs2_Var.set(1.0)
                
        if value == 'LCDM + f_NL':
            self.phi_0_label.grid_forget(); self.phi_0.grid_forget(); self.Gamma_label.grid_forget()
            self.Gamma.grid_forget(); self.f_NL_label.grid_forget(); self.f_NL.grid_forget()
            
            self.f_NL_label.grid(row = 1, column = 4, sticky = W+E+N+S); self.f_NL.grid(row = 1, column = 5, sticky = W+E+N+S)
            self.w_x_Var.set(-1.0); self.cs2_Var.set(1.0)
        
        elif value == 'wCDM':
            self.phi_0_label.grid_forget(); self.phi_0.grid_forget(); self.Gamma_label.grid_forget(); self.Gamma.grid_forget()
            self.w_x_Var.set(-0.9); self.cs2_Var.set(1.0)

        elif value == 'qCDM':
            self.phi_0_label.grid(row = 1, column = 4, sticky = W+E+N+S); self.phi_0.grid(row = 1, column = 5, sticky = W+E+N+S)
            self.Gamma_label.grid_forget(); self.Gamma.grid_forget()
            self.w_x_Var.set(-0.9); self.cs2_Var.set(1.0)

    def Calc_Redshift(self, *args):
        self.Redshift_listOpt['menu'].delete(0, 'end')
        self.a_ini = 1.0/(float(self.Strt_Redshift_Var.get()) + 1.0)
        self.a_0 = 1.0/(float(self.End_RedshiftVar.get()) + 1.0)
        log_a_start = log10(self.a_ini); log_a_end   = log10(self.a_0)
        log_a_bin = (log_a_end-log_a_start)/(self.Snaps_NumVar.get() - 1.0)
        log_a_output = [log_a_start + (i * log_a_bin) for i in range(self.Snaps_NumVar.get())]
        a_output  = [10.0**log_a_output[i] for i in range(self.Snaps_NumVar.get())]
        z_out = 1.0/array(a_output) - 1.0
        
        self.Snaps_dict = {}
        self.Redshift_list_new = [str(round(z_out[i] ,3)) for i in range(self.Snaps_NumVar.get())]
        for choice in self.Redshift_list_new:
            self.Redshift_listOpt['menu'].add_command(label=choice, command=_setit(self.Redshift_listVar, choice))
        for i in range(self.Snaps_NumVar.get()):
            self.Snaps_dict[str(self.Redshift_list_new[i])] = i - 1

    #---------------------------------
    def callback_NBodyTrace(self, *args):
        if self.run_mode_logic == "local":
            x = main(self.DirtVar.get(), self.Run_nameVar.get())
        else:
            x = main(self.Remote_DirtVar.get(), self.Run_nameVar.get())
        
        # CAMB :-----------------------
        self.CAMB_Parms_listVar['output_root'].set(x.loc_ICs + self.Run_nameVar.get())
        self.CAMB_Parms_listVar['ombh2'].set(self.Omega_bVar.get() * self.H_0Var.get()**2)
        self.CAMB_Parms_listVar['omch2'].set(self.Omega_m_Var.get() * self.H_0Var.get()**2)
        self.CAMB_Parms_listVar['omega_baryon'].set(self.Omega_bVar.get())
        self.CAMB_Parms_listVar['omega_cdm'].set(self.Omega_m_Var.get())
        self.CAMB_Parms_listVar['omega_lambda'].set(self.Omega_l_Var.get())
        self.CAMB_Parms_listVar['hubble'].set(self.H_0Var.get() * 100)
        self.CAMB_Parms_listVar['w'].set(self.w_x_Var.get())
        self.CAMB_Parms_listVar['cs2_lam'].set(self.cs2_Var.get())
        self.CAMB_Parms_listVar['scalar_spectral_index(1)'].set(self.n_sVar.get())
        self.CAMB_Parms_listVar['transfer_redshift(1)'].set(self.Init_Redshift_Var.get())
        
        # N-GenIC :--------------------
        self.NGenIC_listVar['Nmesh'].set(self.N_partVar.get())
        self.NGenIC_listVar['Nsample'].set(self.N_partVar.get())
        self.NGenIC_listVar['Box'].set(self.Box_SizeVar.get())
        self.NGenIC_listVar['FileBase'].set(self.Run_nameVar.get())
        self.NGenIC_listVar['OutputDir'].set(x.loc_ICs)
        self.NGenIC_listVar['GlassFile'].set(x.loc_ICs + 'grid')
        self.NGenIC_listVar['FileWithInputSpectrum'].set(x.loc_ICs + self.Run_nameVar.get() + '_matterpower.dat')
        self.NGenIC_listVar['FileWithInputTransfer'].set(x.loc_ICs + self.Run_nameVar.get() +  '_transfer_out.dat')
        
        self.NGenIC_listVar['Omega'].set(self.Omega_m_Var.get())
        self.NGenIC_listVar['OmegaLambda'].set(self.Omega_l_Var.get())
        self.NGenIC_listVar['OmegaBaryon'].set(self.Omega_bVar.get())
        self.NGenIC_listVar['HubbleParam'].set(self.H_0Var.get())
        self.NGenIC_listVar['Redshift'].set(self.Init_Redshift_Var.get())
        self.NGenIC_listVar['Sigma8'].set(self.sigma_8Var.get())
        self.NGenIC_listVar['PrimordialIndex'].set(self.n_sVar.get())
        self.NGenIC_listVar['RedshiftFnl'].set(self.Init_Redshift_Var.get())
        self.NGenIC_listVar['Fnl'].set(self.f_NL_Var.get())
        #Gadget 2:----------------------
        self.Gadget2_listVar['InitCondFile'].set(x.loc_ICs + self.Run_nameVar.get())
        self.Gadget2_listVar['OutputDir'].set(x.loc_Snaps)
        self.Gadget2_listVar['SnapshotFileBase'].set(self.Run_nameVar.get())
        self.Gadget2_listVar['OutputListFilename'].set(x.loc_Snaps + 'Output_times')
        self.Gadget2_listVar['TimeBegin'].set(1.0/(self.Init_Redshift_Var.get() + 1.0))
        self.Gadget2_listVar['TimeMax'].set(1.0/(self.Finl_RedshiftVar.get() + 1.0))
        self.Gadget2_listVar['Omega0'].set(self.Omega_m_Var.get())
        self.Gadget2_listVar['OmegaLambda'].set(self.Omega_l_Var.get())
        self.Gadget2_listVar['OmegaBaryon'].set(self.Omega_bVar.get())
        self.Gadget2_listVar['HubbleParam'].set(self.H_0Var.get())
        self.Gadget2_listVar['BoxSize'].set(self.Box_SizeVar.get())
        self.Gadget2_listVar['ErrTolIntAccuracy'].set(self.etaVar.get())
        self.Gadget2_listVar['SofteningHalo'].set(self.epsilonVar.get())
        self.Gadget2_listVar['SofteningHaloMaxPhys'].set(self.epsilonVar.get())
        #AHF :-------------------------
        self.AHF_listVar['ic_filename'].set(x.loc_Snaps + self.Run_nameVar.get() + '_%03d' %(self.Snaps_dict[str(self.Redshift_listVar.get())] + 1))
        self.AHF_listVar['outfile_prefix'].set(x.loc_Halos + self.Run_nameVar.get() + '_%03d' %(self.Snaps_dict[str(self.Redshift_listVar.get())] + 1))
        self.AHF_listVar['LgridDomain'].set(self.N_partVar.get())
        self.AHF_listVar['LgridMax'].set(self.N_partVar.get()**3)
        #POWMS :-----------------------
        self.POWMS_listVar[' filein '].set('\'' + x.loc_Snaps + self.Run_nameVar.get() + '_%03d' %(self.Snaps_dict[str(self.Redshift_listVar.get())] + 1) + '\'')
        self.POWMS_listVar[' ngrid '].set(self.N_partVar.get())
        self.POWMS_listVar[' filepower '].set( '\'' + x.loc_PowerSpectrum + self.Run_nameVar.get() + '_%03d_powspec' %(self.Snaps_dict[str(self.Redshift_listVar.get())] + 1) + '\'')

        self.list["+AHF"] = ['AHF_%s' %self.Redshift_listVar.get()]
        self.list["+POWMS"] = ['POWMS_%s' %self.Redshift_listVar.get()]

    def callback_MakeOptionsTrace(self, *args):
        self.Gadget_MakeOptions_CheckButton[4].config(text='-DPMGRID=%s' %self.N_partVar.get())
        self.Gadget_MakeOptions_CheckButton[4].config(onvalue='-DPMGRID=%s' %self.N_partVar.get())
    
        self.Gadget_MakeOptions_CheckButton[-1].config(text='-DMAKEGLASS=%s' %int(self.N_partVar.get())**3)
        self.Gadget_MakeOptions_CheckButton[-1].config(onvalue='-DMAKEGLASS=%s' %int(self.N_partVar.get())**3)
    

    def softining_length(self,event):
        x = float(self.Box_SizeVar.get())/(40.0 * float(self.N_partVar.get()))
        self.epsilonVar.set(round(x,4))

#--------- RUN ----------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root = Tk()
    app = Application(master=root)
    app.mainloop()
