# ytdl

Yet another CLI based YouTube downloader tool for linux.


[![PyPI version](https://badge.fury.io/py/ytdl.svg)](https://badge.fury.io/py/ytdl)
[![Build Status](https://travis-ci.org/ndaidong/ytdl.svg?branch=main)](https://travis-ci.org/ndaidong/ytdl)
[![Coverage Status](https://coveralls.io/repos/github/ndaidong/ytdl/badge.svg?branch=main)](https://coveralls.io/github/ndaidong/ytdl?branch=main)


### Features:

- Download only neccessary stream, not the whole video
- Download all videos or audios belong to a playlist
- Download with custom name and bounding

Just gather your favourite videos into a playlist, then let's `ytdl` download them overnight.


## Prerequisites

- Fedora 32+, Ubuntu 20+, Debian 10+
- [python](https://www.python.org/) 3.6.5 or newer
- [ffmpeg](https://ffmpeg.org/) 4.0 or newer
- [YouTube API key](https://developers.google.com/youtube/registering_an_application)


## Install


Recommend to use [pipx](https://pipxproject.github.io/pipx/):

```bash
pipx install ytdl
ytdl config
```

However, `pip` may work too:


```bash
pip install ytdl

# don't
sudo pip install ytdl
```

Build from source requires [poetry](https://python-poetry.org/):

```bash
git clone git@github.com:ndaidong/ytdl.git && cd ytdl
poetry install

# use raw script
poetry run python main.py info
poetry run python main.py [command] [arguments]

# build wheel to `./dist` folder
poetry build

# then install it
pipx install dist/ytdl-VERSION-py3-none-any.whl

# test it
ytdl info
```


## CLIs

### Basic commands

| Command | Description | Shortcut |
|--|--|--|
| `ytdl config KEY VALUE` | Set config value | `c` |
| `ytdl config KEY` | Show config property |
| `ytdl playlist PLAYLIST_URL` | Get playlist index | `p` |
| `ytdl video VIDEO_URL` | Download a video | `v` |
| `ytdl audio VIDEO_URL` | Download audio only | `a` |

Almost cases, `VIDEO_URL` and `PLAYLIST_URL` can be replaced with video ID or playlist ID.


### Advanced usage


#### Config

There are 2 properties to configure: `api_key` and `store_dir`.
At the first time, `api_key` is empty and you have to set it before using other features.

```bash
# set new `api_key`
ytdl config api_key YOUR_OWN_YOUTUBE_API_KEY

# change `store_dir` to new path
ytdl config store_dir /storage/downloads/youtube

# get the current value of `api_key`
ytdl config api_key

# show all
ytdl config
```

By default, `store_dir` is being set to `/home/{YOUR_USER_NAME}/ytdl_files`, you should change it to more appropriate place.


#### Playlist

Note that this command does not download actual video/audio, but a list of indexed items.

```bash
# get playlist metadata into `{store_dir}/{title}.json`
# this file contains a list of videos with their ID and title to download later
ytdl playlist https://www.youtube.com/playlist?list=PLAYLIST_ID

# get playlist metadata into `{store_dir}/my_custom_playlist_name.json`
ytdl playlist https://www.youtube.com/playlist?list=PLAYLIST_ID my_custom_playlist_name
```

For example if we download the playlist [Linux Tips and Tricks](https://www.youtube.com/playlist?list=PLSmXPSsgkZLsw-vEwve1O7w-Row9TIVqi)

The indexed file looks like below:

![](https://imgshare.io/images/2020/08/31/playlist-indexed.png)

Then we will have some powerful ways to download the videos in this list with `ytdl video` or `ytdl audio`.


#### Video

Download a single video file.

```bash
# download a video file to `{store_dir}/video/{VIDEO_TITLE}.mp4`
ytdl video https://www.youtube.com/watch?v=VIDEO_ID

# custom name
ytdl video https://www.youtube.com/watch?v=VIDEO_ID my_custom_video_name

```

To download multi items from indexed playlist, please refer the following arguments:

- `--index_file`: path to playlist index file (required)
- `--since`: video ID of the video where you want to start downloading from
- `--limit`: number of items to download, count from `since` or the begining of the list
- `--prefix_name`: to auto naming downloaded file
- `--prefix_num`: to auto naming downloaded file

Examples:

```bash
# download all videos from saved playlist index file above
# these video files will be stored in `{store_dir}/video`
ytdl video --index_file "/path/to/Linux Tips and Tricks.json"

# download 5 videos from saved playlist index file above, since first item
ytdl video --index_file "/path/to/Linux Tips and Tricks.json" --limit 5

# download 5 videos from saved playlist index file above, with prefix name
ytdl video --index_file "/path/to/Linux Tips and Tricks.json" --limit 5 --prefix_name "Linux Tutorial"
# downloaded videos should look like "Linux Tutorial - 1.mp4", "Linux Tutorial - 2.mp4" and so on
# prefix_name will be useful when you want to put these files into an already created list for your different purpose

# download 5 videos from saved playlist index file above, with prefix name and prefix number
ytdl video --index_file "/path/to/Linux Tips and Tricks.json" --limit 5 --prefix_name "Linux Tutorial" --prefix_num 25
# this will be useful for the playlists those are splited to multi parts
# in this case, your serie "Linux Tutorial" had already 24 items before, now count from 25 onwards
# downloaded videos should look like "Linux Tutorial - 25.mp4", "Linux Tutorial - 26.mp4" and so on

# similar to above command, but start from given item
ytdl video --index_file "/path/to/Linux Tips and Tricks.json" --since VIDEO_ID --limit 5 --prefix_name "Linux Tutorial" --prefix_num 25
```

While downloading video, the stream with highest `resolution` will be selected.


#### Audio

This is similar to `ytdl video`, but only download audio file.
While downloading, the stream with highest `abr` (average bitrate) will be selected.



```bash
# download a audio file to `{store_dir}/audio/{VIDEO_TITLE}.mp3`
ytdl audio https://www.youtube.com/watch?v=VIDEO_ID

# custom name
ytdl audio https://www.youtube.com/watch?v=VIDEO_ID my_custom_audio_name
```

To download multi items from indexed playlist, please refer the following arguments:

- `--index_file`: path to playlist index file (required)
- `--since`: video ID of the video where you want to start downloading from
- `--limit`: number of items to download, count from `since` or the begining of the list
- `--prefix_name`: to auto naming downloaded file
- `--prefix_num`: to auto naming downloaded file


Examples:

```bash
# download all audios from saved playlist index file above
# these audio files will be stored in `{store_dir}/audio`
ytdl audio --index_file "/path/to/Linux Tips and Tricks.json"

# download 5 audios from saved playlist index file above, since first item
ytdl audio --index_file "/path/to/Linux Tips and Tricks.json" --limit 5

# download 5 audios from saved playlist index file above, with prefix name
ytdl audio --index_file "/path/to/Linux Tips and Tricks.json" --limit 5 --prefix_name "Linux Tutorial"
# downloaded audios should look like "Linux Tutorial - 1.mp3", "Linux Tutorial - 2.mp3" and so on
# prefix_name will be useful when you want to put these files into an already created list for your different purpose

# download 5 audios from saved playlist index file above, with prefix name and prefix number
ytdl audio --index_file "/path/to/Linux Tips and Tricks.json" --limit 5 --prefix_name "Linux Tutorial" --prefix_num 25
# this will be useful for the playlists those are splited to multi parts
# in this case, your serie "Linux Tutorial" had already 24 items before, now count from 25 onwards
# downloaded audios should look like "Linux Tutorial - 25.mp3", "Linux Tutorial - 26.mp3" and so on

# similar to above command, but start from given item
ytdl audio --index_file "/path/to/Linux Tips and Tricks.json" --since VIDEO_ID --limit 5 --prefix_name "Linux Tutorial" --prefix_num 25
```

Downloaded stream will be converted to .mp3 with `ffmpeg`.


## Dependencies

This lib was built on top of the following packages:

| Dependency | License |
|--|--|
| [pytube3](https://github.com/get-pytube/pytube3) | MIT |
| [python-youtube](https://github.com/sns-sdks/python-youtube) | MIT |
| [python-fire](https://github.com/google/python-fire) | Apache License v2 |


## Test

```bash
git clone git@github.com:ndaidong/ytdl.git && cd ytdl
poetry install
YOUTUBE_API_KEY=your_own_key ./run_test.sh
```


# License

The MIT License (MIT)
