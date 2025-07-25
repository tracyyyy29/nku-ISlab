
import os
import torch
import torch.nn as nn
import time
from PIL import Image
from torchvision import transforms

os.putenv('MLU_VISIBLE_DEVICES','')
cfgs = [64,'R', 64,'R', 'M', 128,'R', 128,'R', 'M',
       256,'R', 256,'R', 256,'R', 256,'R', 'M',
       512,'R', 512,'R', 512,'R', 512,'R', 'M',
        512,'R', 512,'R', 512,'R', 512,'R', 'M']

IMAGE_PATH = 'data/strawberries.jpg'
VGG_PATH = 'models/vgg19.pth'

def vgg19():
    layers = [
        'conv1_1', 'relu1_1', 'conv1_2', 'relu1_2', 'pool1',
        'conv2_1', 'relu2_1', 'conv2_2', 'relu2_2', 'pool2',
        'conv3_1', 'relu3_1', 'conv3_2', 'relu3_2', 'conv3_3','relu3_3', 'conv3_4', 'relu3_4', 'pool3',
        'conv4_1', 'relu4_1', 'conv4_2', 'relu4_2', 'conv4_3','relu4_3', 'conv4_4', 'relu4_4', 'pool4',
        'conv5_1', 'relu5_1', 'conv5_2', 'relu5_2', 'conv5_3','relu5_3', 'conv5_4', 'relu5_4', 'pool5',
        'flatten', 'fc6', 'relu6','fc7', 'relu7', 'fc8', 'softmax'
    ]
    layer_container = nn.Sequential()
    in_channels = 3
    num_classes = 1000
    for i, layer_name in enumerate(layers):
        if layer_name.startswith('conv'):
            # TODO: 在时序容器中传入卷积运算
            while cfgs and isinstance(cfgs[0], str):
                cfgs.pop(0)
            out_channels = cfgs.pop(0) if cfgs else in_channels
            layer_container.add_module(layer_name, nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1))
            in_channels = out_channels
        elif layer_name.startswith('relu'):
            # TODO: 在时序容器中执行ReLU计算
            layer_container.add_module(layer_name, nn.ReLU(inplace=True))
        elif layer_name.startswith('pool'):
            # TODO: 在时序容器中执行maxpool计算
            layer_container.add_module(layer_name, nn.MaxPool2d(kernel_size=2, stride=2))
        elif layer_name == 'flatten':
            # TODO: 在时序容器中执行flatten计算
            layer_container.add_module(layer_name, nn.Flatten())
        elif layer_name == 'fc6':
            # TODO: 在时序容器中执行全连接层计算
            out_features = 4096
            layer_container.add_module(layer_name, nn.Linear(512*7*7, out_features))
            in_channels = out_features
        elif layer_name == 'fc7':
            # TODO: 在时序容器中执行全连接层计算
            out_features = 4096
            layer_container.add_module(layer_name, nn.Linear(in_channels, out_features))
            in_channels = out_features
        elif layer_name == 'fc8':
            # TODO: 在时序容器中执行全连接层计算
            out_features = num_classes
            layer_container.add_module(layer_name, nn.Linear(in_channels, out_features))
            in_channels = out_features
        elif layer_name == 'softmax':
            # TODO: 在时序容器中执行Softmax计算
            layer_container.add_module(layer_name, nn.Softmax(dim=1))
    return layer_container


def load_image(path):
    #TODO: 使用 Image.open模块读入输入图像，并返回形状为（1,244,244,3）的数组 image
    image = Image.open(path)
    transform = transforms.Compose([transforms.Resize(256),
                                  transforms.CenterCrop(224),
                                  transforms.ToTensor(),
                                  transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                      std=[0.229, 0.224, 0.225])])
    #TODO: 对图像调用transform函数进行预处理
    image = transform(image)
    #TODO: 对tensor的第0维进行扩展
    image = image.unsqueeze(0)
    return image

if __name__ == '__main__':
    input_image = load_image(IMAGE_PATH)
    #TODO: 生成VGG19网络模型并保存在net中
    net = vgg19()
    #TODO: 加载网络参数到net中
    net.load_state_dict(torch.load(VGG_PATH))
    #TODO: 模型进入推理模式
    net.eval()
    st = time.time()
    # TODO: 计算 net,得到prob
    prob = net(input_image)
    print("cpu infer time:{:.3f} s".format(time.time()-st))
    with open('./labels/imagenet_classes.txt') as f:
        classes = [line.strip() for line in f.readlines()]
        _, indices = torch.sort(prob, descending=True)
    print("Classification result: id = %s, prob = %f " % (classes[indices[0][0]], prob[0][indices[0][0]].item()))
    if classes[indices[0][0]] == 'strawberry':
       print('TEST RESULT PASS.')
    else:
       print('TEST RESULT FAILED.')
       exit()
