'''
Enable the RSTP server with the following docker
docker run --rm -it -e RTSP_PROTOCOLS=tcp -p 8554:8554 aler9/rtsp-simple-server

https://github.com/MaxDam/iot_experiments/tree/main/rtsp_producer_consumer_basic
https://www.youtube.com/watch?v=0waGEDZSFQs
https://trac.ffmpeg.org/wiki/Encode/H.264
https://ffmpeg.org/ffmpeg-formats.html
Parameters Mean
https://www.bannerbear.com/blog/ffmpeg-101-top-10-command-options-you-need-to-know-with-examples/#size--s
Bitrate Instructions
https://superuser.com/questions/945413/how-to-consider-bitrate-maxrate-and-bufsize-of-a-video-for-web
https://trac.ffmpeg.org/wiki/Limiting%20the%20output%20bitrate
'''


import cv2
import subprocess as sp

#rtsp_server = 'rtsp://localhost:8554/mystream'
rtsp_server = 'rtsp://localhost:8554/mystream'



cap = cv2.VideoCapture("/dev/video0")
sizeStr = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + 'x' + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = int(cap.get(cv2.CAP_PROP_FPS))
    
command = ['ffmpeg',
            '-re',
            '-s', sizeStr,
            '-r', str(fps),  # rtsp fps (from input server)
            '-i', '-',
               
            # You can change ffmpeg parameter after this item.
            #-pix_fmt', 'yuv420p', #https://ffmpeg.org/pipermail/ffmpeg-devel/2007-May/035617.html
            '-r', '30',  # output fps
            '-g', '50',
            '-c:v', 'libx264',
            '-b:v', '2M',
            '-bufsize', '64M',
            '-maxrate', "4M",
            '-preset', 'ultrafast',#ultrafast #veryfast
            '-rtsp_transport', 'tcp',
            #'-segment_times', '5',# 2 default
            '-f', 'rtsp',
            rtsp_server]

process = sp.Popen(command, stdin=sp.PIPE)

while(cap.isOpened()):
    ret, frame = cap.read()
    ret2, frame2 = cv2.imencode('.png', frame)
    process.stdin.write(frame2.tobytes())

