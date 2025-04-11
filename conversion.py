import numpy as np 
import json
import os
import pandas as pd 

all_data = []

def read_data():    
    # path = "00010/keypoints3d"
    path = "keypoints3d"
    data_list = []
    for file in os.listdir(path):
        file_name = os.path.join(path,file)
        with open(file_name) as temp:
            data = json.load(temp)
            coordinates = data[0]['keypoints3d']
            data_list.append(coordinates)
    return data_list



def create_trc_header():
    """
    Create the header for the TRC file.
    Set fps to 60 and the number of markers to 25.
    """
    header = """PathFileType\t4\t(X/Y/Z)\t\n\
DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames\n\
60\t60\t{num_frames}\t{num_markers}\tm\t100\t1\t{num_frames}\n\
Frame#\tTime\t"""
    return header

def convert_to_trc(output_file):
    marker_names = [
        'Nose', 'Neck', 'RShoulder', 'RElbow', 'RWrist',
        'LShoulder', 'LElbow', 'LWrist','CHip',
        'RHip', 'RKnee', 'RAnkle', 'LHip',
        'LKnee', 'LAnkle', 'REye', 'LEye',
        'REar', 'LEar', 'LBigToe', 'LSmallToe',
        'LHeel', 'RBigToe', 'RSmallToe', 'RHeel'
    ]
    
    num_frames = len(all_data)
    num_markers = len(marker_names)
    
    with open(output_file, 'w') as f:
        header = create_trc_header().format(
            num_frames=num_frames,
            num_markers=num_markers
        )
        f.write(header)
        column_labels = '\t'.join([f'{name}\t\t\t' for name in marker_names])
        f.write(column_labels + '\n')
        
        xyz_labels = '\t'.join(['X{}\tY{}\tZ{}'.format(i+1,i+1,i+1) for i in range(num_markers)])
        f.write(xyz_labels + '\n')
        
        for frame_idx,frame_data in enumerate(all_data):
            frame_line = [str(frame_idx+1),str(frame_idx/60)]
            for marker_data in frame_data:
                x,y,z = marker_data
                frame_line.extend([str(x),str(z),str(-y)])
            f.write('\t'.join(frame_line) + '\n')

if __name__ == '__main__':
    all_data = read_data()
    output_file = 'output.trc'
    create_trc_header()
    convert_to_trc(output_file)