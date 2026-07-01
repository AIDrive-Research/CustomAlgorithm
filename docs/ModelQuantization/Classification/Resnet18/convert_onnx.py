import torch
import torchvision.models as models

input_path = 'best.pth'
output_path = 'best.onnx'
num_classes= 2


model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(in_features=512, out_features=num_classes)
model.load_state_dict(torch.load(input_path))
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(model, dummy_input, output_path, 
                  export_params=True,        
                  opset_version=12,         
                  do_constant_folding=True,  
                  input_names=['input'],    
                  output_names=['output'])

print(f"模型已成功转换为 ONNX 格式并保存到 {output_path}")


