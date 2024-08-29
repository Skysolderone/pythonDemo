import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader,TensorDataset
# 示例数据
X = torch.tensor([[1.0], [2.0], [3.0], [4.0]], dtype=torch.float32)
y = torch.tensor([[2.0], [4.0], [6.0], [8.0]], dtype=torch.float32)

# 创建数据集和数据加载器
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

class SimpleLinearModel(nn.Module):
    def __init__(self):
        super(SimpleLinearModel,self).__init__()
        self.linear = nn.Linear(1, 1)
    def forward(self,x):
        return self.linear(x)
    
model=SimpleLinearModel()

criterion=nn.MSELoss()
optimizer=optim.SGD(model.parameters(),lr=0.01)
num_epochs=100
for epoch in range(num_epochs):
    for inputs,targets in dataloader:
        outputs=model(inputs)
        loss=criterion(outputs,targets)
        #反向传播
        optimizer.zero_grad()#梯度归零
        loss.backward()
        optimizer.step()
    if (epoch+1)%10==0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


with torch.no_grad():
    preicted=model(X)
    print(f'Predicted values: {preicted.numpy()}')
#save model
torch.save(model.state_dict(),'model.pth')
#load model
model=SimpleLinearModel()
# model.load_state_dict(torch.load('model.pth'))
model.load_state_dict(torch.load('model.pth', weights_only=True))
model.eval()