# Requirements
1. Python 3.13+. Simply download the latest version from python.org
2. `yt-dlp`
3. `ffmpeg`
4. PDM (optional, but it'll make things easier)
5. GIT (optional)

All of these programs should already be installed and is available on your environment path.

PDM is a Package and Dependecy Manager for python. Read their [instructions](https://pdm-project.org/en/latest/#installation) on how to install it based on what your OS is.

Git is a version control software, check their [Installation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) page.

# Cloning the repository
Open cmd in the folder in which you want this repository to live in and type in:
```
git clone https://github.com/hemakodaa/multi-pov.git
```

# 'Offset' and 'Reference'
Think of **Offset** and **Reference** like **timezones**. If you live in New York, your timezone in terms of UTC is UTC-5. In this case, **Reference** is UTC and **offset** is that little **-5**. 

In this utility, **Reference** is the streamer/POV you're watching from and **Offset** is the timestamp in which **the same event** happened across **all** VODs. Practical example [below](#the-reference-streamer).

## the **Offset** file
The offset file **must be located inside `offset/` folder**, and the file itself contains 3 columns, separated by commas. Think of it as a CSV file, but it doesn't have to be `.csv`. As long as it's a text file, you're good.

Pay attention to the format:
```
streamer_name,timestamp,youtube_vod_link

Example:
erina,11:54,https://www.youtube.com/watch?v=o32Zq76Bf1U
```

**timestamp** is the time in which, across **all** VODs, **some event** happened. 

For example (this is from a Lockdown Protocol collab):

```
erina,11:54,https://www.youtube.com/watch?v=o32Zq76Bf1U
tenma,11:48,https://www.youtube.com/watch?v=DasbU_b2-7w
lia,11:56,https://www.youtube.com/watch?v=w2I65urGITI
iori,9:54,https://www.youtube.com/watch?v=db2wBGyvR-Q
panko,7:52,https://www.youtube.com/watch?v=NKxuD0o4mZM
```
if you open any of these links at the specific timestamps, it will lead to the same event happening across all VODs, in which Tenma speaks (or joke crying, in this case). 

This file will be used to calculate the appropriate offset for *any* section of the video you want to download.

## The **Reference** streamer
Say you're watching the Lockdown Protocol collab above from **Erina's perspective**, and something interesting happens. You may wonder *what is happening on the other streamers?*

In this example, Erina is the **Reference** streamer. You are watching the collab from **Erina's perspective** and you want to download this section of a video in which this event happened **alongside all the other POVs**. That's what this utility is for.

# Basic commands

**IMPORTANT: Change directory (`cd`) to multi_pov/cloned repository.**

If you have `pdm` installed, the base command is `pdm run main`. If you don't, the base command will be `python .\src\multi_pov\main.py`
## Bulk Downloads
Bulk downloads uses the offset file. 
- Start multi POV section downloads: 

`pdm run main -o offset_file.txt`
- Maximum resolution of 720p: 

`pdm run main -o offset_file.txt -p 720`
- Maximum of 2 parallel downloads: 

`pdm run main -o offset_file.txt -t 2`
- Change reference streamer to (name) :

`pdm run main -o offset_file.txt -r (name)`
- Download full vods concurrently

`pdm run main -o offset_file.txt --full`
- All the above at once: 

`pdm run main -o offset_file.txt -p 720 -t 2 -r (name) --full` <- the order doesn't matter for the options.

## Single downloads
- Download a section of a video

`pdm run main -s https://www.youtube.com/watch?v=w8DLUoEbtLk`

- Max resolution of 720p

`pdm run main -s https://www.youtube.com/watch?v=w8DLUoEbtLk -p 720`

- Download an entire video

`pdm run main -s https://www.youtube.com/watch?v=w8DLUoEbtLk --full`

- All the above at once

`pdm run main -s https://www.youtube.com/watch?v=w8DLUoEbtLk -p 720 --full`


# Options
```
> pdm run main
usage: multi-pov [-h] [-o OFFSETFILE] [-r REFERENCE] [-t THREADS]
                 [-p RESOLUTION] [-s SINGLE] [--full]

Download multiple POVs at once

options:
  -h, --help            show this help message and exit
  -o, --offsetfile OFFSETFILE
                        Filename of the offset file (include extension e.g.
                        .txt)
  -r, --reference REFERENCE
                        Set the reference streamer
  -t, --threads THREADS
                        Set the amount of parallel downloads (default=4)
  -p, --resolution RESOLUTION
                        Set the maximum resolution (default=1080)
  -s, --single SINGLE   Download single videos
  --full                Download full VODs.

```
## Reference
You can change who the reference is based on from which POV you're watching from. It will default to whoever is on the first line of the offset file.
## Threads
The maximum number of parallel downloads at any given time. `-t 1` is a sequential download. Defaults to 4.
## Resolution
Sets the **maximum** resolution, meaning it will download the specified resolution **or lower**. Defaults to 1080p.

# Section Download Interface
Section downloads for both single and bulk downloads are the same. Single downloads will have `single_download` as its default or you can change it via `-r` flag.
```
> pdm run main offset.txt

Reference streamer: iori
URL: https://www.youtube.com/watch?v=_EhQFt-Gv70

Streamers:
iori (REF)
tenma
uruka
michiru

Max resolution: 1080p

Start:
```

This is the main interface. You will input your `Start` and `End` timestamps when prompted. When you're done, a familiar console text will show up indicating `yt-dlp` is downloading the sections of the VOD.

```
Start: 10:00
End: 11:00
[youtube] Extracting URL: https://www.youtube.com/watch?v=0zaNppnzWrQ
[youtube] Extracting URL: https://www.youtube.com/watch?v=-bSnX_Fos0o
[youtube] 0zaNppnzWrQ: Downloading webpage
[youtube] -bSnX_Fos0o: Downloading webpage
[youtube] Extracting URL: https://www.youtube.com/watch?v=TRZZvakcss4
[youtube] TRZZvakcss4: Downloading webpage
[youtube] Extracting URL: https://www.youtube.com/watch?v=_EhQFt-Gv70
[youtube] _EhQFt-Gv70: Downloading webpage
```
It will show reports from all 4 parallel downloads.


