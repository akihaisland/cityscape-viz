import os
import pandas as pd
import numpy as np
import torch
from sklearn.metrics import precision_recall_fscore_support



def calculate_accuracy(model, data_loader):
    model.eval()  # 设置模型为评估模式
    total_correct = 0
    total_samples = 0
    
    with torch.no_grad():  # 在评估阶段不计算梯度
        for *groups, labels in data_loader:
            outputs = model(*groups)
            _, predicted = torch.max(outputs.data, 1)
            total_samples += labels.size(0)
            total_correct += (predicted == labels).sum().item()
    
    model.train()  # 将模型设置回训练模式
    return total_correct / total_samples

def calculate_metrics(model, data_loader, num_classes):
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for *groups, labels in data_loader:
            outputs = model(*groups)
            _, predicted = torch.max(outputs, 1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # 计算每个类别的准确率和召回率
    precision, recall, _, _ = precision_recall_fscore_support(all_labels, all_preds, labels=range(num_classes), zero_division=0)
    
    return precision, recall