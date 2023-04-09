import os
import os.path as osp
from tqdm import tqdm
from io import StringIO
'''
将mot的gt标签批量转换为yolo的标签
每个序列的图片必须以帧数命名
'''

def save_txt(str_list: list, name):
    with open(name, 'w', encoding='utf-8') as f:
        for i in str_list:
            f.write(i + '\n')

def read_text(file_path):
    item_list = []
    with open(file_path,'r',encoding='utf-8') as file:
        file_content = file.read()
    with StringIO(file_content) as f:
        for line in f:
            item_list.append(line.rstrip('\n\r'))
    return item_list

def main():

    # 输入输出路径
    input = 'work_dir'                     # 输入文件夹路径
    output = 'output_file'                 # 输出文件夹路径
    sets = ['train', ]
    video_folders = list()


    for subset in sets:
        in_folder = osp.join(input, subset)
        video_names = os.listdir(in_folder)  # 得到输入下视频文件夹的名称
        # 得到视频路径并排列
        for video_name in video_names:
            video_folder = osp.join(in_folder, video_name)  # 得到视频的路径
            infos = read_text(f'{video_folder}/seqinfo.ini')
            assert video_name == infos[1].strip().split('=')[1]
            video_folders.append(video_folder)
            video_folders = sorted(video_folders)

        for video_folder in video_folders:  # 选择视频文件夹
            video_name = video_folder.strip().split('/')[-1]
            print(end='\n')
            print(f"处理视频序列{video_name}")
            infos = read_text(f'{video_folder}/seqinfo.ini')
            img_folder = infos[2].strip().split('=')[1]
            width = int(infos[5].strip().split('=')[1])
            height = int(infos[6].strip().split('=')[1])
            img_folder_path = osp.join(video_folder,img_folder)
            gts = read_text(f'{video_folder}/gt/gt.txt')  # 读取标签的信息
            imgs = sorted(os.listdir(img_folder_path))
            for img_name in tqdm(imgs):
                img_frame_id = img_name.strip().split('.')[0]
                img_frame_id = int(img_frame_id)
                yolo_file = list()
                for k in range(len(gts)):
                    gt = gts[k]
                    if img_frame_id  == int(float(gt.split(',')[0])):
                        x1 = float(gt.split(',')[2])
                        y1 = float(gt.split(',')[3])
                        x_width = float(gt.split(',')[4])
                        y_height = float(gt.split(',')[5])
                        label = int(gt.split(',')[7]) - 1
                        x_c = x1 + 0.5 * x_width
                        y_c = y1 + 0.5 * y_height
                        rela_x_c = x_c / width
                        rela_y_c = y_c / height
                        rela_x_width = x_width / width
                        rela_y_heigth = y_height / height
                        yolo_info = f'{label} {rela_x_c} {rela_y_c} {rela_x_width} {rela_y_heigth}'
                        yolo_file.append(yolo_info)
                if not os.path.exists(output):
                    os.makedirs(output)
                save_txt(yolo_file, f'{output}/{video_name}{img_frame_id:04d}.txt')


if __name__ == '__main__':
    main()
