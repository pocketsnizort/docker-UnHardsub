#hardsubedded_video="video1.mp4" #Hardsubbed video from which you wish to retain most data
#raw_video="video2.mkv" #Raw video from which subtitle parts will be replaced
#crop="[284,874,1350,150]" #position and dimention of the cropping box [x_pos, y_pos, width, height]
#timecodes="[(0, -26), (14524, -40)]" #Timecode of delays between the two clips, understood as a list of couple (timecode, delay) both in frames

crop_x, crop_y, crop_w, crop_h = crop.decode("utf-8")[1:-1].split(",")

crop_x = int(crop_x)
crop_y = int(crop_y)
crop_w = int(crop_w)
crop_h = int(crop_h)
timecodes = eval(timecodes.decode("utf-8"))

import vapoursynth as vs
from kagefunc import hardsubmask

core=vs.get_core()
hclip=core.ffms2.Source(source=hardsubedded_video.decode("utf-8"))
rclip=core.ffms2.Source(source=raw_video.decode("utf-8"))


#Apply timecodes of delay
new_rclip = rclip

for frame, delay in timecodes:
    if delay < 0:
        #reduce length of the raw clip
        if frame > 0:
            new_rclip = core.std.Splice([core.std.Trim(clip=new_rclip, last=frame - 1), core.std.Trim(clip=new_rclip, first=frame - delay)])
        else:
            new_rclip = core.std.Trim(clip=rclip, first=-delay)
    elif delay > 0:
        #lengthen raw clip with parts of hardseubbed clip
        if frame > 0:
            new_rclip = core.std.Splice([core.std.Trim(clip=new_rclip, last=frame - 1), core.std.Trim(clip=hclip, first=frame, length=delay), core.std.Trim(clip=new_rclip, first=frame)])
        else:
            new_rclip = core.std.Splice([core.std.Trim(clip=hclip, first=0, length=delay), rclip])

rclip = new_rclip
    
crop_hclip = core.std.CropAbs(clip=hclip,width=crop_w,height=crop_h,left=crop_x,top=crop_y)
crop_rclip = core.std.CropAbs(clip=rclip,width=crop_w,height=crop_h,left=crop_x,top=crop_y)

crop_mclip=hardsubmask(crop_hclip, crop_rclip)
mclip = core.std.AddBorders(clip=crop_mclip, left=crop_x, right=hclip.width - crop_w - crop_x, top=crop_y, bottom=hclip.height - crop_h - crop_y)

cclip = core.std.MaskedMerge(clipa=hclip, clipb=rclip, mask=mclip, first_plane=1)

cclip.set_output()

