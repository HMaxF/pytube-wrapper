# What is pytube-wrapper
A wrapper to use pytube from https://github.com/pytube/pytube to download YouTube video.


# Problem to solve
pytube is easy to use, but running pytube directly from command line like:
```
$ pytube https://youtube.com/watch?v=2lAe1cqCOXo
```
Only able to download an 720p video, this is resolution is the highest downloadable video with audio.

# Solution
Using a simple python code to download a YouTube video using the highest possible video and audio.

# Requirement
1. Python v3.x (https://www.python.org/)
2. Pytube v15.0 (https://github.com/pytube/pytube)
3. FFMPEG v6.0 (https://ffmpeg.org/)

# How to use
Using command line (CLI)
```
$ python3 pytube-wrapper.py https://youtube.com/watch?v=2lAe1cqCOXo
```

# Limitation
1. Only download to the current directory.
2. Downloaded filename will only use .mp4 extension

# Warning
Because will use highest possible video quality, therefore the output file size will be large.  


To download 2160p (4K) video, the file size may be more than 1 GB