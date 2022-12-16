import os

# Check number of images
images_dir = './data/images/'

images_train_num = len(os.listdir(os.path.join(images_dir, 'train')))
images_val_num = len(os.listdir(os.path.join(images_dir, 'val')))
images_test_num = len(os.listdir(os.path.join(images_dir, 'test')))

# Check number of labels
labels_dir = './data/labels/'

labels_train_num = 0
labels_val_num   = 0
labels_test_num  = 0
for fn in os.listdir(os.path.join(labels_dir, 'train')):
    if fn == 'classes.txt':
        continue
    labels_train_num += 1
for fn in os.listdir(os.path.join(labels_dir, 'val')):
    if fn == 'classes.txt':
        continue
    labels_val_num += 1
for fn in os.listdir(os.path.join(labels_dir, 'test')):
    if fn == 'classes.txt':
        continue
    labels_test_num += 1

# Check number of classes
num_classes_dict = dict()
for fn in os.listdir(os.path.join(labels_dir, 'train')):
    if fn == 'classes.txt':
        continue
    with open(os.path.join(labels_dir, 'train', fn), 'r') as f:
        lines = f.readlines()
        for line in lines:
            c = line.split()[0]
            if c not in num_classes_dict.keys():
                num_classes_dict[c] = 0
            else:
                num_classes_dict[c] += 1

for fn in os.listdir(os.path.join(labels_dir, 'val')):
    if fn == 'classes.txt':
        continue
    with open(os.path.join(labels_dir, 'val', fn), 'r') as f:
        lines = f.readlines()
        for line in lines:
            c = line.split()[0]
            if c not in num_classes_dict.keys():
                num_classes_dict[c] = 1
            else:
                num_classes_dict[c] += 1

for fn in os.listdir(os.path.join(labels_dir, 'test')):
    if fn == 'classes.txt':
        continue
    with open(os.path.join(labels_dir, 'test', fn), 'r') as f:
        lines = f.readlines()
        for line in lines:
            c = line.split()[0]
            if c not in num_classes_dict.keys():
                num_classes_dict[c] = 1
            else:
                num_classes_dict[c] += 1

# Check redundant images, labels
redundant_images = []
redundant_labels = []
for fn in os.listdir(os.path.join(images_dir, 'train')):
    if not os.path.exists(
        os.path.join(labels_dir, 'train', fn[:-3] + 'txt')
    ):
        redundant_images.append(os.path.join(images_dir, 'train', fn))

for fn in os.listdir(os.path.join(images_dir, 'val')):
    if not os.path.exists(
        os.path.join(labels_dir, 'val', fn[:-3] + 'txt')
    ):
        redundant_images.append(os.path.join(images_dir, 'val', fn))

for fn in os.listdir(os.path.join(images_dir, 'test')):
    if not os.path.exists(
        os.path.join(labels_dir, 'test', fn[:-3] + 'txt')
    ):
        redundant_images.append(os.path.join(images_dir, 'test', fn))

# labels
for fn in os.listdir(os.path.join(labels_dir, 'train')):
    if fn == 'classes.txt':
        continue
    if not os.path.exists(
        os.path.join(images_dir, 'train', fn[:-3] + 'jpg')
    ):
        redundant_labels.append(os.path.join(labels_dir, 'train', fn))

for fn in os.listdir(os.path.join(labels_dir, 'val')):
    if fn == 'classes.txt':
        continue
    if not os.path.exists(
        os.path.join(images_dir, 'val', fn[:-3] + 'jpg')
    ):
        redundant_labels.append(os.path.join(labels_dir, 'val', fn))

for fn in os.listdir(os.path.join(labels_dir, 'test')):
    if fn == 'classes.txt':
        continue
    if not os.path.exists(
        os.path.join(images_dir, 'test', fn[:-3] + 'jpg')
    ):
        redundant_labels.append(os.path.join(labels_dir, 'test', fn))

# remove
# for fn in redundant_images:
#     os.remove(fn)
# for fn in redundant_labels:
#     os.remove(fn)

# Empty label file
empty_labels = []
for fn in os.listdir(os.path.join(labels_dir, 'train')):
    if os.stat(os.path.join(labels_dir, 'train', fn)).st_size == 0:
        empty_labels.append(fn)
for fn in os.listdir(os.path.join(labels_dir, 'val')):
    if os.stat(os.path.join(labels_dir, 'val', fn)).st_size == 0:
        empty_labels.append(fn)
for fn in os.listdir(os.path.join(labels_dir, 'test')):
    if os.stat(os.path.join(labels_dir, 'test', fn)).st_size == 0:
        empty_labels.append(fn)

# for fn in empty_labels:
#     os.remove(os.path.join(labels_dir, 'train', fn))

# print results
print(f'Images: train / val / test / total = {images_train_num} / {images_val_num} / {images_test_num} / {images_train_num + images_test_num + images_val_num}')
print(f'Labels: train / val / test / total = {labels_train_num} / {labels_val_num} / {labels_test_num} / {labels_train_num + labels_test_num + labels_val_num}')
print('Classes:', num_classes_dict)
print(f'Redundant images: {len(redundant_images)}')
print(f'Redundant labels: {len(redundant_labels)}')
print(f'Empty label files: {len(empty_labels)}')
