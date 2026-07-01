# model

`model`：Stores model files, inference code, and model configuration files. If you use the PyTorch framework, the model files here will be in the common `.pt` format.

This module includes 3 parts:
- Model folder: [custom_segment](./person_segmentation/model/custom_segment)
- Inference code: [custom_segment_yolov11.py](./person_segmentation/model/custom_segment_yolov11.py)
- Model configuration file: [model.yaml](./person_segmentation/model/model.yaml) 

## 1. custom_segment Folder

**Custom Algorithm Requirements:**

- This algorithm package is a standard system-provided package. When creating a custom algorithm package by referring to this one, modifications must be made as required to ensure no conflicts with the standard package.
- The folder name `custom_segment` here refers to the <span style="color:red;"> model name </span> mentioned below. For custom algorithm packages, the folder can be renamed to any other name. For example: `custom_segment` can be changed to `custom_segmentation`，and this name will be used as an example in the following content.
- Users need to replace the default "model" file in the `custom_segmentation` folder with their own model file. The model file must be uniformly named <span style="color:red;"> model </span> and cannot be modified。
- Complete model preparation, inference code modification, and model configuration file modification according to the following steps.

**Preparing Model Files**  
For instance segmentation tasks, we recommend YOLO series algorithms. Users can freely choose YOLOv8/11 to train their desired algorithm models. We recommend the official versions:
- YOLOv8 & YOLOv11：https://github.com/ultralytics/ultralytics 

After training your own `.pt` model file with PyTorch (it is recommended to test the model effect first), you need to convert it to `ONNX` format first, and then further convert it to `RKNN` format — the latter is the final form that can be used directly.

**Converting `pt` Model File to `onnx` Format**

To adapt to the subsequent conversion process, the trained PyTorch model (`.pt` format) needs to be converted to `ONNX` format. Please refer to the official Rockchip documentation:
- [YOLOv8-seg Model Export](https://github.com/airockchip/ultralytics_yolov8/blob/main/RKOPT_README.md)
- [YOLOv11-seg Model Export](https://github.com/airockchip/ultralytics_yolo11/blob/main/RKOPT_README.md)   

<span style="color:red;">Note: The conversion of `pt` model files to `onnx` must use the code from this repository, not the training repository code.</span>

**Converting `onnx` Model File to `rknn` Format**  

Finally, the `ONNX` model needs to be converted to the `RKNN` format compatible with the device. Please refer to the official Rockchip documentation:
- [YOLOv8-seg Model Quantization](https://github.com/airockchip/rknn_model_zoo/tree/v2.3.2/examples/yolov8_seg)
- [YOLOv11-seg Model Quantization](https://github.com/airockchip/rknn_model_zoo/tree/v2.3.2/examples/yolov8_seg) (Same as YOLOv8-seg)

<span style="color:red;">Note: Rename the generated RKNN file to "model" without any suffix,and replace the default file in the `custom_segmentation` model folder.</span>

## 2. Inference Code [custom_segment_yolov11.py](./person_segmentation/model/custom_segment_yolov11.py)  

The example `custom_segment_yolov11.py` is suitable for inference with the `YOLOv11-seg` model. If using `YOLOv8-seg` models, this file needs to be replaced.

- [YOLOv8-seg Inference Code](../../../docs/InferenceDemo/InstanceSegmentation/custom_segment_yolov8.py)
- [YOLOv11-seg Inference Code](../../../docs/InferenceDemo/InstanceSegmentation/custom_segment_yolov11.py)

**Custom Algorithm Requirements:**  

- If using the `YOLOv11-seg` model, the inference code `custom_segment_yolov11.py` can be used without modification.</span>

- <span style="color:red;">If using `YOLOv8` models, the inference code must be replaced with `custom_segment_yolov8.py`，and the original file `custom_segment_yolov11.py` is no longer needed and can be deleted.</span>

- If using other instance segmentation algorithms, you need to implement the inference logic yourself with reference to [custom_segment_yolov11.py](./person_segmentation/model/custom_segment_yolov11.py).

## 3. Model Configuration File: [model.yaml](./person_segmentation/model/model.yaml) 

```bash
custom_segment:                  # Model name: the name of the model folder in model, required
  type: custom_segment_yolov11   # Inference code corresponding to the model, required
  args:                       # Default parameters for model inference, required
    conf_thres: 0.1           # Model parameter, optional
    img_size: 640
    nms_thres: 0.45
  infer_time: 200             # Inference time, required
```
**Custom Algorithm Requirements:**

- If the inference code is replaced with `custom_segment_yolov8.py`，the `type` here should be `custom_segment_yolov8`(i.e., the file name of the inference code without the file type suffix);

- If the inference code is replaced with `custom_segment_yolov11.py`，the `type`here should be `custom_segment_yolov11`(i.e., the file name of the inference code without the file type suffix);

- `infer_time`: The time consumed for a single inference of the model, used to dynamically calculate the inference frame sampling interval. 