import numpy as np


def accept_new():
    pass

def accept_original():
    pass

def get_next_pcd(clusters,pointer):
    #return a numpy array with shape (n,9)
    # [x,y,z,r,g,b,label_0,label_1,mask]

    # coordinates: n x 3
    # color: n x 3
    # label_0: n x 1
    # label_1: n x 1 pre
    # mask: n x 1 , 1 for current part,0 for others
    #TODO
    print(pointer)
    pcd = clusters[pointer]
    return pcd

def get_prev_pcd():
    #TODO
    pcd = np.hstack((np.random.normal(0,1,(1000,3)),np.random.uniform(0,255,(1000,3)),np.random.randint(0,3,(1000,3))))
    return pcd
