#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Develop by Bolin 
# Date: Aug 16, 2021


# In[56]:


import paddle
import paddleseg.transforms as T
from paddleseg.models import BiSeNetV2
from paddleseg.datasets import OpticDiscSeg
from paddleseg.models.losses import CrossEntropyLoss
from paddleseg.core import train
import os


# # 模型训练

# ## 1. 构建模型

# In[57]:


model = BiSeNetV2(num_classes=2,
                 lambd=0.25,
                 align_corners=False,
                 pretrained=None)


# ## 2. 构建训练集及数据预处理流程

# ### 数据准备

# In[58]:


# 构建训练用的数据增强和预处理
transforms = [
    T.Resize(target_size=(100, 100)),
    T.RandomHorizontalFlip(),
    T.Normalize()
]

# 构建训练集
train_dataset = OpticDiscSeg(
    dataset_root='data/outputs',
    transforms=transforms,
    mode='train'
)


# ### 数据增强

# In[ ]:





# ## 3. 构建验证集及数据预处理流程

# In[59]:


# 构建验证用的数据增强和预处理
transforms = [
    T.Resize(target_size=(100, 100)),
    T.Normalize()
]

# 构建验证集
val_dataset = OpticDiscSeg(
    dataset_root='data/outputs',
    transforms=transforms,
    mode='val'
)


# ## 4. 构建优化器

# In[60]:


# 设置学习率
base_lr = 0.01
lr = paddle.optimizer.lr.PolynomialDecay(base_lr, power=0.9, decay_steps=1000, end_lr=0)

optimizer = paddle.optimizer.Momentum(lr, parameters=model.parameters(), momentum=0.9, weight_decay=4.0e-5)


# ## 5. 构建损失函数

# In[61]:


losses = {}
losses['types'] = [CrossEntropyLoss()] * 5
losses['coef'] = [1]* 5


# ## 6. 训练

# In[62]:


train(
    model=model,
    train_dataset=train_dataset,
    val_dataset=val_dataset,
    optimizer=optimizer,
    save_dir='output',
    iters=1000,
    batch_size=8,
    save_interval=100,
    log_iters=10,
    num_workers=0,
    losses=losses,
    use_vdl=True)


# # 模型评估

# ## 6. 构建模型

# In[63]:


from paddleseg.models import BiSeNetV2
model = BiSeNetV2(num_classes=2,
                 lambd=0.25,
                 align_corners=False,
                 pretrained=None)


# ## 7. 加载模型参数

# In[64]:


model_path = 'output/best_model/model.pdparams'
if model_path:
    para_state_dict = paddle.load(model_path)
    model.set_dict(para_state_dict)
    print('Loaded trained params of model successfully')
else: 
    raise ValueError('The model_path is wrong: {}'.format(model_path))


# ## 8. 构建验证集

# In[65]:


# 构建验证用的transforms
transforms = [
    T.Resize(target_size=(100, 100)),
    T.Normalize()
]

# 构建验证集
from paddleseg.datasets import OpticDiscSeg
val_dataset = OpticDiscSeg(
    dataset_root='data/outputs',
    transforms=transforms,
    mode='val'
)


# ## 9. 评估

# In[66]:


from paddleseg.core import evaluate
evaluate(
        model,
        val_dataset)


# ## 10. 多尺度+翻转评估

# In[67]:


evaluate(
        model,
        val_dataset,
        aug_eval=True,
        scales=[0.75, 1.0, 1.25],
        flip_horizontal=True)


# # 效果可视化

# ## 11. 构建模型

# In[68]:


model = BiSeNetV2(num_classes=2,
                 lambd=0.25,
                 align_corners=False,
                 pretrained=None)


# ## 12. 创建transform

# In[69]:


transforms = T.Compose([
    T.Resize(target_size=(512, 512)),
    T.RandomHorizontalFlip(),
    T.Normalize()
])


# ## 13. 构建待预测的图像列表

# In[70]:


def get_image_list(image_path):
    """Get image list"""
    valid_suffix = [
        '.JPEG', '.jpeg', '.JPG', '.jpg', '.BMP', '.bmp', '.PNG', '.png'
    ]
    image_list = []
    image_dir = None
    if os.path.isfile(image_path):
        if os.path.splitext(image_path)[-1] in valid_suffix:
            image_list.append(image_path)
    elif os.path.isdir(image_path):
        image_dir = image_path
        for root, dirs, files in os.walk(image_path):
            for f in files:
                if os.path.splitext(f)[-1] in valid_suffix:
                    image_list.append(os.path.join(root, f))
    else:
        raise FileNotFoundError(
            '`--image_path` is not found. it should be an image file or a directory including images'
        )

    if len(image_list) == 0:
        raise RuntimeError('There are not image file in `--image_path`')

    return image_list, image_dir
image_path = 'data/outputs/JPEGImages/nail501.png' # 也可以输入一个包含图像的目录
image_list, image_dir = get_image_list(image_path)


# ## 14. 预测

# In[71]:


from paddleseg.core import predict
predict(
        model,
        model_path='output/best_model/model.pdparams',
        transforms=transforms,
        image_list=image_list,
        image_dir=image_dir,
        save_dir='output/results'
    )


# In[ ]:





# In[ ]:




