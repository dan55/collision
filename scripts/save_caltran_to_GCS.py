import argparse
import sys

def main(argv):

    # Define the parser
    parser = argparse.ArgumentParser(description='Stores Caltran live traffic footage to Google Cloud Storage')
    # Declare an argument (`--algo`), telling that the corresponding value
    # should be stored in the `algo` field, and using a default value if the argument isn't given
    
    parser.add_argument('--district_id', action="store", dest='district_id', default='D4')
    parser.add_argument('--camera_name', action="store", dest='camera_name', default='S880_JNO_The_Alameda')
    parser.add_argument('--duration', action="store", dest='duration', default=240)
    parser.add_argument('--segment_time', action="store", dest='segment_time', default=60)
    
    # Now, parse the command line arguments and store the values in the `args` variable
    args = parser.parse_args()
    # Individual arguments can be accessed as attributes...
    #print(args.name)
    import os
    import cv2
    import subprocess
    import time
    import numpy as np
    import pandas as pd
    
    rmtp_stream = "rtmp://wzmedia.dot.ca.gov"
    district_id = args.district_id #'D4'
    cam_name = args.camera_name 

    #cam_name = 'S880_JNO_The_Alameda'
    #cam_name = 'W80_at_Carlson_Blvd_OFR'

    full_rmtp_url = os.path.join(rmtp_stream,district_id,cam_name+'.stream')
    print(full_rmtp_url)
    video_id = district_id + "_" + cam_name
    dur = args.duration
    segment_time = args.segment_time
    
    while(True):
        usec_time = str(round(time.time() * 1000))    
        print("Iteration @ USEC time: {}".format(usec_time))
        fname = 'caltran_' + video_id + '_usec_' + usec_time + '_%01d' + '.mp4'
        clips_fname = 'clips_'+str(usec_time)+'.csv'
        subprocess.call(['ffmpeg','-t',str(dur),
                         '-i', full_rmtp_url,'-c','copy','-flags','global_header',
                         '-f','segment',
                         '-segment_time',str(segment_time),
                         '-segment_atclocktime','1',
                         '-reset_timestamps','1',
                         '-segment_list',clips_fname, fname])
        all_files = pd.read_csv(clips_fname, header = None)
        all_files.columns = ['vid_name','start_time','end_time']
        
        for fname in all_files.vid_name:
            folder_name = district_id + "_" + cam_name
            gcs_path = os.path.join('gs://w251-accident-detection/caltran',folder_name,fname)
            subprocess.call(['gsutil','cp',fname,gcs_path])
            print('{} saved into GCS at location {}'.format(fname,gcs_path))
            os.remove(fname)
        
        map_csv = 'caltran_' + video_id + '_usec_' + usec_time + '.csv'
        gcs_path = os.path.join('gs://w251-accident-detection/caltran/index_maps',folder_name,map_csv)
        subprocess.call(['gsutil','cp',clips_fname,gcs_path])
        os.remove(clips_name)
        print("Removing local files - mp4 and index files.")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        

if __name__ == "__main__":
   main(sys.argv[1:])