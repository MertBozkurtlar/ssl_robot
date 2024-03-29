import torch
import torch.nn as nn

class DenseVMNet(nn.Module):
    def __init__(self, size_in=(201*20), size_hidden_a=256, size_hidden_b=512, size_out=72):
        super().__init__()
        self.vmLayer = VonMisesLayer(size_in, size_hidden_a)
        self.fc1 = nn.Linear(size_hidden_a * 8, size_hidden_b)
        self.fc2 = nn.Linear(size_hidden_b, size_out)
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()
        self.bn1 = nn.BatchNorm2d(8)
        self.bn2 = nn.BatchNorm1d(size_hidden_b)
        self.dropout = nn.Dropout(p=0.5)
        self.flatten = nn.Flatten(start_dim=2)
        self.flatten2 = nn.Flatten()

    def forward(self, x):
        x = self.flatten(x)
        x = self.vmLayer(x)
        x = self.bn1(x)
        x = self.sigmoid(x)
        x = self.flatten2(x)
        x = self.dropout(x)
        x = self.fc1(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
    
    
class VonMisesLayer(nn.Module):
    def __init__(self, size_in, size_out):
        super().__init__()
        self.size_in = size_in
        self.size_out = size_out
        # self.weightW = nn.Parameter(torch.Tensor(self.size_in, self.size_out))
        # self.weightZ = nn.Parameter(torch.Tensor(self.size_in, self.size_out))
        self.W = nn.Linear(size_in, size_out, bias = False)
        self.Z = nn.Linear(size_in, size_out, bias=False)
        # self.bias = nn.Parameter(torch.Tensor(1, self.size_out))
        # torch.nn.init.normal_(self.weightW)
        # torch.nn.init.normal_(self.weightZ)
        # torch.nn.init.normal_(self.bias)
        
    def forward(self, x):
        # sin_mul = torch.matmul(torch.sin(x), self.weightW)
        # cos_mul = torch.matmul(torch.cos(x), self.weightZ)
        # return sin_mul + cos_mul + self.bias
        sin_layer = self.W(torch.sin(x))
        cos_layer = self.Z(torch.cos(x))
        return sin_layer + cos_layer
