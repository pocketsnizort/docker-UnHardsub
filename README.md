# docker-UnHardsub
a docker for removing hardsubbed part of videos


How to use
==========

It requires to have both a subtitled video and a reference one (without subs)

```
docker run \
--rm -it \
-v /raw.mkv:/input/raw.mkv \
-v /hardsub.mp4:/input/hardsud.mp4 \
-v /outputdir:/output \
unhardsub \
'vspipe --y4m -a hardsubedded_video="/input/hardsud.mp4" -a raw_video="/input/raw.mkv" -a crop="[284,874,1350,150]" -a timecodes="[(0, -26), (14524, -40)]" /usr/share/vsscripts/unhardsub.vpy - | ffmpeg -i pipe: <MyParam> /output/output.mp4'
```

Some explaination:
- `--rm` to delete the container after it has finished, because this container is more of a "launched manually" than a real service. It will NOT delete the data present in you mounted volumes.
- `-it` may be necessary for ffmpeg feedback ?
- `-v /raw.mkv:/input/raw.mkv` mount raw video
- `-v /outputdir:/output` mount the output dir
- `-v /hardsub.mkv:/input/hardsub.mkv` mount hardsub video

And for the vapoursynth arguments:
- `-a hardsubedded_video="/input/hardsud.mp4"` to specify hardsubbed input
- `-a raw_video="/input/raw.mkv"` to specify raw input (without subs)
- `-a crop="[284,874,1350,150]"` to specify a rectangle where to expect subtitles. format is [pos_x, pos_y, width, height].
- `-a timecodes="[(0, -26), (14524, -40)]"` to specify when to delay one video or another. it is a list of tuples where the first part is the frame from which the delay is apply, and the second is the delay in frames relative from the hardsubbed video.

Also, do not forget the simple quotes in the docker command, without them, you will pipe to the hosts' ffmpeg (if any).