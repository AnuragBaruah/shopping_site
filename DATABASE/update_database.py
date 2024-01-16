import csv, pickle
with open('products.csv', 'r') as f:
    data = list(csv.reader(f))
tags = []
for i in data:
    L = i[1].split('.')
    for p in L:
        if p not in tags:
            tags.append(p)
while 1:
    try:
        tags.remove('')
    except:
        break
while 1:
    try:
        tags.remove(' ')
    except:
        break
while 1:
    try:
        tags.remove('  ')
    except:
        break
with open('tagsused.dat', 'wb') as f:
    pickle.dump(tags, f)

with open('tagsused.dat', 'rb') as f:
    print(pickle.load(f))

"""
with open('products.csv', 'r') as f:
    data = list(csv.reader(f))
L = '../IMAGES/img'
K = '.jpg'
c = 1
for i in data:
    for j in [3,4,5,6,7]:
        i[j] = L + str(c) + K
        c += 1

with open('products.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(data)
"""        
