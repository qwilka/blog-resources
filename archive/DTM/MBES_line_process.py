from __future__ import division
from __future__ import print_function

import collections
import glob
import os
import re
import subprocess
import sys

module_path = os.path.abspath('C:/Users/Stephen/Documents/stephen/Projects/src/kongevei')
if module_path not in sys.path:
    sys.path.append(module_path) 

from MBES.MBESlib import (segment_line, bbox_from_KP_in_XL, segment_XYZ,
   XL_to_pipeXYZ, pipeXYZ_to_PLY)

lineID = "L01"
surveydate = "2015-07-25"

OD = 0.660 + (3.2+45.0)*2/1000

_5pt_file = "C:/Users/Stephen/Documents/MBES/2015_Skarv/5-point Listings/2015INS801-GEP26-GVI/NO.E10503 BP GVI 2015INS801_GEP26_kp-000001kp079929_5pt Listing_MSL.xlsx"
_5pt_ws = "BP 5 pt"
_5pt_1st_datarow=8
Ecol=3
Ncol=4
Zcol=7
KPcol=6
_5ptZfactor=-1.0
pipecolour = (255, 85, 0)

MBES_dir = "C:/Users/Stephen/Documents/MBES/2015_Skarv/DTMs/"
xyzZfactor=1.0
XYZsep=" "
xyz_1st_datarow=1
# shift UTM coordinates to OpenGL-friendly values
Xshift=-390000.
Yshift=-7220000.
Eextend=20
Nextend=20

target_segment_len = 1000.
KPstart = 65000.
KPend = 80000.

ccexe = "C:/Users/Stephen/Documents/bin/CloudCompare_v2.6.2_bin_x64/CloudCompare.exe"

reMBESfname = re.compile(r'(?i)^DTM_(\w+)_(\w+)_KP([+-]?\d*\.?\d*)_KP([+-]?\d*\.?\d*)_(\d+).zip$')

file_KPrange_map = collections.OrderedDict()
fileslist = [ MBES_dir + "DTM_GEP26_801_kp064.608_kp065.202_20150724232016.zip" ]
fileslist.extend(glob.glob(MBES_dir + 'DTM_GEP26_801_kp06[5-9].*.zip'))
fileslist.extend(glob.glob(MBES_dir + 'DTM_GEP26_801_kp07[0-9].*.zip'))
for fpath in fileslist:
    fname = os.path.basename(fpath)
    m = reMBESfname.match(fname)
    print(m.groups())
    KPmin = float(m.group(3))
    KPmax = float(m.group(4))
    file_KPrange_map[(KPmin, KPmax)] = fpath


segment_length, num_segments, segments_list = segment_line(KPend=KPend, 
    target_seglen=target_segment_len, KPstart=KPstart, maxret=True)

for ii, currKPs in enumerate(segments_list):
    print("Segment {} KPs = {},{}".format(ii, currKPs[0], currKPs[1]))
    XYZfiles = []

    for k in file_KPrange_map:
        inrange = False
        if k[0]<currKPs[1] and k[1]>currKPs[0]:
            inrange = True
        else:
            inrange = False
        if inrange:
            fpath = file_KPrange_map[k]
            fname = os.path.basename(fpath)
            fname_base = os.path.splitext(fname)[0]
            XYZfiles.append( (fpath, fname_base+'.xyz') )
        #print(XYZfiles)

    bbox = bbox_from_KP_in_XL(XLfile=_5pt_file,
                      wsname="BP 5 pt", Ecol=Ecol, Ncol=Ncol, KPcol=KPcol, 
                      data_row_1st=_5pt_1st_datarow, KP_bounds=currKPs, 
                      Eextend=Eextend, Nextend=Nextend )
    print(bbox) 
    OPfile="{0}_MBES_KP{1:d}-KP{2:d}_{3}.xyz".format(lineID, int(currKPs[0]*1000), int(currKPs[1]*1000), surveydate)
    print(OPfile)
    tmpXYZfile = segment_XYZ(XYZfiles, 
                         bbox=bbox, 
                data_row_1st=xyz_1st_datarow, 
                Xshift=Xshift, Yshift=Yshift, Zshift=0, Zfactor=xyzZfactor,
                XYZsep=XYZsep,
                OPfile=OPfile, OPsep=",")

    ccoptions =  " -SILENT -NO_TIMESTAMP -AUTO_SAVE OFF " # -SILENT
    ccoptions +=  " -O " + tmpXYZfile 
    #ccoptions +=  " -SET_ACTIVE_SF 2 "
    ccoptions += " -DELAUNAY -AA -MAX_EDGE_LENGTH 0.6 "
    #ccoptions += " -SAVE_CLOUDS "
    ccoptions += " -SAVE_MESHES "
    arglist = [ccexe,]
    arglist.extend(ccoptions.split())
    rtnstr = subprocess.check_output(arglist , 
                      stderr=subprocess.STDOUT,
                      shell=False)
    print("CC returned message: {}".format(rtnstr))
    
    print("deleting temp files {}".format(tmpXYZfile))
    os.remove(tmpXYZfile) 
  


    OPfile="DELETE_{0}_5pt_KP{1:.3f}_KP{2:.3f}_{3}.xyz".format(lineID, currKPs[0], currKPs[1], surveydate)
    tmp5ptfile = XL_to_pipeXYZ(XLfile=_5pt_file, 
                                wsname=_5pt_ws, Xcol=Ecol, Ycol=Ncol, Zcol=Zcol, KPcol=KPcol,
                                data_row_1st=_5pt_1st_datarow, data_row_last=None,
                                Xshift=Xshift, Yshift=Yshift, Zshift=-OD/2, Zfactor=_5ptZfactor,
                                KP_bounds=currKPs, 
                                OPfile=OPfile, OPsep=" "  )

    PLYfile_5pt="{0}_5pt_KP{1:d}-KP{2:d}_{3}.ply".format(lineID, int(currKPs[0]*1000), int(currKPs[1]*1000), surveydate)
    pipeXYZ_to_PLY(tmp5ptfile, 
                   OD = OD, 
                   OPfile=PLYfile_5pt,
                   colour=pipecolour)    


    ccoptions =  " -SILENT -NO_TIMESTAMP -AUTO_SAVE OFF " # -SILENT
    ccoptions +=  " -COMPUTE_NORMALS "  # not working for PLY file
    ccoptions +=  " -O " + PLYfile_5pt 
    ccoptions += " -SAVE_MESHES "
    arglist = [ccexe,]
    arglist.extend(ccoptions.split())
    rtnstr = subprocess.check_output(arglist , 
                      stderr=subprocess.STDOUT,
                      shell=False)
    print("CC returned message: {}".format(rtnstr))


    print("deleting temp files {} {}".format(tmp5ptfile, PLYfile_5pt))
    os.remove(tmp5ptfile)
    os.remove(PLYfile_5pt)

