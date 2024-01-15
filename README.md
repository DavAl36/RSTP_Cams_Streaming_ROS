# RSTP_Cams_Streaming_ROS

### Description

Stream the N cameras using rstp server.

### Instructions

List of available cameras

```shell
sudo apt-get install v4l-utils
v4l2-ctl --list-devices
```

Run the docker image of rstp server 

```shell
docker run --rm -it -e RTSP_PROTOCOLS=tcp -p 8554:8554 aler9/rtsp-simple-server
```

Run python script to enable the streaming

```shell
python main.py
```

Open rstp link with vlc to see the video.

### References

Bitrate parameters: [link1](https://superuser.com/questions/945413/how-to-consider-bitrate-maxrate-and-bufsize-of-a-video-for-web), [link2](https://trac.ffmpeg.org/wiki/Limiting%20the%20output%20bitrate), [link3](https://trac.ffmpeg.org/wiki/EncodingForStreamingSites), [link4](https://trac.ffmpeg.org/wiki/Limiting%20the%20output%20bitrate).
[Github reference Code](https://github.com/MaxDam/iot_experiments/tree/main/rtsp_producer_consumer_basic)
[Youtube](https://www.youtube.com/watch?v=0waGEDZSFQs)



