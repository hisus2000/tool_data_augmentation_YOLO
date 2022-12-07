import albumentations as A
import cv2
import os

train_test=["train","val"]

# User can optimize in here
# Dir of data set
data_dir="data"

console_0={
"HorizontalFlip": 1,
"VerticalFlip": 1,
"Rotate_-90" : 1,
"Rotate_-180" : 1,
"Rotate_90" : 1,
"Rotate_180" : 1,
}

console_1={
"RandomBrightnessContrast_-02_00_": 1,
"RandomBrightnessContrast_00_02_": 1,
"MultiplicativeNoise_07_09_" : 1,
"MultiplicativeNoise_04_06_" : 1,
"MultiplicativeNoise_09_11_" : 1,
}

# Dash Board to do action
dashboard_0={
"HorizontalFlip": A.HorizontalFlip(always_apply=True),
"VerticalFlip": A.VerticalFlip(always_apply=True),
"Rotate_-90" : A.Rotate(limit=[-90,-90],always_apply=True),
"Rotate_-180" : A.Rotate(limit=[-180,-180],always_apply=True),
"Rotate_90" : A.Rotate(limit=[90,90],always_apply=True),
"Rotate_180" : A.Rotate(limit=[180,180],always_apply=True),
} 
dashboard_1={
"RandomBrightnessContrast_-02_00_": A.RandomBrightnessContrast(always_apply=True, brightness_limit=(-0.2, 0)),
"RandomBrightnessContrast_00_02_": A.RandomBrightnessContrast(always_apply=True, brightness_limit=(0, 0.2)),
"MultiplicativeNoise_07_09_" : A.MultiplicativeNoise (multiplier=(0.7, 0.9), per_channel=False, elementwise=False, always_apply=True, p=0.5),
"MultiplicativeNoise_04_06_" : A.MultiplicativeNoise (multiplier=(0.4, 0.6), per_channel=False, elementwise=False, always_apply=True, p=0.5),
"MultiplicativeNoise_09_11_" : A.MultiplicativeNoise (multiplier=(0.9, 1.1), per_channel=False, elementwise=False, always_apply=True, p=0.5),
}

# Transform_name is set name for each image affter transform
transform_names_0 =[]
transform_names_1 =[]

for i in console_0:
    if console_0[i]==1:
        transform_names_0.append(i)

for i in console_1:
    if console_1[i]==1:
        transform_names_1.append(i)

images_dir_path = "./"+data_dir+"/images/"
labels_dir_path = "./"+data_dir+"/labels/"

# STEP 1
for transform_name in transform_names_0:     
    for i in train_test:    
        images_dir = images_dir_path
        labels_dir = labels_dir_path
        images_dir = images_dir + str(i)
        labels_dir = labels_dir + str(i)
        # VerticalFlip, HorizontalFlip, RandomBrightnessContrast        
        transform = A.Compose([dashboard_0[transform_name]], bbox_params=A.BboxParams(format='yolo'))
        count = 0
        images_list = os.listdir(images_dir)
        for fn in images_list:
            if fn.startswith('aug_step1_'):
                continue
            image = cv2.imread(images_dir + '/' + fn)
            bboxes = []
            with open(labels_dir + '/' + fn.split(".jp")[0] + '.txt', 'r') as fl:
                anns = fl.readlines()
                for ann in anns:
                    ann = ann.strip('\n').split()  
                    cl = ann[0]
                    bbox = list(map(float, ann[1:])) + [cl]
                    bboxes.append(bbox)
            transformed = transform(image=image, bboxes=bboxes)
            transformed_image = transformed['image']
            transformed_bboxes = transformed['bboxes']        
            # save image 
            cv2.imwrite(filename=os.path.join(images_dir, f'aug_step1_{transform_name}_{fn}'), img=transformed_image)        
            # save labels
            with open(labels_dir + f'/aug_step1_{transform_name}_' + fn.split(".jp")[0] + '.txt', 'w') as fw:
                for transformed_bbox in transformed_bboxes:
                    transformed_ann = f'{int(transformed_bbox[4])} {transformed_bbox[0]} {transformed_bbox[1]} {transformed_bbox[2]} {transformed_bbox[3]}'
                    fw.write(transformed_ann)    
            count += 1
# STEP 2
for transform_name in transform_names_1:     
    for i in train_test:    
        images_dir = images_dir_path
        labels_dir = labels_dir_path
        images_dir = images_dir + str(i)
        labels_dir = labels_dir + str(i)
        # VerticalFlip, HorizontalFlip, RandomBrightnessContrast        
        transform = A.Compose([dashboard_1[transform_name]], bbox_params=A.BboxParams(format='yolo'))
        count = 0
        images_list = os.listdir(images_dir)
        for fn in images_list:
            if fn.startswith('aug_step2_'):
                continue
            image = cv2.imread(images_dir + '/' + fn)
            bboxes = []
            with open(labels_dir + '/' + fn.split(".jp")[0] + '.txt', 'r') as fl:
                anns = fl.readlines()
                for ann in anns:
                    ann = ann.strip('\n').split()  
                    cl = ann[0]
                    bbox = list(map(float, ann[1:])) + [cl]
                    bboxes.append(bbox)
            transformed = transform(image=image, bboxes=bboxes)
            transformed_image = transformed['image']
            transformed_bboxes = transformed['bboxes']        
            # save image 
            cv2.imwrite(filename=os.path.join(images_dir, f'aug_step2_{transform_name}_{fn}'), img=transformed_image)        
            # save labels
            with open(labels_dir + f'/aug_step2_{transform_name}_' + fn.split(".jp")[0] + '.txt', 'w') as fw:
                for transformed_bbox in transformed_bboxes:
                    transformed_ann = f'{int(transformed_bbox[4])} {transformed_bbox[0]} {transformed_bbox[1]} {transformed_bbox[2]} {transformed_bbox[3]}'
                    fw.write(transformed_ann)    
            count += 1

print(f'{count} images augmented by applying {transform_name}')