import cv2

class basic_operation(object):
    def __init__(self,dict):
        self.__dict__=dict
    def __str__(self):
        s=''
        for k in self.__dict__:
            s+='{key}::{value}\n'.format(key=k,value=self.__dict__[k])
        return s
    
    def forward(self,im):
        raise NotImplementedError

    def backword(self,im):
        raise NotImplementedError

class imresize(basic_operation):
    def __init__(self,tar_size=None,src_size=None):
        super().__init__({"tar_size":tar_size,'src_size':src_size})
    
    def forward(self, im):
        if self.src_size is None:
            self.src_size=(im.shape[1],im.shape[0])
        print(self.tar_size)
        return cv2.resize(im,self.tar_size)

    def backward(self, im):
        if self.tar_size is None:
            self.tar_size=(im.shape[1],im.shape[0])
        print(self.src_size)
        return cv2.resize(im,self.src_size)
    
class imrotate(basic_operation):
    def __init__(self,angle=0):
        super().__init__({'angle':angle})
    
    def forward(self,im):
        if self.angle==0:
            return im
        else:
            (h, w) = im.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, self.angle, 1.0)
            rotated = cv2.warpAffine(im, M, (w, h))
            return rotated
    def backward(self,im):
        if self.angle==0:
            return im
        else:
            (h, w) = im.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, 360-self.angle, 1.0)
            rotated = cv2.warpAffine(im, M, (w, h))
            return rotated


class imflip(basic_operation):
    '''
    flipcode:
        Flipped Horizontally              : 0
        Flipped Vertically                : 1
        Flipped Horizontally & Vertically :-1
    '''
    def __init__(self,flipcode=0):
        super().__init__({'flipcode':flipcode})

    def forward(self,im):
        return cv2.flip(im,self.flipcode)

    def backward(self,im):
        return cv2.flip(im,self.flipcode)





import matplotlib.pyplot as plt
if __name__=='__main__':
    im_path='C:/Users/SeldomRiver/Pictures/2018081810163.jpg'
    im=cv2.imread(im_path)
    plt.imshow(im)
    plt.show()
    op_flip=imflip(0)
    im=op_flip.forward(im)
    plt.imshow(im)
    plt.show()
    op_resize=imresize(tar_size=(300,300))
    im=op_resize.forward(im)
    plt.imshow(im)
    plt.show()
    op_rotate=imrotate(angle=25)
    im=op_rotate.forward(im)
    plt.imshow(im)
    plt.show()
    im=op_rotate.backward(im)
    plt.imshow(im)
    plt.show()
    im=op_resize.backward(im)
    plt.imshow(im)
    plt.show()
    im=op_flip.backward(im)
    plt.imshow(im)
    plt.show()