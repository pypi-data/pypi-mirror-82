mkvsubmerge
======

Split MKV file according to timestamp pairs specified by SRT
subtitle file and then merge into a new video file.

Requirements
------------

1. Python 3
2. MKVToolNix

Install
-------

Install latest version:

```bash
 pip install mkvsubmerge
```

Usage
-----

    usage: mkvsubmerge [-h] [-o OUT] [--srt SRT]
                       [--srt-encoding SRT_ENCODING]
                       [--start-offset START_OFFSET]
                       [--end-offset END_OFFSET]
                       mkv

    positional arguments:
      mkv                   MKV file

    optional arguments:
      -h, --help            show this help message and exit
      -o OUT                output MKV file
      --srt SRT             SRT file
      --srt-encoding SRT_ENCODING
                            SRT file encoding
      --start-offset START_OFFSET
                            offset to apply to every start
                            timestamp
      --end-offset END_OFFSET
                            offset to apply to every end
                            timestamp

About
-----

Med0paW

medopaw@gmail.com

https://github.com/medopaw
