# Paints
Auto paint sketch based on CNN(from lineart to anime illustration) 

This work utilizes about a million pairs of illustration and lineart, while the former is from [Danbooru dataset](https://www.gwern.net/Danbooru2018#download) and the latter is from [lllyasviel's work](https://github.com/lllyasviel/sketchKeras). For now, the result is not satisfying and more efforts are needed. If you look for a better auto-paint network please have a look at [this](https://github.com/pfnet/PaintsChainer) and [this](https://github.com/lllyasviel/style2paints).

## How to use:


Open your shell or terminal:

	git clone https://github.com/adamz799/Paints.git
    cd V1
	
Then you need to download [network](https://drive.google.com/file/d/1pNlnZnQQf-LxdmBZlwMVmzhAFxJFvbt-/view?usp=sharing) to V1/ and run:

    python app.py --lineart YOUR_LINEART_FILE_PATH --ref_img YOUR_REFERENCE_IMAGE_FILE_PATH 
    

<br>I work on this alone and have no time to implement a GUI, so all the interactive functions are achieved by OpenCV, which might be a little weird. In painting, you need to pick a color from a reference image and draw it to the lineart, then press 'r' in your keyboard to launch the network. It is fine to draw only a part of the lineart to see the result and then draw other parts to correct network's fault.




![logo](https://github.com/adamz799/Paints/blob/master/demo/splice_51419210.png)
<br>These pictures are from Danbooru dataset.
<br>
<br>![logo](https://github.com/adamz799/Paints/blob/master/demo/d2.PNG)
<br>![logo](https://github.com/adamz799/Paints/blob/master/demo/d3.PNG)
<br>![logo](https://github.com/adamz799/Paints/blob/master/demo/d4.PNG)
<br>![logo](https://github.com/adamz799/Paints/blob/master/demo/d5.PNG)
### This lineart is searched from the Internet by search engine, if this violate you right please contact me or report an issue. 


## Installation Dependencies:
* CUDA
* CuDNN
* Python 3.5
* Numpy
* [Pytorch 1.0.1](https://pytorch.org/)
* OpenCV-python

## Disclaimer
This work takes following repo(s) as reference(s):

[lllyasviel/style2paints](https://github.com/lllyasviel/style2paints)
<br>[pfnet/PaintsChainer](https://github.com/pfnet/PaintsChainer)
