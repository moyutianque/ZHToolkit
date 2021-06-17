import os
import json
import sys
from pytube import YouTube
import os.path as osp
from multiprocessing import Pool,cpu_count

dataset_root='./'
video_dwn = './raw_video'
annotations=json.load(open(osp.join(dataset_root, 'violin_annotation.json')))

from tqdm import tqdm

def download(youtube_id:str, file_name:str):
    try:
        yt = YouTube(f'https://youtube.com/watch?v={youtube_id}')
        yt.streams.filter(progressive=True).order_by('resolution').desc().first().download(output_path=video_dwn, filename=file_name)
    except:
        with open('./missing_videos.log','a') as f:
            f.write(f"{file_name}\t{youtube_id}\n")
        print(f'[warning] Cannot download {file_name} from id {youtube_id}')

p = Pool(cpu_count())

for i, (k,v) in enumerate(tqdm(annotations.items())):
    file_name = v['file'].strip()
    youtube_id = v['source'].strip()
    p.apply_async(download, args=(youtube_id, file_name,))

p.close()
p.join()
