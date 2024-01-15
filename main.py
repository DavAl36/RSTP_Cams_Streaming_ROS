'''
Enable the RSTP server with the following docker
docker run --rm -it -e RTSP_PROTOCOLS=tcp -p 8554:8554 aler9/rtsp-simple-server

https://github.com/MaxDam/iot_experiments/tree/main/rtsp_producer_consumer_basic
https://www.youtube.com/watch?v=0waGEDZSFQs
https://trac.ffmpeg.org/wiki/Encode/H.264
https://ffmpeg.org/ffmpeg-formats.html
Parameters Mean
https://www.bannerbear.com/blog/ffmpeg-101-top-10-command-options-you-need-to-know-with-examples/#size--s

Speed Up/Down video
https://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video
Latency 
https://trac.ffmpeg.org/wiki/StreamingGuide#Latency

How choose the following parameters: -b:v, -preset, -maxrate, -bufsize and -g
https://superuser.com/questions/945413/how-to-consider-bitrate-maxrate-and-bufsize-of-a-video-for-web
https://trac.ffmpeg.org/wiki/Limiting%20the%20output%20bitrate
https://trac.ffmpeg.org/wiki/EncodingForStreamingSites
https://trac.ffmpeg.org/wiki/Limiting%20the%20output%20bitrate
'''


import cv2
import subprocess as sp

######################################################### GENERAL CONFIGURATIONS #########################################################

output_framerate = 24 # ffmpeg -r parameter
g = output_framerate * 2 # ffmpeg -g parameter

# maxrate / bufsize must be a value between 1 and 2
bv = '4M' # ffmpeg -b:v parameter
maxrate = '64M'
bufsize = '64M'
#preset = 'ultrafast'
video_size = '640x640'
filterv = 'setpts=1.5*PTS' # speeding up/down stream
######################################################### STREAM CAM 1 #########################################################

rtsp_server_cam1 = 'rtsp://localhost:8554/cam1'
#cap_cam1 = cv2.VideoCapture("/dev/video0")
#sizeStr_cam1 = str(int(cap_cam1.get(cv2.CAP_PROP_FRAME_WIDTH))) + 'x' + str(int(cap_cam1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#fps_cam1 = int(cap_cam1.get(cv2.CAP_PROP_FPS))


command_cam1 = ['ffmpeg',
            '-i', '/dev/video0', 
            #'-filter:v', filterv,
            '-s', video_size,  
            '-r', str(output_framerate),
            '-g', str(g),
            '-b:v', bv,
            '-bufsize', bufsize,
            '-maxrate', maxrate,
            '-rtsp_transport', 'tcp',
            '-f', 'rtsp',
            rtsp_server_cam1]
'''
command_cam1 = ['ffmpeg',
            '-re',
            '-s', video_size,
            '-i', '-',               
            '-pix_fmt', 'yuv420p', #https://ffmpeg.org/pipermail/ffmpeg-devel/2007-May/035617.html
            '-r', str(output_framerate),  # output fps
            '-g', str(g),
            '-c:v', 'libx264',
            '-b:v', bv,
            #'-fflags','nobuffer',
            '-bufsize', bufsize,
            '-maxrate', maxrate,
            '-preset', preset,
            '-rtsp_transport', 'tcp',
            #'-segment_times', '5',# 2 default
            '-f', 'rtsp',
            rtsp_server_cam1]
'''
process_cam1 = sp.Popen(command_cam1, stdin=sp.PIPE)

######################################################### STREAM CAM 2 #########################################################

rtsp_server_cam2 = 'rtsp://localhost:8554/cam2'

#cap_cam2 = cv2.VideoCapture("/dev/video2")
#sizeStr_cam2 = str(int(cap_cam2.get(cv2.CAP_PROP_FRAME_WIDTH))) + 'x' + str(int(cap_cam2.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#fps_cam2 = int(cap_cam2.get(cv2.CAP_PROP_FPS))

command_cam2 = ['ffmpeg',
            '-i', '/dev/video2',
            #'-filter:v', filterv,   
            '-r', str(output_framerate),
            '-g', str(g),
            '-b:v', bv,
            '-bufsize', bufsize,
            '-maxrate', maxrate,
            '-rtsp_transport', 'tcp',
            '-f', 'rtsp',
            rtsp_server_cam2]

process_cam2 = sp.Popen(command_cam2, stdin=sp.PIPE)

######################################################### STREAMING CAMS #########################################################

while(cap_cam1.isOpened()): 

    _, frame_cam1 = cap_cam1.read()
    _, frame2_cam1 = cv2.imencode('.png', frame_cam1)
    process_cam1.stdin.write(frame2_cam1.tobytes())
    
    _, frame_cam2 = cap_cam2.read()
    _, frame2_cam2 = cv2.imencode('.png', frame_cam2)
    process_cam2.stdin.write(frame2_cam2.tobytes())
    


