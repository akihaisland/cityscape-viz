import torch.nn as nn
import torch
import torch.nn.functional as F

class MLPEmbedding(nn.Module):
    def __init__(self, input_sizes, embedding_sizes, hidden_size, num_classes):
        super(MLPEmbedding, self).__init__()
        # 确保输入的尺寸列表和嵌入尺寸列表长度为5
        assert len(input_sizes) == 5 and len(embedding_sizes) == 5, "Input sizes and embedding sizes must be lists of length 5."
        
        # 动态创建5个嵌入层
        self.embeddings = nn.ModuleList([nn.Linear(in_size, out_size) for in_size, out_size in zip(input_sizes, embedding_sizes)])
        
        # 首个全连接层的输入尺寸是所有嵌入尺寸之和
        self.fc1 = nn.Linear(sum(embedding_sizes), hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)


    def forward(self, x1, x2, x3, x4, x5, return_embedding=False):
        # x应为一个包含5个tensor的列表，每个tensor对应一个输入
        x = [x1, x2, x3, x4, x5]
        out_embeddings = []
        for i, embedding in enumerate(self.embeddings):
            out = F.relu(embedding(x[i]))
            out_embeddings.append(out)
        
        # 沿着特征维度(concatenate)拼接所有嵌入输出
        out = torch.cat(out_embeddings, dim=1)
        
        # 继续通过网络的剩余部分
        out = self.fc1(out)
        if return_embedding:
            return out
        out = self.relu(out)
        out = self.fc2(out)
        return out