# What is youtube_backup
A simple tool that use pytube (https://github.com/pytube/pytube) to make backup of self-own video that has been uploaded to YouTube as Public (every one can search and see) or Unlisted (not searchable but only people with the link can see it)

# Problem to solve
pytube is easy to use, but running pytube directly from command line like:
```
pytube https://youtube.com/watch?v=2lAe1cqCOXo
```
Only able to download an 720p video, 720p is the highest resolution downloadable video with audio.

# Solution
Using this simple python code to download (for backup) self-own video using the highest possible quality.

# Requirement
1. Python v3.x (https://www.python.org/)
2. Pytube v15.0 (https://github.com/pytube/pytube)
3. FFMPEG v6.0 (https://ffmpeg.org/)

# How to use
Using command line (CLI)
```
python3 youtube_backup.py https://youtube.com/watch?v=2lAe1cqCOXo
```

# Limitation
1. Only download to the current directory.
2. Downloaded filename will only use .mp4 extension

# Warning
Because will use highest possible video quality, therefore the output file size will be ver large, downloaded file size can easily be more than 1GB for a 2160p (4K) video.
