from collections import *

#--------------------------------------
LibIncls_dict = OrderedDict([
('CC',  'mpicc'),
('OPTIMIZE',  '-O2 -Wall -g'),
('GSL_INCL', '-I/opt/envhpc/gsl/1.9/include/'),
('GSL_LIBS', '-L/opt/envhpc/gsl/1.9/lib/'),
('FFTW_INCL', '-I/opt/envhpc/fftw/2.1.5/include'),
('FFTW_LIBS', '-L/opt/envhpc/fftw/2.1.5/lib'),
('MPICHLIB', '-L/usr/local/lib/'),
('HDF5INCL', '-I/opt/envhpc/hdf5/1.8.14/include'),
('HDF5LIB', '-L/opt/envhpc/hdf5/1.8.14/lib -lhdf5') ])

#--------------------------------------
Gadget_MakeOptions = OrderedDict([
#--------------------------------------- Basic operation mode of code
('OPT0',     '-DPERIODIC'),
('OPT1',     '-DUNEQUALSOFTENINGS'),


#--------------------------------------- Things that are always recommended
('OPT2',     '-DPEANOHILBERT'),
('OPT3',     '-DWALLCLOCK'),


#--------------------------------------- TreePM Options
('OPT4',     '-DPMGRID='),
('OPT5',     '-DPLACEHIGHRESREGION=3'),
('OPT6',     '-DENLARGEREGION=1.2'),
('OPT7',     '-DASMTH=1.25'),
('OPT8',     '-DRCUT=4.5'),


#--------------------------------------- Single/Double Precision
('OPT9',     '-DDOUBLEPRECISION'),
('OPT10',     '-DDOUBLEPRECISION_FFTW'),


#--------------------------------------- Time integration options
('OPT11',     '-DSYNCHRONIZATION'),
('OPT12',     '-DFLEXSTEPS'),
('OPT13',     '-DPSEUDOSYMMETRIC'),
('OPT14',     '-DNOSTOP_WHEN_BELOW_MINTIMESTEP'),
('OPT15',     '-DNOPMSTEPADJUSTMENT'),


#--------------------------------------- Output 
('OPT16',     '-DHAVE_HDF5'),
('OPT17',     '-DOUTPUTPOTENTIAL'),
('OPT18',     '-DOUTPUTACCELERATION'),
('OPT19',     '-DOUTPUTCHANGEOFENTROPY'),
('OPT20',     '-DOUTPUTTIMESTEP'),


#--------------------------------------- Things for special behaviour
('OPT21',     '-DNOGRAVITY'),
('OPT22',     '-DNOTREERND'),
('OPT23',     '-DNOTYPEPREFIX_FFTW'),
('OPT24',     '-DLONG_X=60'),
('OPT25',     '-DLONG_Y=5'),
('OPT26',     '-DLONG_Z=0.2'),
('OPT27',     '-DTWODIMS'),
('OPT28',     '-DSPH_BND_PARTICLES'),
('OPT29',     '-DNOVISCOSITYLIMITER'),
('OPT30',     '-DCOMPUTE_POTENTIAL_ENERGY'),
('OPT31',     '-DLONGIDS'),
('OPT32',     '-DISOTHERM_EQS'),
('OPT33',     '-DADAPTIVE_GRAVSOFT_FORGAS'),
('OPT34',     '-DSELECTIVE_NO_GRAVITY=2+4+8+16'),

#--------------------------------------- Testing and Debugging options
('OPT35',     '-DFORCETEST=0.1'),


#--------------------------------------- Glass making
('OPT36' ,    '-DMAKEGLASS=')])

#-------------------------
gadget_make_dict = OrderedDict([ ('EXEC   =  ', ''),
('OPT =  ',  ''),
#--------------------------------------
('CC = ',  'mpicc'),
('OPTIMIZE = ',  '-O2 -Wall -g'),
('GSL_INCL = ', '-I/opt/envhpc/gsl/1.9/include/'),
('GSL_LIBS = ', '-L/opt/envhpc/gsl/1.9/lib/'),
('FFTW_INCL = ', '-I/opt/envhpc/fftw/2.1.5/include'),
('FFTW_LIBS = ', '-L/opt/envhpc/fftw/2.1.5/lib'),
('MPICHLIB = ', '-L/usr/local/lib/'),
('HDF5INCL = ', '-I/opt/envhpc/hdf5/1.8.14/include'),
('HDF5LIB = ', '-L/opt/envhpc/hdf5/1.8.14/lib -lhdf5'),

#----------------------------------------
('OPTIONS =  $(OPTIMIZE) $(OPT)\n\
OBJS   = main.o  run.o  predict.o begrun.o endrun.o global.o timestep.o  init.o restart.o  io.o accel.o read_ic.o  ngb.o system.o  allocate.o  density.o gravtree.o hydra.o  driftfac.o domain.o  allvars.o potential.o forcetree.o   peano.o gravtree_forcetest.o pm_periodic.o pm_nonperiodic.o longrange.o \n\
\n\
INCL   = allvars.h  proto.h  tags.h  Makefile \n\
CFLAGS = $(OPTIONS) $(GSL_INCL) $(FFTW_INCL) $(HDF5INCL) \n\
ifeq (NOTYPEPREFIX_FFTW,$(findstring NOTYPEPREFIX_FFTW,$(OPT))) \n\
    FFTW_LIB = $(FFTW_LIBS) -lrfftw_mpi -lfftw_mpi -lrfftw -lfftw \n\
else \n\
ifeq (DOUBLEPRECISION_FFTW,$(findstring DOUBLEPRECISION_FFTW,$(OPT))) \n\
    FFTW_LIB = $(FFTW_LIBS) -ldrfftw_mpi -ldfftw_mpi -ldrfftw -ldfftw \n\
else \n\
    FFTW_LIB = $(FFTW_LIBS) -lsrfftw_mpi -lsfftw_mpi -lsrfftw -lsfftw \n\
endif \n\
endif \n\
LIBS   =   $(HDF5LIB) -g  $(MPICHLIB)  $(GSL_LIBS) -lgsl -lgslcblas -lm $(FFTW_LIB) \n\
$(EXEC): $(OBJS) \n\
\t$(CC) $(OBJS) $(LIBS)   -o  $(EXEC)  \n\
$(OBJS): $(INCL) \n\
clean: \n\
\trm -f $(OBJS) $(EXEC)', '') ])


#--------------------------------
N_GenIC_MakeOptions = OrderedDict([
('OPT0' , '-DPRODUCEGAS'),
('OPT1' , '-DMULTICOMPONENTGLASSFILE'),
('OPT2' , '-DDIFFERENT_TRANSFER_FUNC'),
('OPT3' , '-DNO64BITID'),
('OPT4' , '-DCORRECT_CIC'),
('OPT5' , '-DONLY_ZA'),
('OPT6' , '-DONLY_GAUSSIAN'),
('OPT7' , '-DLOCAL_FNL'),
('OPT8' , '-DEQUIL_FNL'),
('OPT9' , '-DORTOG_FNL') ])

#--------------------------------
N_GenIC_make_dict = OrderedDict([
('EXEC = ' , ''),
('OPT = ' , ''),
('CC = ' , ' mpicc'),
('OPTIMIZE = ' , '  -O3 -Wall'),
('GSL_INCL = ' , '-I/opt/envhpc/gsl/1.9/include/'),
('GSL_LIBS = ' , '-L/opt/envhpc/gsl/1.9/lib/'),
('FFTW_INCL = ' , '-I/opt/envhpc/fftw/2.1.5/include'),
('FFTW_LIBS = ' , '-L/opt/envhpc/fftw/2.1.5/lib'),
('MPICHLIB = ' , '-L/usr/local/lib/'),
('HDF5INCL = ', ''),
('HDF5LIB = ', ''),


#---------------------------------------
('OPTIONS =  $(OPT) \n\
OBJS   = main.o power.o checkchoose.o allvars.o save.o read_param.o  read_glass.o nrsrc/nrutil.o nrsrc/qromb.o nrsrc/polint.o nrsrc/trapzd.o \n\
INCL   = allvars.h proto.h  nrsrc/nrutil.h  Makefile \n\
FFTW_LIB =  $(FFTW_LIBS) -lsrfftw_mpi -lsfftw_mpi -lsrfftw -lsfftw \n\
LIBS   =   -lm  $(MPICHLIB)  $(FFTW_LIB)  $(GSL_LIBS)  -lgsl -lgslcblas \n\
CFLAGS =   $(OPTIONS)  $(OPTIMIZE)  $(FFTW_INCL) $(GSL_INCL) \n\
$(EXEC): $(OBJS) \n\
\t$(CC) $(OPTIMIZE) $(OBJS) $(LIBS)   -o  $(EXEC) \n\
$(OBJS): $(INCL) \n\
.PHONY : clean \n\
clean: \n\
\trm -f $(OBJS) $(EXEC)', '') ])


#---------------------------------------

LibIncls_Local_dict = OrderedDict([
('CC' , 'mpicc'),
('OPTIMIZE' , '-O2 -Wall -g'),

('GSL_INCL' , '-I/opt/envhpc/gsl/1.9/include/'),
('GSL_LIBS' , '-L/opt/envhpc/gsl/1.9/lib/'),

('FFTW_INCL' , '-I/opt/envhpc/fftw/2.1.5/include'),
('FFTW_LIBS' , '-L/opt/envhpc/fftw/2.1.5/lib'),

('MPICHLIB' , '-L/usr/local/lib/'),

('HDF5INCL' , '-I/opt/envhpc/hdf5/1.8.14/include'),
('HDF5LIB' , '-L/opt/envhpc/hdf5/1.8.14/lib -lhdf5') ])


LibIncls_Sciama_dict = OrderedDict([
('CC' , 'mpicc'),
('OPTIMIZE' , '-O3 -Wall'),

('GSL_INCL' , '-I/opt/apps/libs/gsl/1.16/intel-64.v13.1.046/include'),
('GSL_LIBS' , '-L/opt/apps/libs/gsl/1.16/intel-64.v13.1.046/lib'),

('FFTW_INCL' , '-I/opt/apps/libs/fftw2/2.1.5/intel-64.v13.1.046/include'),
('FFTW_LIBS' , '-L/opt/apps/libs/fftw2/2.1.5/intel-64.v13.1.046/lib'),

('MPICHLIB' , '-L/opt/apps/mpi/openmpi/1.4.3/intel-64.v13.1.046/lib'),

('HDF5INCL' , '-I/opt/gridware/pkg/apps/hdf5_mpi/1.8.11/gcc-4.4.7+openmpi-1.8.1/include'),
('HDF5LIB' , '-L/opt/gridware/pkg/apps/hdf5_mpi/1.8.11/gcc-4.4.7+openmpi-1.8.1/lib') ])

LibIncls_MPA_dict = OrderedDict([
('CC' , 'mpicc'),
('OPTIMIZE' , '-O3 -Wall'),
('GSL_INCL' , '-I/usr/common/pdsoft/include'),
('GSL_LIBS' , '-L/usr/common/pdsoft/lib  -Wl,"-R /usr/common/pdsoft/lib"'),
('FFTW_INCL' , ''),
('FFTW_LIBS' , ''),
('MPICHLIB' , ''),
('HDF5INCL' , ''),
('HDF5LIB' , '-lhdf5 -lz') ])



LibIncls_OpteronMPA_dict = OrderedDict([
('CC' , 'mpicc'),
('OPTIMIZE' , '-O3 -Wall -m64'),
('GSL_INCL' , '-L/usr/local/include'),
('GSL_LIBS' , '-L/usr/local/lib'),
('FFTW_INCL' , ''),
('FFTW_LIBS' , ''),
('MPICHLIB' , ''),
('HDF5INCL' , '-I/opt/hdf5/include'),
('HDF5LIB' , '-L/opt/hdf5/lib -lhdf5 -lz  -Wl,"-R /opt/hdf5/lib"') ])



LibIncls_OPA_Cluster32_dict = OrderedDict([
('CC' , 'mpicc'),
('OPTIMIZE' , '-O3 -Wall'),
('GSL_INCL' , '-I/afs/rzg/bc-b/vrs/opteron32/include'),
('GSL_LIBS' , '-L/afs/rzg/bc-b/vrs/opteron32/lib  -Wl,"-R /afs/rzg/bc-b/vrs/opteron32/lib"'),
('FFTW_INCL' , '-I/afs/rzg/bc-b/vrs/opteron32/include'),
('FFTW_LIBS' , '-L/afs/rzg/bc-b/vrs/opteron32/lib'),
('MPICHLIB' , ''),
('HDF5INCL' , ''),
('HDF5LIB' , '-lhdf5 -lz') ])



LibIncls_OPA_Cluster64_dict = OrderedDict([
('CC' , 'mpicc'),
('OPTIMIZE' , '-O3 -Wall -m64'),
('GSL_INCL' , '-I/afs/rzg/bc-b/vrs/opteron64/include'),
('GSL_LIBS' , '-L/afs/rzg/bc-b/vrs/opteron64/lib  -Wl,"-R /afs/rzg/bc-b/vrs/opteron64/lib"'),
('FFTW_INCL' , '-I/afs/rzg/bc-b/vrs/opteron64/include'),
('FFTW_LIBS' , '-L/afs/rzg/bc-b/vrs/opteron64/lib'),
('MPICHLIB' , ''),
('HDF5INCL' , ''),
('HDF5LIB' , '-lhdf5 -lz') ])



LibIncls_Mako_dict = OrderedDict([
('CC' , 'mpicc'),
('OPTIMIZE' , '-O3 -march=athlon-mp  -mfpmath=sse'),
('GSL_INCL' , ''),
('GSL_LIBS' , ''),
('FFTW_INCL' , ''),
('FFTW_LIBS' , ''),
('MPICHLIB' , ''),
('HDF5INCL' , ''),
('HDF5LIB' , '-lhdf5 -lz') ])



LibIncls_Regatta_dict = OrderedDict([
('CC' , 'mpcc_r'),
('OPTIMIZE' , '-O5 -qstrict -qipa -q64'),
('GSL_INCL' , '-I/afs/rzg/u/vrs/gsl_psi64/include'),
('GSL_LIBS' , '-L/afs/rzg/u/vrs/gsl_psi64/lib'),
('FFTW_INCL' , '-I/afs/rzg/u/vrs/fftw_psi64/include'),
('FFTW_LIBS' , '-L/afs/rzg/u/vrs/fftw_psi64/lib  -q64 -qipa'),
('MPICHLIB' , ''),
('HDF5INCL' , '-I/afs/rzg/u/vrs/hdf5_psi64/include'),
('HDF5LIB' , '-L/afs/rzg/u/vrs/hdf5_psi64/lib  -lhdf5 -lz') ])



LibIncls_RZG_LinuxCluster_dict = OrderedDict([
('CC' , 'mpicci'),
('OPTIMIZE' , '-O3 -ip'),
('GSL_INCL' , '-I/afs/rzg/u/vrs/gsl_linux/include'),
('GSL_LIBS' , '-L/afs/rzg/u/vrs/gsl_linux/lib  -Wl,"-R /afs/rzg/u/vrs/gsl_linux/lib"'),
('FFTW_INCL' , '-I/afs/rzg/u/vrs/fftw_linux/include'),
('FFTW_LIBS' , '-L/afs/rzg/u/vrs/fftw_linux/lib'),
('MPICHLIB' , ''),
('HDF5INCL' , '-I/afs/rzg/u/vrs/hdf5_linux/include'),
('HDF5LIB' , '-L/afs/rzg/u/vrs/hdf5_linux/lib -lhdf5 -lz  -Wl,"-R /afs/rzg/u/vrs/hdf5_linux/lib"') ])



LibIncls_RZG_LinuxCluster_gcc_dict = OrderedDict([
('CC' , 'mpiccg'),
('OPTIMIZE' , '-Wall -g -O3 -march=pentium4'),
('GSL_INCL' , '-I/afs/rzg/u/vrs/gsl_linux_gcc3.2/include'),
('GSL_LIBS' , '-L/afs/rzg/u/vrs/gsl_linux_gcc3.2/lib  -Wl,"-R /afs/rzg/u/vrs/gsl_linux_gcc3.2/lib"'),
('FFTW_INCL' , '-I/afs/rzg/u/vrs/fftw_linux_gcc3.2/include'),
('FFTW_LIBS' , '-L/afs/rzg/u/vrs/fftw_linux_gcc3.2/lib'),
('MPICHLIB' , ''),
('HDF5INCL' , '-I/afs/rzg/u/vrs/hdf5_linux/include'),
('HDF5LIB' , '-L/afs/rzg/u/vrs/hdf5_linux/lib  -lhdf5 -lz  -Wl,"-R /afs/rzg/u/vrs/hdf5_linux/lib"') ])

#-------------------------------------------
CAMB_make_dict = OrderedDict([
('FISHER=' , ''),

('EQUATIONS     ?=' , 'equations'),
('POWERSPECTRUM ?=' , 'power_tilt'),
('REIONIZATION ?=' , 'reionization'),
('RECOMBINATION ?=' , 'recfast'),
('BISPECTRUM ?=' , 'SeparableBispectrum'),
('NONLINEAR     ?=' , 'halofit_ppf'),
('DRIVER        ?=' , 'inidriver.F90'),

('FITSDIR       ?=' , '/usr/local/lib'),
('FITSLIB       =' , 'cfitsio'),
('HEALPIXDIR    ?=' , '/usr/local/healpix'),

('F90C     = gfortran\n\
FFLAGS =  -O3 -fopenmp -ffast-math -fmax-errors=4\n\
DEBUGFLAGS = -cpp -g -fbounds-check -fbacktrace -ffree-line-length-none -fmax-errors=4 -ffpe-trap=invalid,overflow,zero\n\
MODOUT =  -J$(OUTPUT_DIR)\n\
IFLAG = -I',''),

('ifneq ($(FISHER),)\n\
FFLAGS += -DFISHER\n\
EXTCAMBFILES = Matrix_utils.o\n\
else\n\
EXTCAMBFILES =\n\
endif\n\
\n\
DEBUGFLAGS ?= FFLAGS\n\
Debug: FFLAGS=$(DEBUGFLAGS)' , ''),

('Release: OUTPUT_DIR = Release\n\
Debug: OUTPUT_DIR = Debug\n\
OUTPUT_DIR ?= Release\n\
\n\
Release: camb\n\
Debug: camb\n\
\n\
CAMBLIB       = $(OUTPUT_DIR)/libcamb_$(RECOMBINATION).a\n\
F90FLAGS      = $(FFLAGS)\n\
F90FLAGS += $(MODOUT) $(IFLAG)$(OUTPUT_DIR)/\n\
HEALPIXLD     = -L$(HEALPIXDIR)/lib -lhealpix -L$(FITSDIR) -l$(FITSLIB)\n\
F90CRLINK ?= -lstdc++', ''),

('CAMBOBJ       =  $(OUTPUT_DIR)/constants.o  $(OUTPUT_DIR)/utils.o $(EXTCAMBFILES)  $(OUTPUT_DIR)/subroutines.o $(OUTPUT_DIR)/inifile.o  $(OUTPUT_DIR)/$(POWERSPECTRUM).o  $(OUTPUT_DIR)/$(RECOMBINATION).o $(OUTPUT_DIR)/$(REIONIZATION).o $(OUTPUT_DIR)/modules.o $(OUTPUT_DIR)/bessels.o $(OUTPUT_DIR)/$(EQUATIONS).o $(OUTPUT_DIR)/$(NONLINEAR).o $(OUTPUT_DIR)/lensing.o $(OUTPUT_DIR)/$(BISPECTRUM).o $(OUTPUT_DIR)/cmbmain.o $(OUTPUT_DIR)/camb.o\n\
\n\
ifeq ($(RECOMBINATION),cosmorec)\n\
COSMOREC_PATH ?=../CosmoRec/\n\
GSL_LINK ?=-lgsl -lgslcblas\n\
camb: libCosmoRec.a\n\
$(CAMBLIB): libCosmoRec.a\n\
F90CRLINK += -L$(COSMOREC_PATH) -lCosmoRec $(GSL_LINK)\n\
endif\n\
\n\
ifeq ($(RECOMBINATION),hyrec)\n\
HYREC_PATH ?= ../HyRec/\n\
camb: libhyrec.a\n\
$(CAMBLIB): libhyrec.a\n\
F90CRLINK += -L$(HYREC_PATH) -lhyrec\n\
endif\n\
\n\
default: camb\n\
all: camb libcamb\n\
libcamb: $(CAMBLIB)\n\
$(OUTPUT_DIR)/subroutines.o: $(OUTPUT_DIR)/constants.o $(OUTPUT_DIR)/utils.o\n\
$(OUTPUT_DIR)/$(POWERSPECTRUM).o: $(OUTPUT_DIR)/subroutines.o  $(OUTPUT_DIR)/inifile.o\n\
$(OUTPUT_DIR)/$(RECOMBINATION).o: $(OUTPUT_DIR)/subroutines.o $(OUTPUT_DIR)/inifile.o\n\
$(OUTPUT_DIR)/$(REIONIZATION).o: $(OUTPUT_DIR)/constants.o $(OUTPUT_DIR)/inifile.o\n\
$(OUTPUT_DIR)/modules.o: $(OUTPUT_DIR)/$(REIONIZATION).o $(OUTPUT_DIR)/$(POWERSPECTRUM).o $(OUTPUT_DIR)/$(RECOMBINATION).o\n\
$(OUTPUT_DIR)/bessels.o: $(OUTPUT_DIR)/modules.o\n\
$(OUTPUT_DIR)/$(EQUATIONS).o: $(OUTPUT_DIR)/bessels.o\n\
$(OUTPUT_DIR)/$(NONLINEAR).o:  $(OUTPUT_DIR)/modules.o $(OUTPUT_DIR)/$(EQUATIONS).o\n\
$(OUTPUT_DIR)/lensing.o: $(OUTPUT_DIR)/bessels.o\n\
$(OUTPUT_DIR)/$(BISPECTRUM).o: $(OUTPUT_DIR)/lensing.o $(OUTPUT_DIR)/modules.o\n\
$(OUTPUT_DIR)/cmbmain.o: $(OUTPUT_DIR)/lensing.o $(OUTPUT_DIR)/$(NONLINEAR).o $(OUTPUT_DIR)/$(EQUATIONS).o $(OUTPUT_DIR)/$(BISPECTRUM).o\n\
$(OUTPUT_DIR)/camb.o: $(OUTPUT_DIR)/cmbmain.o\n\
$(OUTPUT_DIR)/Matrix_utils.o: $(OUTPUT_DIR)/utils.o\n\
\n\
camb: directories $(CAMBOBJ) $(DRIVER)\n\
\t$(F90C) $(F90FLAGS) $(CAMBOBJ) $(DRIVER) $(F90CRLINK) -o $@\n\
\n\
$(CAMBLIB): directories $(CAMBOBJ)\n\
\tar -r $@ $(CAMBOBJ)\n\
\n\
camb_fits: directories writefits.f90 $(CAMBOBJ) $(DRIVER)\n\
\t$(F90C) $(F90FLAGS) -I$(HEALPIXDIR)/include $(CAMBOBJ) writefits.f90 $(DRIVER) $(HEALPIXLD) -DWRITE_FITS -o $@\n\
\n\
$(OUTPUT_DIR)/%.o: %.f90\n\
\t$(F90C) $(F90FLAGS) -c $*.f90 -o $(OUTPUT_DIR)/$*.o\n\
\n\
$(OUTPUT_DIR)/%.o: %.F90\n\
\t$(F90C) $(F90FLAGS) -c $*.F90 -o $(OUTPUT_DIR)/$*.o\n\
\n\
directories:\n\
\tmkdir -p $(OUTPUT_DIR)\n\
\n\
clean:\n\
\trm -f *.o *.a *.d core *.mod $(OUTPUT_DIR)/*.o $(OUTPUT_DIR)/*.mod\n\
\trm -rf Release*\n\
\trm -rf Debug*\n\
\n\
cleanCR:\n\
\tcd $(COSMOREC_PATH); make tidy;\n\
\n\
libCosmoRec.a:\n\
\tcd $(COSMOREC_PATH); make lib;\n\
\n\
libhyrec.a:\n\
\tcd $(HYREC_PATH); make libhyrec.a;', '') ])

#------------------------------------------------
AHF_make_dict = OrderedDict([
('DEFINEFLAGS	= ' , ''),

('CC         	= ' , 'mpicc -std=c99 -Wall -W'),
('FC         	= ' , 'mpif90'),
('OPTIMIZE	= ' , '-O2'),
('CCFLAGS		= ' , ''),
('LNFLAGS		= ' , ''),
('DEFINEFLAGS	+= ' , '-DWITH_MPI'),
('MAKE		= ' , 'make'),

#------------------------------------------------------------------#
('MASTER_DEFINEFLAGS = ' , '$(DEFINEFLAGS)'),

#------------------------------------------------------------------#
('export CC\n\
export FC\n\
export OPTIMIZE\n\
export CCFLAGS\n\
export LNFLAGS\n\
export MASTER_DEFINEFLAGS\n\
export MAKE', ''),

#===================
('AHF:	FORCE dirs\n\
\tcd src; ${MAKE} AHF; mv -f AHF ../bin/AHF', ''),

('AHF2:	FORCE dirs\n\
\tcd src; ${MAKE} AHF2; mv -f AHF2 ../bin/AHF-v2.0-000', ''),

('clean:	FORCE\n\
\tcd src; ${MAKE} clean; cd ../convert; ${MAKE} clean; cd ../tools; ${MAKE} clean; cd ../analysis; ${MAKE} clean', ''),

('FORCE:' , ''),

('dirs:\n\
\tmkdir -p bin', '') ])

#----------------------------------------------
POWMS_make_dict = OrderedDict([
('FC = ' , 'ifort'),
('FCFLAGS = ' , '-Vaxlib -CB -mcmodel=large -O -openmp -DOMP'),
('LIBS = ', '-lrfftw_threads -lrfftw -lfftw_threads -lfftw -lpthread'),

('INC = ', ''),

('OBJS =  ../src/twopidef.o ../src/numrec_tools.o ../src/random_number_tools.o ../src/fourier_tools.o ../src/gadget_ramses_tools.o ../src/fourier_taylor_tools.o ../src/fourier_tools3D.o ../src/powmes_common.o ../src/powmes.o', ''),

('all: ', 'powmes'),

('powmes:  $(OBJS)\n\
\t$(FC) $(FCFLAGS)  $(OBJS) -o $@ $(INC) $(LIBS)', ''),

('clean:\n\
\t/bin/rm  ../src/*.o *.mod', ''),

('.SUFFIXES:\n\
.SUFFIXES: .f90 .F90 .o', ''),
('.f90.o:\n\
\t$(FC) $(FCFLAGS)  $(INC) -c $< -o $@', ''),
('.F90.o:\n\
\t$(FC) $(FCFLAGS)  $(INC) -c $< -o $@', '') ])


#------------------------------------------------
AHF_MakeOptions = OrderedDict([
('OPT0'	, '-DMULTIMASS'),
('OPT1'	, '-DAHFshellshape'),
('OPT2'	, '-DBYTESWAP'),
('OPT3'	, '-DGAS_PARTICLES'),
('OPT4'	, '-DAHFrfocus'),
('OPT5'	, '-DDOUBLE'),
('OPT6'	, '-DAHFnoremunbound'),
('OPT7'	, '-DMETALHACK'),
('OPT8'	, '-DAHFptfocus=0'),
('OPT9'	, '-DDVIR_200RHOCRIT'),
('OPT10' , '-DMANUAL_DVIR=200'),
('OPT11' , '-DTIPSY_ZOOMDATA'),
('OPT12' , '-DVERBOSE2'),
('OPT13' , '-DPATCH_DEBUG'),
('OPT14' , '-DGADGET'),
('OPT15' , '-DDEBUG_AHF2'),
('OPT16' , '-DDPhalos'),
('OPT17' , '-DAHFgridtreefile'),
('OPT18' , '-DSUSSING2013'),
('OPT19' , '-DVERBOSE'),
('OPT20' , '-DCUBEKEY_128'),
('OPT20' , '-DAHFwritePreliminaryHalos') ])

