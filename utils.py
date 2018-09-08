import cv2
import imageio
import numpy as np


def auto_canny(image, sigma=0.3):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged


def resize_img(image, width=None, height=None, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized


def get_frames(vid_filename, n_sample_frames=100):
    vid = imageio.get_reader(vid_filename, 'ffmpeg')
    if n_sample_frames is None:
        nums = range(0, len(vid))
    else:
        nums = np.linspace(0, len(vid) - n_sample_frames, n_sample_frames, dtype=int)
    frames = []
    for num in nums:
        try:
            image = vid.get_data(num)
        except RuntimeError:
            pass
        frames.append(image)
    return np.array(frames)


def get_median_frame(frames):
    median_frame = np.median(frames, axis=0)
    return median_frame


def get_stdev_frame(frames):
    stdev_frame = np.std(frames, axis=0)
    return stdev_frame


def get_frame_box_coords(input_frame, sz=300, min_area_ratio=0.2, max_area_ratio=0.9, pad=5):
    ratio = input_frame.shape[0] / float(sz)
    input_frame_resized = resize_img(input_frame, height=sz)
    input_frame_resized = input_frame_resized.astype(np.uint8)
    total_area = input_frame_resized.shape[0] * input_frame_resized.shape[1]
    color = [255, 255, 255]
    input_frame_padded = cv2.copyMakeBorder(input_frame_resized, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=color)
    gray = cv2.cvtColor(input_frame_padded, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 10, 10, 10)
    edged = auto_canny(gray, sigma=0.9)
    _, contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None
    area_lst = []
    rect_coord_lst = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        area = w * h
        if min_area_ratio * total_area < area < max_area_ratio * total_area:
            area_lst.append(w * h)
            x0 = max(0, x - pad)
            y0 = max(0, y - pad)
            rect_coord_lst.append(np.array([x0, y0, w, h]))

    if len(area_lst) == 0:
        return None
    max_idx = np.array(area_lst).argmax()
    rect = rect_coord_lst[max_idx]
    x0, y0, width, height = (rect * ratio).astype(int)
    return x0, y0, width, height
