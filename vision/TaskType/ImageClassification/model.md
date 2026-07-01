# model

`model`：Stores model files, inference code, and model configuration files. If you use the PyTorch framework, the model files here will be in the common `.pt` format.

This module includes 3 parts:
- Model folder: [custom_fog_classify](./fog/model/custom_fog_classify)
- Inference code: [custom_classify.py](./fog/model/custom_classify.py)
- Model configuration file: [model.yaml](./fog/model/model.yaml) 

## 1. custom_fog_classify Folder

**Custom Algorithm Requirements:**

- This algorithm package is a manufacturer-provided optional algorithm package. When creating a custom algorithm package by referring to this one, modifications must be made as required to ensure no conflicts with the system algorithm packages.
- The folder name `custom_fog_classify` here refers to the <span style="color:red;"> model name </span> mentioned below. 
- Users need to replace the default "model" file in the `custom_fog_classify` folder with their own model file. The model file must be uniformly named <span style="color:red;"> model </span> and cannot be modified。
- Complete model preparation, inference code modification, and model configuration file modification according to the following steps.

**Preparing Model Files**  
For image classification tasks, we recommend using the ResNet series algorithms. Users can also freely choose other model structures to train the required algorithms. We provide a Resnet18 training example:
- [Resnet18](../../../docs/ModelQuantization/Classification/Resnet18/README_TRAIN.md)

After training your own `.pt` model file with PyTorch (it is recommended to test the model effect first), you need to convert it to `ONNX` format first, and then further convert it to `RKNN` format — the latter is the final form that can be used directly.

**Converting `pt` Model File to `onnx` Format**

To adapt to the subsequent conversion process, the trained PyTorch model (`.pt` format) needs to be converted to `ONNX` format. Please refer to the documentation:
- [Resnet18 Model Export](../../../docs/ModelQuantization/Classification/Resnet18/README_EXPORT.md) 

<span style="color:red;">Note: The conversion of `pt` model files to `onnx` must use the code from this repository, not the training repository code.</span>

**Converting `onnx` Model File to `rknn` Format**  

Finally, the `ONNX` model needs to be converted to the `RKNN` format compatible with the device. Please refer to the documentation:
- [Resnet18 Model Quantization](../../../docs/ModelQuantization/Classification/Resnet18/README_QUANTIZATION.md)

<span style="color:red;">Note: Rename the generated RKNN file to "model" without any suffix,and replace the default file in the `custom_fog_classify` model folder.</span>

## 2. Inference Code [custom_classify.py](./fog/model/custom_classify.py)  

The example `custom_classify.py` is suitable for inference with the `Resnet` model. 

- [Resnet Inference Code](../../../docs/InferenceDemo/Classification/custom_classify_resnet.py)

**Custom Algorithm Requirements:**  

- If using the `Resnet` model, the inference code `custom_classify.py` can be used without modification.</span>

- <span style="color:red;">If using other models, the inference code must be replaced，and the original file `custom_classify.py` is no longer needed and can be deleted.</span>

- If using other classification algorithms, you need to implement the inference logic yourself with reference to [custom_classify.py](./fog/model/custom_classify.py). 

## 3. Model Configuration File: [model.yaml](./fog/model/model.yaml) 

```bash
custom_fog_classify:          # Model name: the name of the model folder in model, required
  type: custom_classify       # Inference code corresponding to the model, required
  args:                       # Default parameters for model inference, required
    img_size: 224
    conf_thres: 0.5
  infer_time: 15              # Inference time, required
```
**Custom Algorithm Requirements:**

- If the inference code is replaced with `custom_classify_resnet.py`，the `type` here should be `custom_classify_resnet`(i.e., the file name of the inference code without the file type suffix);

- `infer_time`: The time consumed for a single inference of the model, used to dynamically calculate the inference frame sampling interval. 