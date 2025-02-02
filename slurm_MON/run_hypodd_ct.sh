#!/bin/bash

WORKING_DIR=$PWD
region="MontereyBay"
cd $region/hypodd

# if [ ! -d "HypoDD" ]; then
#   git clone git@github.com:zhuwq0/HypoDD.git
#   export PATH=$PATH:$PWD/HypoDD
#   make -C HypoDD/src/
# fi

cat <<EOF > ph2dt.inp
* ph2dt.inp - input control file for program ph2dt
* Input station file:
stations_hypoDD.dat
* Input phase file:
hypoDD.pha
*MINWGHT: min. pick weight allowed [0]
*MAXDIST: max. distance in km between event pair and stations [200]
*MAXSEP: max. hypocentral separation in km [10]
*MAXNGH: max. number of neighbors per event [10]
*MINLNK: min. number of links required to define a neighbor [8]
*MINOBS: min. number of links per pair saved [8]
*MAXOBS: max. number of links per pair saved [20]
*MINWGHT MAXDIST MAXSEP MAXNGH MINLNK MINOBS MAXOBS
   0      120     10     50     8      8     100
EOF

cat <<EOF > ct.inp
* RELOC.INP:
*--- input file selection
* cross correlation diff times:

*
*catalog P diff times:
dt.ct
*
* event file:
event.sel
*
* station file:
stations_hypoDD.dat
*
*--- output file selection
* original locations:
hypodd.loc
* relocations:
hypodd_ct.reloc
* station information:
hypodd.sta
* residual information:
hypodd.res
* source paramater information:
hypodd.src
*
*--- data type selection: 
* IDAT:  0 = synthetics; 1= cross corr; 2= catalog; 3= cross & cat 
* IPHA: 1= P; 2= S; 3= P&S
* DIST:max dist [km] between cluster centroid and station 
* IDAT   IPHA   DIST
    2     3     120
*
*--- event clustering:
* OBSCC:    min # of obs/pair for crosstime data (0= no clustering)
* OBSCT:    min # of obs/pair for network data (0= no clustering)
* OBSCC  OBSCT    
     0     0        
*
*--- solution control:
* ISTART:  	1 = from single source; 2 = from network sources
* ISOLV:	1 = SVD, 2=lsqr
* NSET:      	number of sets of iteration with specifications following
*  ISTART  ISOLV  NSET
    2        2      4
*
*--- data weighting and re-weighting: 
* NITER: 		last iteration to used the following weights
* WTCCP, WTCCS:		weight cross P, S 
* WTCTP, WTCTS:		weight catalog P, S 
* WRCC, WRCT:		residual threshold in sec for cross, catalog data 
* WDCC, WDCT:  		max dist [km] between cross, catalog linked pairs
* DAMP:    		damping (for lsqr only) 
*       ---  CROSS DATA ----- ----CATALOG DATA ----
* NITER WTCCP WTCCS WRCC WDCC WTCTP WTCTS WRCT WDCT DAMP
   4     -9     -9   -9    -9   1     1      6   10 4000 
   4     -9     -9   -9    -9   1     1      6    8 3000 
   4     -9     -9   -9    -9   1     1      6    6 2000 
   4     -9     -9   -9    -9   1     1      6    4 1000 
*
*--- 1D model:
* NLAY:		number of model layers  
* RATIO:	vp/vs ratio 
* TOP:		depths of top of layer (km) 
* VEL: 		layer velocities (km/s)
* NLAY  RATIO 
   12     1.73
* TOP 
0.0 1.0 3.0 5.0 7.0 9.0 11.0 13.0 17.0 21.0 31.00 31.10
* VEL
5.30 5.65 5.93 6.20 6.20 6.20 6.20 6.20 6.20 6.20 7.50 8.11
*
*--- event selection:
* CID: 	cluster to be relocated (0 = all)
* ID:	cuspids of event to be relocated (8 per line)
* CID    
    0      
* ID
EOF

# if [ ! -f "dt.ct" ]; then
#     ./HypoDD/src/ph2dt/ph2dt ph2dt.inp
# fi
# ./HypoDD/src/hypoDD/hypoDD ct.inp
# cp hypodd_ct.reloc hypodd_ct_catalog.txt
# cd $WORKING_DIR

if [ ! -f "dt.ct" ]; then
    ./HypoDD/ ph2dt.inp
fi
./HypoDD/ ct.inp
cp hypodd_ct.reloc hypodd_ct_catalog.txt
cd $WORKING_DIR