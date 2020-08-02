# Automatic Image Enhancement
-----------
### Description
For detailed information, see [this link](https://support.google.com/merchants/answer/9242973)
Basically, google shopping ads doesn't approve product image that contains call to actions text, promotional overlay and other distracting patches.
The goal of this project is to create a machine learning model that automatically crop out relevant part of the product region.

### Installation
```bash
    git clone https://github.com/Tranquangdai/Auto-Image-Improvements.git
    cd Auto-Image-Improvements/
    python setup.py install
```

### Usage
Please refer to this [Google Collab](https://colab.research.google.com/drive/1JG1zm7sIA-GhwWRiXjjmQbhBdi_A3y2D#scrollTo=I1AqCjYyf2wl) for a thorough guide on how to install, prepare data and train the model.
The notebook also provide way to load a pretrained model and use it for inference.

### Method:
- We make use of self-supervised learning to artificially generate bounding box and segmentations for product regions, and overlay that region to a designed background.
- Then we use [detectron2](https://github.com/facebookresearch/detectron2) to train a Masked-RCNN model for Object-Detection and Instance-Segmentation.
- For a more general approach, see [this_link](https://blog.picaas.io/2019/08/02/image-ai-leverage-image-insights-via-ml-picaas-for-google-shopping-ads/)

### Pretrained models
The pretrained model was trained on nearly 11500 data samples over various products and background for 2400 iterations. Visit [this_link](https://drive.google.com/file/d/1jylcsSSd1NVq5MaEFHQF4GAgAU-zSqBk/view?usp=sharing) to download the model.
