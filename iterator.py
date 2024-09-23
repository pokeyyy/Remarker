import numpy as np


def accept_new():
    pass

def accept_original():
    pass

def get_next_pcd():
    #return a numpy array with shape (n,9) 
    # [x,y,z,r,g,b,label_0,label_1,mask]

    # coordinates: n x 3
    # color: n x 3
    # label_0: n x 1
    # label_1: n x 1
    # mask: n x 1 , 1 for current part,0 for others
    pcd = np.random.random((1000,9))
    return pcd

def get_prev_pcd():
    return pcd
