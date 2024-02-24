"""
Use Pytube (https://github.com/pytube/pytube)

# download Pytube
$ python -m pip install pytube

# example direct download
$ pytube https://youtube.com/watch?v=2lAe1cqCOXo

# require ffmpeg for merging video and audio
reference: https://ffmpeg.org/

Implement simple code to get highest quality VIDEO and AUDIO
"""

from pytube import YouTube

import argparse # to get arguments using pattern
import sys # to get arguments (parameter) manually

import subprocess # to run ffmpeg
import os # delete file os.remove()

# from pprint import pp

def on_progress_callback(stream, data, remainingByte):
    # print(f"Downloaded: {stream.filesize} bytes, remaining: {remainingByte} bytes")

    # print info in the same line and replacing previous content (on this line)
    print(f"\r.. remaining: {remainingByte:,} bytes", end="\r", flush=True)

def on_complete_callback(stream, filePath):
    print(f"Download complete: {filePath}")


def downloadYouTube(ytURL = None):

    if ytURL is None:
        return
    
    yt = YouTube(ytURL,
            on_progress_callback=on_progress_callback,
            on_complete_callback=on_complete_callback,
            use_oauth=True,
            allow_oauth_cache=True
    )

    if yt is None:
        print(f"Error, please make sure the YouTube URL is valid.")
        return
    
    print(f"Title: {yt.title}")


    displayStreams = False
    if displayStreams:
        print('-------------- stream list ----------')

        #query streams that has both video and audio
        #yt.streams.filter(progressive=True)

        for stream in yt.streams:
            print(stream)

        """
        sample list:
        <Stream: itag="18" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">
        <Stream: itag="22" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">
        <Stream: itag="337" mime_type="video/webm" res="2160p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="336" mime_type="video/webm" res="1440p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="335" mime_type="video/webm" res="1080p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="136" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.4d401f" progressive="False" type="video">
        <Stream: itag="247" mime_type="video/webm" res="720p" fps="30fps" vcodec="vp9" progressive="False" type="video">
        <Stream: itag="334" mime_type="video/webm" res="720p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="135" mime_type="video/mp4" res="480p" fps="30fps" vcodec="avc1.4d401f" progressive="False" type="video">
        <Stream: itag="244" mime_type="video/webm" res="480p" fps="30fps" vcodec="vp9" progressive="False" type="video">
        <Stream: itag="333" mime_type="video/webm" res="480p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="134" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.4d401e" progressive="False" type="video">
        <Stream: itag="243" mime_type="video/webm" res="360p" fps="30fps" vcodec="vp9" progressive="False" type="video">
        <Stream: itag="332" mime_type="video/webm" res="360p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="133" mime_type="video/mp4" res="240p" fps="30fps" vcodec="avc1.4d4015" progressive="False" type="video">
        <Stream: itag="242" mime_type="video/webm" res="240p" fps="30fps" vcodec="vp9" progressive="False" type="video">
        <Stream: itag="331" mime_type="video/webm" res="240p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="160" mime_type="video/mp4" res="144p" fps="30fps" vcodec="avc1.4d400c" progressive="False" type="video">
        <Stream: itag="278" mime_type="video/webm" res="144p" fps="30fps" vcodec="vp9" progressive="False" type="video">
        <Stream: itag="330" mime_type="video/webm" res="144p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">
        <Stream: itag="139" mime_type="audio/mp4" abr="48kbps" acodec="mp4a.40.5" progressive="False" type="audio">
        <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">
        <Stream: itag="249" mime_type="audio/webm" abr="50kbps" acodec="opus" progressive="False" type="audio">
        <Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus" progressive="False" type="audio">
        <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">
        """
        print('------ end stream list ----------')
    

    # for details which stream is suitable: https://pytube.io/en/latest/user/streams.html
    # NOTES:
    # a. some streams have both Audio and Video, some others are separated stream !
    # b. Normally only 720p or lower resolution has both Audio and Video in 1 stream !
    # c. see list of stream's tag (code): https://gist.github.com/AgentOak/34d47c65b1d28829bb17c24c04a0096f


    # select HIGHEST audio resolution
    audioStreams = yt.streams.filter(type="audio").order_by('abr').desc()
    streamHighestAudio = yt.streams.get_by_itag(audioStreams[0].itag)
    # <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">

    # select HIGHEST video resolution
    testingDownloadOnly1080p = False
    if testingDownloadOnly1080p:
        # for testing, just using 1080p (smaller than 2160p)
        streamHighestVideo = yt.streams.filter(type="video", resolution="1080p")[0]
    else:
        videoStreams = yt.streams.filter(type="video").order_by('resolution').desc()
        streamHighestVideo = yt.streams.get_by_itag(videoStreams[0].itag)
        # <Stream: itag="337" mime_type="video/webm" res="2160p" fps="60fps" vcodec="vp9.2" progressive="False" type="video">

    

    # download both audio and video

    # first download audio because it is smaller and shorter time to download
    fileAudio = downloadStream(streamHighestAudio)

    # then download the video
    fileVideo = downloadStream(streamHighestVideo)
    
    result = mergeVideoAudio(fileVideo, fileAudio, f"{yt.title}.mp4")
    if result is None or result == 0:
        # delete temporary files
        os.remove(fileAudio)
        os.remove(fileVideo)


def mergeVideoAudio(fileVideo, fileAudio, outputFilename = None):
    print(f"Going to merge '{fileVideo = }' and '{fileAudio = }'")

    if outputFilename is None:
        outputFilename = f"{fileVideo}.mp4"

    # merge using ffmpeg, note: use double-quote for filename (because it may contains space)
    cmd = f'ffmpeg -i "{fileVideo}" -i "{fileAudio}" -c:v copy -map 0:v -map 1:a -y "{outputFilename}"'
    print(f"going to run command: {cmd}")

    return_value = subprocess.call(cmd, shell=True)

    print(f"subprocess return: {return_value}")

    return return_value

def downloadStream(stream):

    if stream is None:
        print('Error, no stream is provided')
        return None

    filename = None

    codec = stream.codecs[0]
    match codec:
        case s if s.startswith('vp9'):
            # video
            filename = generateFilenameFromStream(stream)
        case s if s.startswith('mp4'):
            # could be VIDEO or AUDIO
            filename = generateFilenameFromStream(stream)
        case s if s.startswith('opus'):
            # audio            
            filename = generateFilenameFromStream(stream)
        case _:
            print(f"Error, unhandled stream codec")

    if filename:
        print(f'Filename: {filename}')
        print(f'Filesize: {stream.filesize:,}')
        
        stream.download(filename=filename)
        print(f"Downloaded !!")
    
    return filename

def generateFilenameFromStream(stream):
    filename = f"{stream.title}.{stream.itag}.{stream.mime_type.replace('/', '-')}.temp"
    return filename

if __name__ == "__main__":

    # parse youtube URL
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument(
    #     "--url", help="YouTube URL"
    # )
    # args = vars(argparser.parse_args())
    # match args.__len__:
    #     case 1:
    #         ytURL = args["url"]
    #         print(f"YouTube URL: {ytURL}")

    #         downloadYouTube(ytURL)
        
    #     case _:
    #         print(f"Please provide parameter, ie: 'https://youtube.com/dummyabc'")


    if len(sys.argv) == 2:
        downloadYouTube(sys.argv[1])
        print(f"*** Download successful, the end ***")
    else:
        print(f"Please provide parameter, ie: 'https://youtube.com/dummyabc'")

    
