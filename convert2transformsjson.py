# convert the json files generated by nvisii_mvs into a nerf transforms.py 
# this is compatible with ngp

import json
import math
import subprocess
import argparse
import cv2
import glob
import numpy as np
import pyexr
parser = argparse.ArgumentParser()

parser.add_argument(
    '--path', 
    type = str, 
    default = None,
    required = True,
)

parser.add_argument(
    '--ext', 
    type = str, 
    default = 'png',
)


opt = parser.parse_args()
scale = 1
json_files = sorted(glob.glob(opt.path+"*.json"))


out = {}
out['frames']=[]

for i_file_name, file_name in enumerate(json_files):
  if "transforms.json" in file_name:
    continue 
  c2w=[]
  print(i_file_name,file_name)


  with open(file_name) as json_file:
    data = json.load(json_file)
  c2w = data["camera_data"]["cam2world"]        
  # print(data["camera_data"])

  fr={}
  fr["file_path"]= f"{str(i_file_name).zfill(5)}.{opt.ext}"
  fr["transform_matrix"]=[[c2w[0][0],c2w[1][0],c2w[2][0],c2w[3][0]*scale],
                          [c2w[0][1],c2w[1][1],c2w[2][1],c2w[3][1]*scale],
                          [c2w[0][2],c2w[1][2],c2w[2][2],c2w[3][2]*scale],
                          [c2w[0][3],c2w[1][3],c2w[2][3],c2w[3][3]]]  
  out['frames'].append(fr)

out['aabb'] = [
  [
    data['camera_data']['scene_min_3d_box'][0]*3,
    data['camera_data']['scene_min_3d_box'][1]*3,
    data['camera_data']['scene_min_3d_box'][2]*3,
  ],
  [
    data['camera_data']['scene_max_3d_box'][0]*3,
    data['camera_data']['scene_max_3d_box'][1]*3,
    data['camera_data']['scene_max_3d_box'][2]*3,
  ],
]

fx = data['camera_data']['intrinsics']['fx']
cx = data['camera_data']['intrinsics']['cx']
# camang = math.atan(cx/fx)*2
out['fl_x']=data['camera_data']['intrinsics']['fx']
out['fl_y']=data['camera_data']['intrinsics']['fy']
out['cx']=data['camera_data']['intrinsics']['cx']
out['cy']=data['camera_data']['intrinsics']['cy']
out['w']=data['camera_data']['width']
out['h']=data['camera_data']["height"]

with open(f'{opt.path}/transforms.json', 'w') as outfile:
    json.dump(out, outfile, indent=2)
