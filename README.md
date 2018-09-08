# Video Frame Remover
## Remove frames and borders around videos

### Features:
- Works with both static and dynamically moving borders
- Preserves resolution

### Installation:

`conda create --name vfr --file spec-file.txt`
`source activate vfr`

### Usage example:

`(vfr)$ python video_frame_remover.py -i test_videos/test_video_0.mp4 -o out/test_video_0_out.mp4`

### Example outputs:

| Input  |  Output |
|---|---|
| ![alt text](https://github.com/alexkimxyz/video_frame_remover/blob/master/img_examples/0.png)  |  ![alt text](https://github.com/alexkimxyz/video_frame_remover/blob/master/img_examples/0_out.png) |
| ![alt text](https://github.com/alexkimxyz/video_frame_remover/blob/master/img_examples/1.png)  |  ![alt text](https://github.com/alexkimxyz/video_frame_remover/blob/master/img_examples/1_out.png) |
| ![alt text](https://github.com/alexkimxyz/video_frame_remover/blob/master/img_examples/2.png)  |  ![alt text](https://github.com/alexkimxyz/video_frame_remover/blob/master/img_examples/2_out.png) |


