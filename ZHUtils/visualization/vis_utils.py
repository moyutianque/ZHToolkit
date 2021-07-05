from PIL import ImageDraw, ImageFont
import numpy as np
from graphviz import Digraph
import cv2

def resize_box(box, scale):
    resized_box = box * scale
    return resized_box

def draw_single_box(pic, box, img_shape, color="#e04a3f", draw_info=None):
    """
        "blue and yellow": ["#3d6ec9", "#ffd04b"],
        "dark green and dark red": ["#00A13B", "#8B0000"],
        "light green and light red": ["#0dab62", "#e04a3f"],
    """
    img_w, img_h = img_shape
    draw = ImageDraw.Draw(pic)

    x1,y1,x2,y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    x1 = np.clip(x1, 0, img_w)
    x2 = np.clip(x2, 0, img_w)
    y1 = np.clip(y1, 0, img_h)
    y2 = np.clip(y2, 0, img_h)
    
    draw.rectangle(((x1, y1), (x2, y2)), outline=color)

    text_size = min(img_h, img_w)//50
    fnt = ImageFont.truetype('DejaVuSans-Bold.ttf', text_size)
    if draw_info:
        draw.rectangle(((x1, y1), (x2, y1+text_size+4)), fill=color)
        info = draw_info
        if fnt is not None:
            draw.text((x1+2,y1+2), info, font=fnt)
        else:
            draw.text((x1+2, y1+2), info)

def fix_height_draw_box(img_path, bboxes_dict, fixed_height=480):
    if isinstance(img_path, (np.ndarray, np.generic) ):
        # high possibility cv2 in bgr
        print(f"[WARNING] Please make sure the input ndarray image is a BGR image from opencv")
        img_opencv = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img_opencv)
    elif isinstance(img_path, str):
        img = Image.open(img_path)
    else:
        raise TypeError(f"Not support type {type(img_path)} for img_path")
        
    height_percent = (fixed_height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    img = img.resize((width_size, fixed_height), Image.BILINEAR)

    w,h = img.size
    
    for k,v in bboxes_dict.items():
        for box in v:
            # box in the fomat [x1, y1, x2, y2, score]
            box_coord = box[:4]
            score = box[-1]
            resized_box = resize_box(np.array(box_coord), float(height_percent))
            draw_single_box(
                img, resized_box, (w,h), 
                draw_info="{label:}: {score:.2f}".format(label=k, score=score), 
                color="#0dab62"
            )
    return img

def draw_sg(center_obj, relations, objid2info,  out_file=None):
    """
    Args:
        center_obj: obj_name
        relations: triples in the format [subject_id, object_id, relation_name]
        objid2info: object id to information
        out_file: output file info
    Return:
        dot object decribing the relational graph
    """
    dot = Digraph(comment='sg diagram', strict=True)
    for rel in relations:
        subj, obj, r = rel
        subj_name = objid2info[subj]['synsets']
        subj_attr = []
        if 'attributes' in objid2info[subj]:
            subj_attr = objid2info[subj]['attributes']
        
        obj_name = objid2info[obj]['synsets']
        obj_attr = []
        if 'attributes' in objid2info[obj]:
            obj_attr = objid2info[obj]['attributes']
        
        subj_c = 'black'; obj_c = 'black'
        if subj_name == center_obj: subj_c = 'red'
        if obj_name == center_obj: obj_c = 'red'
            
        dot.node(str(subj), subj_name, color=subj_c)
        dot.node(str(obj), obj_name, color=obj_c)
        dot.edge(str(subj), str(obj), r)
        
        # add attribute node to graph
        for sa in subj_attr:
            dot.node(str(subj)+sa, sa, color='lightblue', shape='box')
            dot.edge(str(subj), str(subj)+sa, dir='none', style='dashed')

        for sa in obj_attr:
            dot.node(str(obj)+sa, sa, color='lightblue', shape='box')
            dot.edge(str(obj), str(obj)+sa, dir='none', style='dashed')
        
    if out_file is not None:
        dot.render(out_file)
    return dot

if __name__ == "__main__":
    from PIL import Image
    img_path = ''
    img = Image.open(img_path)
    fixed_height = 720
    height_percent = (fixed_height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    img = img.resize((width_size, fixed_height), Image.BILINEAR)

    w,h = img.size
    box, score = [1, 10, 40, 50], 0.99 # [x1, y1, x2, y2]
    resized_box = resize_box(np.array(box), float(height_percent))
    draw_single_box(img, resized_box, (w,h), draw_info=f"Label information", color="#0dab62")