from importlib.resources import path
import xml.etree.ElementTree as ET
import os
from os import getcwd
from os.path import join
import glob

sets = ['train','test']#分别保存训练集和测试集的文件夹名称
classes = ['cube', 'ball', 'cylinder', 'human body', 'tyre', 'circle cage', 'square cage', 'metal bucket']#标注时的标签

'''
xml中框的左上角坐标和右下角坐标(x1,y1,x2,y2)
》》txt中的中心点坐标和宽和高(x,y,w,h)，并且归一化
'''
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
    
def convert_annotation(data_dir,imageset,image_id):#,npath):
    in_file = open(data_dir+'/%s_annotations/%s.xml' % (imageset,image_id), encoding='utf-8') #读取xml
    
#    oldname=npath+image_id+'.bmp'
    
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    filename = root.find('filename').text[:-4]
#    newname = npath + filename +'.bmp'
#    os.rename(oldname,newname)
    out_file = open(data_dir+'/%s_labels/%s.txt' % (imageset,filename), 'w') #保存txt
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)#获取类别索引
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str('%.6f'%a) for a in bb]) + '\n')

wd = getcwd()
print(wd)#当前路径

data_dir='D:/xml2yolo'
#npath='F:/2022URPC/dataset/val/image/'

for image_set in sets:
    image_ids=[]
    for x in glob.glob(data_dir+'/%s_annotations'%image_set+'/*.xml'):
        print(x)
        image_ids.append(os.path.basename(x)[:-4])        
    print('\n%s数量:'%image_set,len(image_ids))#确认数量
    i=0
    for image_id in image_ids:
        i=i+1
        convert_annotation(data_dir,image_set,image_id)#,npath)
        print("%s 数据:%s/%s文件完成！"% (image_set,i,len(image_ids)))
    
print("Done!!!")
