import os

location = os.path.dirname(os.path.realpath(__file__))
data_object1 = os.path.join(location, 'data', 'dataset1.txt')
data_object2 = os.path.join(location, 'data', 'dataset2.txt')
data_object3 = os.path.join(location, 'data', 'dataset3.txt')
data_object4 = os.path.join(location, 'data', 'dataset4.txt')
data_object5 = os.path.join(location, 'data', 'dataset5.txt')

dataset1 = open(data_object1)
dataset2 = open(data_object2)
dataset3 = open(data_object3)
dataset4 = open(data_object4)
dataset5 = open(data_object5)