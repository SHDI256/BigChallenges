import torch


xn = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0], requires_grad=True)
m = 1
y = torch.pow((torch.sum(torch.pow(xn, m)) / xn.size(0)), 1 / m)
print(y)
y.backward()
print(xn.grad)