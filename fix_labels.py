import os

labels_dir = 'labels'
old_labels_dir = 'old_labels'

for fn in os.listdir(os.path.join(old_labels_dir, 'test')):
    if fn == 'classes.txt':
        continue
    of = open(os.path.join(old_labels_dir, 'test', fn), 'r')
    f = open(os.path.join(labels_dir, 'test', fn), 'w')
    lines = of.readlines()
    for line in lines:
        _, x, y, z, t = line.split()
        f.write(f'0 {x} {y} {z} {t}\n')
    
    of.close()
    f.close()
    
