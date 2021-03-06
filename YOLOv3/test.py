import torch
from torchsummary import summary
from nets.yolo3 import YoloBody
from utils.config import Config

if __name__ == "__main__":
    # Test the device to run on CPU or GPU 
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    config = {"model_params": {"backbone_name": "darknet_53"},"yolo": {"anchors": [[1,2,3],[2,3,4],[3,4,5]],"classes": 80}}
    m = YoloBody(config).to(device)
    summary(m, input_size=(3, 416, 416))
