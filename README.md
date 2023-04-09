# mot2yolo
Convert the gt.txt files of all MOT sequences to YOLO format an coexist in a folder

### MOT format
```
<frame_id>,<track_id>,<x_top_left>,<y_top_left>,<width>,<height>,<1>,<class_id>,<0>
```

### YOLO format
```
<class_id> <x_center> <y_center> <width> <height>
```
