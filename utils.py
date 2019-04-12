import cv2, torch, random, time
import numpy as np
import torch.distributions.normal as N
from multiprocessing import Pool

device = torch.device('cuda')

def weight_init(m):
    classname = m.__class__.__name__
    if 'Conv' in classname:
        m.weight.data.normal_(0.0, 1)
    elif 'BatchNorm' in classname:
        m.weight.data.normal_(0.0, 1)
        m.bias.data.fill_(0)


def get_image(name, tensor):
    img = torch.squeeze(tensor.cpu().detach(),0).numpy()
    if len(img )==5:
        sketch = img[0][:,:,None].astype(np.uint8)
        cv2.imshow('sketch', cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR))
        img = img[2:]
    
    img = np.clip(img,0,255)
    # max_v, min_v = img.max(),img.min()
    # img = (img -min_v)/(max_v-min_v)*255
    img = np.transpose(img,(1,2,0)).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
    cv2.imshow(name,img)
    #cv2.waitKey(0)


def get_tensors(names, data_dir, label_dir, with_clue = False, data_augm = True):

    inputs_batch = [None]*len(names)
    label_batch = [None]*len(names)

    for idx in range(0,len(names)):
        f = names[idx]
               
        lineart = cv2.imread(data_dir+f+'.png', cv2.IMREAD_GRAYSCALE).astype(np.float32)
        #lineart = cv2.cvtColor(lineart, cv2.COLOR_BGR2YUV)
        color = cv2.imread(label_dir+f+'.png')
        color = cv2.cvtColor(color, cv2.COLOR_BGR2YUV).astype(np.float32)
        
        if data_augm:
            t = int(random.random()*4)
            p_noise = random.random()

            # Randimly flip the image
            if t==0:
                lineart = lineart[::-1,:]
                color = color[::-1,:]
            elif t == 1:
                lineart = lineart[:,::-1]
                color = color[:,::-1]
            elif t == 2:
                lineart = lineart[::-1,::-1]
                color = color[::-1,::-1]
            
            # Add noise
            if p_noise<0.15:             
                noise = np.random.normal(0, 3, lineart.shape).astype(lineart.dtype)
                lineart += noise
                noise = np.random.normal(0, 3, color.shape).astype(color.dtype)
                color += noise
       
        lineart = lineart[:,:,None]
        #lineart = np.transpose(lineart, (2,0,1)).astype(np.float32)
        
        if with_clue:
            width = random.randint(14,18) 
            amount = random.randint(25, 35)
            points = np.random.randint(width,len(lineart[0])-width,size=[amount,2])
            hint = np.zeros(color.shape).astype(np.float32)
            hint[:,:,0]=-512.0
            hint[:,:,1]=128.0
            hint[:,:,2]=128.0
             
            color_blur = cv2.GaussianBlur(color,(33,33),10)
            for p in points:
                hint[p[0]-width:p[0]+width,p[1]-width:p[1]+width] = color_blur[p[0]-width:p[0]+width,p[1]-width:p[1]+width]
            lineart = np.concatenate([lineart,lineart,hint ], axis =2)

        color = np.transpose(color, (2,0,1))
        lineart = np.transpose(lineart, (2,0,1))

        inputs_batch[idx] = torch.from_numpy(lineart.copy())
        label_batch[idx] = torch.from_numpy(color.copy())
        
   
    inputs_batch = torch.stack(inputs_batch).cuda()
    label_batch = torch.stack(label_batch).cuda()
    
    return inputs_batch, label_batch

