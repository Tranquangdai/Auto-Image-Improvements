import os

from detectron2.data import build_detection_test_loader
from detectron2.engine import DefaultTrainer
from detectron2.evaluation import COCOEvaluator, inference_on_dataset


def get_pretrained_config():
    from detectron2 import model_zoo
    from detectron2.config import get_cfg

    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = ("train",)
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 14
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = 14
    cfg.SOLVER.BASE_LR = 0.001
    cfg.SOLVER.WARMUP_ITERS = 800
    cfg.SOLVER.GAMMA = 0.9
    cfg.SOLVER.STEPS = (1000, 1500, 2000, 2500)
    cfg.SOLVER.MAX_ITER = 2500
    cfg.SOLVER.NESTEROV = True
    cfg.SOLVER.LR_SCHEDULER_NAME = "WarmupCosineLR"
    cfg.SOLVER.WARMUP_FACTOR = 1.0 / 5
    cfg.SOLVER.CHECKPOINT_PERIOD = 800
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    return cfg


class Trainer:

    def __init__(self, cfg):
        self.cfg = cfg

    def train(self):
        os.makedirs(self.cfg.OUTPUT_DIR, exist_ok=True)
        self.trainer = DefaultTrainer(self.cfg)
        self.trainer.resume_or_load(resume=False)
        self.trainer.train()

    def evaluate(self, model_name='model_final.pth', data_name='val'):
        self.cfg.MODEL.WEIGHTS = os.path.join(self.cfg.OUTPUT_DIR, model_name)
        evaluator = COCOEvaluator(data_name,
                                  self.cfg, False,
                                  output_dir="./output/")
        val_loader = build_detection_test_loader(self.cfg, data_name)
        print(inference_on_dataset(self.trainer.model,
                                   val_loader,
                                   evaluator))
