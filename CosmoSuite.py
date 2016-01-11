from __future__ import division
import os, sys
from numpy import *
from collections import *
import time


#--------------------------------------
class main(object):
    #--------------------------------
    def __init__(self, Run_Dict, Run_name):
        self.__location__ = Run_Dict
        self.Run_name = Run_name
        self.loc_run_name = os.path.join(self.__location__, self.Run_name)
        self.loc_param = os.path.join(self.__location__, self.Run_name + "/Params/")
        self.loc_makefiles = os.path.join(self.__location__, self.Run_name + "/Makefiles/")
        self.loc_pbs_jobs = os.path.join(self.__location__, self.Run_name + "/PBS_Jobs/")
        self.loc_Exc = os.path.join(self.__location__, self.Run_name + "/EXC/")
        #---- N-Body Directories ---------
        self.loc_ICs = os.path.join(self.__location__, self.Run_name +  "/ICs/")
        self.loc_Snaps = os.path.join(self.__location__, self.Run_name + "/Snaps/")
        self.loc_PowerSpectrum = os.path.join(self.__location__, self.Run_name + "/PowerSpectrum/")
        self.loc_Halos = os.path.join(self.__location__, self.Run_name + "/Halos/")

    #--------------------------------
    def create_dirs(self):
        #---: Create working diectory !!
        try:
            os.stat(self.loc_run_name); os.stat(self.loc_param); os.stat(self.loc_makefiles); os.stat(self.loc_pbs_jobs); os.stat(self.loc_Exc)
            os.stat(self.loc_ICs); os.stat(self.loc_Snaps); os.stat(self.loc_PowerSpectrum); os.stat(self.loc_Halos)
        except:
            os.mkdir(self.loc_run_name); os.mkdir(self.loc_param); os.mkdir(self.loc_makefiles); os.mkdir(self.loc_pbs_jobs); os.mkdir(self.loc_Exc)
            os.mkdir(self.loc_ICs); os.mkdir(self.loc_Snaps); os.mkdir(self.loc_PowerSpectrum); os.mkdir(self.loc_Halos)

    #--------------------------------
    def write_param_file(self, code, params):
        f = open(self.loc_param + code, 'w')
        if code != 'N-GenIC' and code != 'Gadget2':
            for i in range(len(params)):
                f.write(params.keys()[i] + ' = ' + str(params.values()[i]) + '\n')
        else:
            for i in range(len(params)):
                f.write(params.keys()[i] + '  ' + str(params.values()[i]) + '\n')
        f.close()
    
    #----------------------------
    def write_makefile(self, code, params):
        f = open(self.loc_makefiles + code, 'w')
        for i in range(len(params)):
            f.write(params.keys()[i] + '' + str(params.values()[i]) + '\n')
        f.close()

    #----------------------------
    def write_pbs_job(self, Dirct, loc_Exc, loc_param, np, nc, code, Exctbl, Email):
        f = open(self.loc_pbs_jobs + code + '.pbs', 'w')
        f.write('#!/bin/bash \n\
#PBS -l nodes=%s:ppn=%s \n\
#PBS -l walltime=9999:00:00 \n\
#PBS -q cluster.q \n\
#PBS -N %s \n\
#PBS -V \n\
#PBS -M %s \n\
#PBS -e %s/%s.error \n\
#PBS -o %s/%s.output \n\
#PBS -d ./ \n' %(np, nc,  self.Run_name + '_' + code, Email, Dirct, self.Run_name+ '_' + code, Dirct, self.Run_name+ '_' + code))
        if  Exctbl != "AHF":
            f.write('\nmodule purge\n\
module add apps/plc/1.1\n\
module add apps/idl/8.5\n\
module add compilers/intel/intel-64.v13.1.046\n\
module add mpi/openmpi/1.4.3/intel-64.v13.1.046\n')
                
        f.write('\nmpirun -np %s ' %(np * nc) + ' ' + loc_Exc + Exctbl + ' ' + loc_param + code)
        f.close()

    def grid_make_idl(self, loc_ICs, Box_Size, N_part):
        f = open(self.loc_param + 'grid.pro', 'w')
        f.write('fout = "'+ loc_ICs + 'grid"')
        f.write('\nN  = %sL' %N_part)
        f.write('\nNtot = N * N * N \n\
npart=lonarr(6) \n\
massarr=dblarr(6) \n\
time=0.0D \n\
redshift=0.0D \n\
flag_sfr=0L \n\
flag_feedback=0L \n\
npartall=lonarr(6) \n\
flag_cooling= 0L \n\
num_files= 1L \n\
BoxSize = 0.0D \n\
bytesleft=120 \n\
la=intarr(bytesleft/2) ')
        f.write('\nBoxSize = %sD ' %Box_Size)
        f.write('\nnpart(1) = Ntot \n\
npartall(1) = Ntot \n\
pos= fltarr(3, Ntot) \n\
for i=0L, N-1 do begin \n\
for j=0L, N-1 do begin \n\
for k=0L, N-1 do begin \n\
pos(0, (i*N+j)*N+k) = (i+0.0)/N * BoxSize \n\
pos(1, (i*N+j)*N+k) = (j+0.0)/N * BoxSize \n\
pos(2, (i*N+j)*N+k) = (k+0.0)/N * BoxSize \n\
endfor \n\
endfor \n\
endfor \n\
openw,1,fout,/f77_unformatted \n\
writeu,1, npart,massarr,time,redshift,flag_sfr,flag_feedback,npartall,flag_cooling,num_files,BoxSize,la \n\
writeu,1, pos \n\
close,1 \n\
end ')
        f.close()

    #----: Task Defining !!
    def qsub_task_run(self, loc_pbs_jobs, Joblist):
        f = open(self.loc_pbs_jobs + 'run.pbs', 'w')
        f.write('#!/bin/bash')
        f.write('\n%s_0=`qsub ' %self.Run_name + loc_pbs_jobs + 'N-GenIC' + '.pbs`')
        f.write('\n%s_1=`qsub -W depend=afterok:$%s_0 '  %(self.Run_name, self.Run_name) + loc_pbs_jobs + 'Gadget2' + '.pbs`')
        for i in range(len(Joblist)):
            f.write('\n%s_%s=`qsub -W depend=afterok:$%s_1 '  %(self.Run_name, i + 2, self.Run_name) + loc_pbs_jobs + Joblist[i].strip("['']") + '.pbs`')
        f.close()

    def output_times(self, z_ini, z_f, NSnaps):
        a_ini = 1.0/(1.0 + z_ini); a_f = 1.0/(1.0 + z_f)
        f = open(self.loc_Snaps + 'Output_times', 'w')
        log_a_start = log10(a_ini); log_a_end   = log10(a_f)
        log_a_bin = (log_a_end-log_a_start)/(NSnaps-1.0)
        log_a_output = [log_a_start + (i * log_a_bin) for i in range(NSnaps)]
        a_output  = [10.0**log_a_output[i] for i in range(NSnaps)]
        for i in range(NSnaps):
            f.write('%s\n' %a_output[i])
        f.close()

    def camb_to_gadget(self, loc_ICs):
        f_py = open(self.loc_param + 'CAMB2Gadget.py', 'w')
        f_py.write('from __future__ import division\nfrom numpy import *\n')
        f_py.write('k_camb, P_k_camb = loadtxt(' + '"' + loc_ICs + self.Run_name + '"' + ' + "_matterpower.dat", unpack=True)\n')
        f_py.write('kt_camb, T_k_camb = loadtxt(' + '"' + loc_ICs + self.Run_name + '"' + ' + "_transfer_out.dat", unpack=True,usecols = [0,1])\n')
        f_py.write('k_gadget = log10(k_camb); P_k_gadget = log10(4 * pi * k_camb**3 * P_k_camb)\n')
        f_py.write('f = open(' + '"' + loc_ICs + self.Run_name + '"' + ' + "_matterpower.dat", "w")\n')
        f_py.write('f.writelines("%s            %s\\n" %(k_gadget[i], P_k_gadget[i]) for i in range(len(k_gadget)))\n')
        f_py.write('ff = open(' + '"' + loc_ICs + self.Run_name + '"' + ' + "_transfer_out.dat", "w")\n')
        f_py.write('kt_gadget = kt_camb; T_k_gadget =  T_k_camb\n\
for i in range(len(kt_gadget)):\n\
    if log10(kt_gadget[0]) <= -4.6:\n\
        ff.writelines("%s            %s\\n" %(kt_gadget[i], T_k_gadget[i]))\n\
    else:\n\
        print "K value is out of Gadget range !!"\n\
f.close(); ff.close()')
        f_py.close()

    def hmf_calc(self, calc_z):
        m_halos = loadtxt(self.loc_Halos + self.Run_name + '_%03d' %(self.calc_Snap + 1) + '.0000.z%3.3f' %calc_z + '.AHF_halos', usecols = [3], unpack = True)
        masses_sim = sort(m_halos); Volume = (self.Box_Size/1000)**3
        n_cumulative_sim = arange(len(masses_sim), 0, -1)
        masses_sim, unique_indices = unique(masses_sim, return_index=True)
        
        sim_volume = Volume
        n_cumulative_sim = n_cumulative_sim[unique_indices]/sim_volume
        
        hmf_data = self.loc_Halos + self.Run_name + '_%03d' %(self.calc_Snap + 1) + '.z%3.3f' %calc_z + '.hmf_simulated'
        hmf_file = open(hmf_data, "w")
        line = \
        "#Columns:\n" + \
        "#1. mass [Msun]\n" + \
        "#2. cumulative number density of halos [comoving Mpc^-3]\n"
        hmf_file.write(line)
        for i in xrange(masses_sim.size - 1):
            line = "%e\t%e\n" % (masses_sim[i], n_cumulative_sim[i])
            hmf_file.write(line)
        hmf_file.close()


