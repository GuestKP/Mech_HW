import lxml
from lxml import etree
import numpy as np

file_path = "ur_description/UR3.xml"
file_path_2 = file_path[:-4] + "_inertia.xml"
file_path_3 = file_path[:-4] + "_armature.xml"
reflected_inertia = 382e-7


def str_to_arr(s):
    if s is not None:
        return np.array(s.split(' '), dtype='float64')
    else:
        return np.array([])


def arr_to_str(arr):
    return ' '.join([f'{i:.9f}' for i in arr])


def read_file(path):
    with open(file_path, 'r') as f:
        return etree.fromstringlist(f.readlines())

tree_inertia = read_file(file_path)

for body in tree_inertia.findall('.//body'):
    joints = body.findall('joint')
    inertials = body.findall('inertial')
    if joints and inertials:
        joint, inertial = joints[0], inertials[0]
        joint_axis = str_to_arr(joint.get('axis'))
        inertial_inertia = str_to_arr(inertial.get('diaginertia'))
        print(body.get('name'), joint_axis, inertial_inertia)
        inertial_inertia = inertial_inertia + joint_axis * reflected_inertia
        inertial.set('diaginertia', arr_to_str(inertial_inertia))
        #print(body.get('name'), joint_axis, inertial_inertia)

with open(file_path_2, 'w') as f:
    f.write(etree.tostring(tree_inertia, pretty_print=True).decode())
        
tree_armature = read_file(file_path)

for body in tree_armature.findall('.//body'):
    joints = body.findall('joint')
    if joints:
        joint = joints[0]
        joint.set('armature', f'{reflected_inertia:.9f}')

with open(file_path_3, 'w') as f:
    f.write(etree.tostring(tree_armature, pretty_print=True).decode())