import os
import argparse
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop
from utils import get_frames, get_median_frame, get_frame_box_coords


def remove_frame(in_fname, out_fname, n_sample_frames=100):
    sample_frames = get_frames(in_fname, n_sample_frames)
    input_frame = get_median_frame(sample_frames)
    res = get_frame_box_coords(input_frame)
    if res is None:
        print("No border was detected in {}".format(in_fname))
        return None
    else:
        x, y, w, h = res
    clip = VideoFileClip(in_fname)
    crop_clip = crop(clip, x1=x, y1=y, x2=x + w, y2=y + h)
    crop_clip.write_videofile(out_fname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input video file path')
    parser.add_argument('-o', help='output video file path')
    args = parser.parse_args()
    out_dirname = os.path.dirname(args.o)
    if not os.path.isdir(out_dirname):
        os.mkdir(out_dirname)
    remove_frame(args.i, args.o)
