from collections import *

#-----------------------------
CAMB_Parms_dict = OrderedDict([('output_root', ''),
('get_transfer', 'T'),
('do_lensing', 'T'),
('do_nonlinear', 1),

('use_physical', 'T'),
('ombh2',''),
('omch2',''),
('omnuh2', 0.0),

('omega_baryon',''),
('omega_cdm',''),
('omega_lambda',''),
('omega_neutrino', 0.0),
('omk', 0.0),

('hubble',''),
('w', -1),
('cs2_lam', 1),
('scalar_spectral_index(1)',''),
('transfer_redshift(1)',''),
#--------------------------------
('get_scalar_cls', 'F'),
('get_vector_cls', 'F'),
('get_tensor_cls', 'F'),
('l_max_scalar', 2200),
('l_max_tensor', 1500),
('k_eta_max_tensor', 3000),
('temp_cmb', 2.7255),
('helium_fraction', 0.24),
('massless_neutrinos', 2.046),
('nu_mass_eigenstates', 1),
('massive_neutrinos', 1),
('share_delta_neff', 'T'),
('nu_mass_fractions', 1),
('nu_mass_degeneracies', ''),
('initial_power_num', 1),
('pivot_scalar', 0.05),
('pivot_tensor', 0.05),
('scalar_amp(1)', 2.1e-9),
('scalar_nrun(1)', 0),
('scalar_nrunrun(1)', 0),
('tensor_spectral_index(1)', 0),
('tensor_nrun(1)', 0),
('tensor_parameterization', 1),
('initial_ratio(1)', 1),
('reionization', 'T'),
('re_use_optical_depth', 'T'),
('re_optical_depth', 0.09),
('re_redshift', 11),
('re_delta_redshift', 1.5),
('re_ionization_frac', -1),
('RECFAST_fudge', 1.14),
('RECFAST_fudge_He', 0.86),
('RECFAST_Heswitch', 6),
('RECFAST_Hswitch', 'T'),
('initial_condition', 1),
('initial_vector', '-1 0 0 0 0'),
('vector_mode', 0),
('COBE_normalize', 'F'),
('CMB_outputscale', 7.42835025e12),
('transfer_high_precision', 'F'),
('transfer_kmax', 6206.13),
('transfer_k_per_logint', 5),
('transfer_num_redshifts', 1),
('transfer_interp_matterpower', 'T'),
('transfer_filename(1)', 'transfer_out.dat'),
('transfer_matterpower(1)', 'matterpower.dat'),
('transfer_power_var', 7),
('scalar_output_file', 'scalCls.dat'),
('vector_output_file', 'vecCls.dat'),
('tensor_output_file', 'tensCls.dat'),
('total_output_file', 'totCls.dat'),
('lensed_output_file', 'lensedCls.dat'),
('lensed_total_output_file', 'lensedtotCls.dat'),
('lens_potential_output_file', 'lenspotentialCls.dat'),
('FITS_filename', 'scalCls.fits'),
('do_lensing_bispectrum', 'F'),
('do_primordial_bispectrum', 'F'),
('bispectrum_nfields', 1),
('bispectrum_slice_base_L', 0),
('bispectrum_ndelta', 3),
('bispectrum_delta(1)', 0),
('bispectrum_delta(2)', 2),
('bispectrum_delta(3)', 4),
('bispectrum_do_fisher', 'F'),
('bispectrum_fisher_noise', 0),
('bispectrum_fisher_noise_pol', 0),
('bispectrum_fisher_fwhm_arcmin', 7),
('bispectrum_full_output_file', ''),
('bispectrum_full_output_sparse', 'F'),
('bispectrum_export_alpha_beta', 'F'),
('feedback_level', 1),
('derived_parameters', 'T'),
('lensing_method', 1),
('accurate_BB', 'F'),
('massive_nu_approx', 1),
('accurate_polarization', 'T'),
('accurate_reionization', 'T'),
('do_tensor_neutrinos', 'T'),
('do_late_rad_truncation', 'T'),
('halofit_version', ''),
('number_of_threads', 0),
('high_accuracy_default', 'T'),
('accuracy_boost', 1),
('l_accuracy_boost', 1),
('l_sample_boost', 1)
])

#----------------------------
NGenIC_dict = OrderedDict([('Nmesh', ''),
('Nsample', ''),
('Box', ''),
('FileBase', ''),
('OutputDir', ''),
('GlassFile', ''),
('TileFac', 1),
('Omega', ''),
('OmegaLambda', ''),
('OmegaBaryon', ''),
('HubbleParam', ''),
('Redshift', ''),
('Sigma8', ''),
('PrimordialIndex', ''),
('SphereMode', 1),
('WhichSpectrum', 1),
('FileWithInputSpectrum', ''),
('InputSpectrum_UnitLength_in_cm',  3.085678e24),
('ReNormalizeInputSpectrum', 0),
('ShapeGamma', 0.21),

('Seed', 123456),
('NumFilesWrittenInParallel', 1),

('UnitLength_in_cm', 3.085678e24),
('UnitMass_in_g', 1.989e43),
('UnitVelocity_in_cm_per_s',  1e5)
])

NGenIC_dict.pop('ReNormalizeInputSpectrum')
NGenIC_dict['GlassTileFac'] = NGenIC_dict.pop('TileFac')
NGenIC_dict['OmegaDM_2ndSpecies'] = 0
NGenIC_dict['WDM_On'] = 0
NGenIC_dict['WDM_Vtherm_On'] = 0
NGenIC_dict['WDM_PartMass_in_kev'] = 10.0
NGenIC_dict['RedshiftFnl'] = ''
NGenIC_dict['Fnl'] = ''
NGenIC_dict['WhichSpectrum'] = 0
NGenIC_dict['WhichTransfer'] = 2
NGenIC_dict['FileWithInputTransfer'] = ''

#----------------------------
Gadget2_dict = OrderedDict([('InitCondFile',''),
('OutputDir', ''),
('EnergyFile', 'energy.txt'),
('InfoFile', 'info.txt'),
('TimingsFile', 'timings.txt'),
('CpuFile', 'cpu.txt'),
('RestartFile', 'restart'),
('SnapshotFileBase',''),
('OutputListFilename',''),
('TimeLimitCPU', 360000),
('ResubmitOn', 0),
('ResubmitCommand', 'my-scriptfile'),
('ICFormat', 1),
('SnapFormat', 1),
('ComovingIntegrationOn', 1),
('TypeOfTimestepCriterion', 0),
('OutputListOn', 1),
('PeriodicBoundariesOn', 1),
('TimeBegin', ''),
('TimeMax', ''),
('Omega0',  ''),
('OmegaLambda', ''),
('OmegaBaryon', ''),
('HubbleParam', ''),
('BoxSize', ''),
('TimeBetSnapshot', 0.5),
('TimeOfFirstSnapshot', 0),
('CpuTimeBetRestartFile', 36000.0),
('TimeBetStatistics', 0.05),
('NumFilesPerSnapshot', 1),
('NumFilesWrittenInParallel', 1),
('ErrTolIntAccuracy', 0.025),
('MaxRMSDisplacementFac', 0.2),
('CourantFac', 0.15),
('MaxSizeTimestep', 0.3),
('MinSizeTimestep', 0.0),
('ErrTolTheta', 0.5),
('TypeOfOpeningCriterion', 1),
('ErrTolForceAcc', 0.005),
('TreeDomainUpdateFrequency', 0.1),
('DesNumNgb', 33),
('MaxNumNgbDeviation', 2),
('ArtBulkViscConst', 0.8),
('InitGasTemp', 0.0),
('MinGasTemp', 0.0),
('PartAllocFactor', 1.6),
('TreeAllocFactor', 0.8),
('BufferSize', 30),
('UnitLength_in_cm', 3.085678e24),
('UnitMass_in_g', 1.989e43),
('UnitVelocity_in_cm_per_s', 1e5),
('GravityConstantInternal', 0),
('MinGasHsmlFractional', 0.25),
('SofteningGas', 0.0),
('SofteningHalo',''),
('SofteningDisk', 0),
('SofteningBulge', 0),
('SofteningStars', 0),
('SofteningBndry', 0),
('SofteningGasMaxPhys', 0.0),
('SofteningHaloMaxPhys', ''),
('SofteningDiskMaxPhys', 0),
('SofteningBulgeMaxPhys', 0),
('SofteningStarsMaxPhys', 0),
('SofteningBndryMaxPhys', 0)
])

#----------------------------
POWMS_dict = OrderedDict([('&input !', ''),
(' verbose ', '.true.'),
(' megaverbose ', '.true.'),
(' filein ', ''),
(' nfile ', 1),
(' nmpi ', -1),
(' read_mass ', '.false.'),
(' nfoldpow ', -512),
(' ngrid ', ''),
(' norder ', 3),
(' shift ', '0.0 0.0 0.0'),
(' filepower ', ''),
(' filepower_fold ', '#powspec'),
(' filetaylor ', '#powspec.taylor'),
('/ !', '')
])

#----------------------------
AHF_dict = OrderedDict([('[AHF] #', ''),
('ic_filename',''),
('ic_filetype', 60),
('outfile_prefix',''),
('LgridDomain', ''),
('LgridMax', ''),
('NperDomCell', 3.0),
('NperRefCell', 3.0),
('VescTune', 1.5),
('NminPerHalo', 20),
('RhoVir', 0),
('Dvir', 200),
('MaxGatherRad', 5.0),
('LevelDomainDecomp', 6),
('NcpuReading', 1),
('de_filename', 'my_dark_energy_table.txt'),

('[GADGET] #', ''),
('GADGET_LUNIT', 1),
('GADGET_MUNIT', 1e10),

('[TIPSY] #', ''),
('TIPSY_BOXSIZE', 50.0),
('TIPSY_MUNIT', 4.75e16),
('TIPSY_VUNIT', 1810.1),
('TIPSY_EUNIT', 0.0),
('TIPSY_OMEGA0', 0.24),
('TIPSY_LAMBDA0', 0.76),

('[ART] #', ''),
('ART_BOXSIZE', 20),
('ART_MUNIT', 6.5e8)
])

#----------------------------
param_h_file_dict = OrderedDict([ ('#ifndef PARAM_INCLUDED\n\
#define PARAM_INCLUDED\n\
#include <float.h>\n\
#include "define.h"\n\
#define AHF_MINPART_GAS     10     /* min. number of gas for spin and shape calculation                                          */\n\
#define AHF_MINPART_STARS   10     /* min. number of stars for spin and shape calculation                                        */\n\
#define AHF_MINPART_SHELL   10     /* min. number of particles in a profile shell for using AHFshellshape                        */\n\
#define AHF_NBIN_MULTIPLIER 1      /* (integer value) increases the number of radial bins by this factor from the standard value */\n\
#define AHF_HIRES_DM_WEIGHT 1.0\n\
#define AHF_HOSTHALOLEVEL   1      /* first level to be considered as credible to spawn subbaloes                                */\n\
#define AHF_HOSTSUBOVERLAP  0.5    /* how far should the subhalo have entered into the host                                      */\n\
#define AHF_MIN_REF_OFFSET  0      /* offset for first refinement to be used by AHF                                              */\n\
#define AHF_RISE            1.00   /* Rho > AHF_RISE*Rho_prev -> rising density                                                  */\n\
#define AHF_SLOPE           0.99   /* outer halo profile at least like r^-AHF_SLOPE                                              */\n\
#define AHF_MAXNRISE        2      /* try to catch variations in density                                                         */\n\
#define AHF_Rmax_r2_NIGNORE 5      /* how many central particle to ignore with AHFparticle_RMax_r2 feature                       */\n\
#define PGAS                0.0   /* identifier for gas particles; has to be exactly 0.0!!!!                                     */\n\
#define PDM                -1.0   /* identifier for dm particles; whatever negative value                                        */\n\
#define PSTAR              -4.0   /* identifier for star particles; whatever negative value                                      */\n\
#define PDMbndry           -5.0   /* identifier for bndry particles; whatever negative value                                     */\n\
\n\
#define AHFrfocusX 57.06044914\n\
#define AHFrfocusY 52.61864923\n\
#define AHFrfocusZ 48.70489744\n\
#define AHFrfocusR 0.5\n\
\n\
#define Gyr       3.1558e16         /* [sec]                   */\n\
#define Mpc       3.08567782e19     /* [km]                    */', ''),
                      
('#define H0 ' , '100.'),
('#define cH0 ' , '2998.0'),
 
('#define rhoc0     2.7755397e11      /* [h^2*Msun]/[Mpc^3]      */\n\
#define Grav      4.3006485e-9      /* [Mpc*km^2]/[Msun*sec^2] */\n\
#define kB_per_mp 0.825481286614E-2 /* [(km/sec)^2/K]          */\n\
#define kBoltzman 6.9416792         /* [(km/sec)^2 Msun/K]     */\n\
#define Msun      1.9891e30         /* [kg]                    */\n\
#define MIN_NNODES 125            /* smallest grid-block 5x5x5     */\n\
#define MAXSTRING    2048   /* used for char statement, i.e. filenames etc.     */\n\
#define AMIGAHEADER  2048   /* maximum size (in bytes) for output file header   */\n\
#define HEADERSTRING 256    /* no. of characters for header string in outfiles  */\n\
#define HEADERSIZE  (HEADERSTRING*sizeof(char)+2*sizeof(long)+6*sizeof(int)+46*sizeof(double))\n\
#define FILLHEADER  (AMIGAHEADER-HEADERSIZE)\n\
#define TERMINATE_AMIGA {"terminateAMIGA"}\n\
#define MAXTIME      10000   /* interpolation points for timeline (cf. tdef.h)   */\n\
#define bytes2GB  9.313225746154785e-10\n\
#define DOMSWEEPS  10     /* number of domain and refinement sweeps...   10   */\n\
#define REFSWEEPS  10     /* ...before checking for convergence          10   */\n\
#define W_SOR      1.34   /* successive over-relaxation parameter        1.34 */\n\
#define ETA        0.625  /* parameter for slow convergence              0.625*/\n\
#define CONVCRIT   0.1    /* convergence criterion                       0.1  */\n\
#define DOMCORRECT 0.25   /* constrained criterion on domain grid        0.25 */\n\
#define SPEEDFRAC  0.01   /* fraction of particles allowed to speed      0.01 */\n\
#ifdef MPI_DEBUG\n\
#undef MAXTIME\n\
#define MAXTIME 100\n\
#endif\n\
#define BITS_PER_DIMENSION 21\n\
#define MAX_SEND_PARTICLES 1000000\n\
#define VERBOSITY 6\n\
#define NSTEPS       1000    /* number of (initial) steps for time stepping     */\n\
#define CA_CRIT      0.15    /* restricts timestep due to da/a criterion    0.05*/\n\
#define CELLFRAC_MAX 0.2     /* how far are particles allowed to move       0.2*/\n\
#define CELLFRAC_MIN 0.05    /* how far should particles move at least      0.05*/\n\
#define CF_MEAN      ((CELLFRAC_MAX+CELLFRAC_MIN)/2)\n\
#define NDIM      3          /* DO NOT EVER TOUCH THIS NUMBER!  */\n\
#define CRITMULTI 8.0\n\
#define NP_RATIO  7.5\n\
#ifdef DOUBLE\n\
#define ZERO         (1E-12)\n\
#define MACHINE_ZERO (5E-16)\n\
#else\n\
#define ZERO         (1e-6)\n\
#define MACHINE_ZERO (5e-16)\n\
#endif\n\
#define MZERO        (1e-10)  /* used when reading GADGET files */\n\
#define GADGET_MUNIT 1.0e10    /* GADGET mass unit in Msol/h    */\n\
#ifdef GADGET_LUNIT_KPC\n\
#define GADGET_LUNIT 1.0e-3\n\
#else                          /* GADGET length unit in Mpc/h   */\n\
#define GADGET_LUNIT 1.0\n\
#endif\n\
#define PI    3.14159265358979323846264338\n\
#define TWOPI 6.28318530717958647692528677\n\
#define SQRT2 1.41421356237309504880168872\n\
#define X 0     /* x-coord symbol */\n\
#define Y 1     /* y-coord symbol */\n\
#define Z 2     /* z-coord symbol */\n\
\n\
#define YES   1\n\
#define NO    0\n\
#define ON    1\n\
#define OFF   0\n\
#define TRUE  1\n\
#define FALSE 0\n\
#endif', '') ])







