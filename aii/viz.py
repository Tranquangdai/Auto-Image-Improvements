import cv2
import matplotlib.pyplot as plt

from aii.components.design import Designer
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances
from detectron2.utils.visualizer import Visualizer

if __name__ == '__main__':
    cfg = {
        'patch': 'images/distractor/patch/',
        'sign': 'images/distractor/sign/',
        'logo': 'images/distractor/logo/',
        'product': 'images/product',
        'background': 'images/background/',
    }

    ds = Designer(cfg)
    ds.generate('_data/small', 3)
    ds.dump_annotations('_data/small.json')

    register_coco_instances("test", {},
                            "_data/test.json",
                            "_data/test")
    metadata = MetadataCatalog.get("test")
    dataset_dicts = DatasetCatalog.get("test")

    d = dataset_dicts[0]
    img = cv2.imread(d["file_name"])
    visualizer = Visualizer(img[:, :, ::-1], metadata=metadata, scale=0.5)
    vis = visualizer.draw_dataset_dict(d)
    plt.figure(figsize=[7, 7])
    plt.imshow(vis.get_image()[:, :, ::-1])
    plt.show()
