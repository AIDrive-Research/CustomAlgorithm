# model

`model`：Stores smell model files, inference code, and the model configuration file. Unlike visual object detection algorithms, smell algorithms do not require YOLO training, ONNX export, or RKNN quantization. The model is exported by the smell training function of `ks-tools.exe`.

This module contains 3 parts:
- Model folder: [zql_air_alcohol_coffee_recognition](./SmellRecognition/air_alcohol_coffee_recognition/model/zql_air_alcohol_coffee_recognition)
- Inference code: [zql_olfaction.py](./SmellRecognition/air_alcohol_coffee_recognition/model/zql_olfaction.py)
- Model configuration file: [model.yaml](./SmellRecognition/air_alcohol_coffee_recognition/model/model.yaml)

## 1. `zql_air_alcohol_coffee_recognition` Folder

**Custom Algorithm Requirements:**

- This algorithm package is a standard system-provided package of `Xiaozhi Jingling`. When creating a custom algorithm package by referring to this package, modify it as required to ensure that it does not conflict with the standard package.
- The folder name `zql_air_alcohol_coffee_recognition` here is the <span style="color:red;">model name</span> referenced below. For custom algorithm packages, rename the folder to a custom model instance name. For example, `zql_air_alcohol_coffee_recognition` can be changed to `custom_air_alcohol_coffee_recognition`, which is used as the example name below.
- Replace the default `model` file in the `custom_air_alcohol_coffee_recognition` folder with the model file exported by `ks-tools.exe` training. The model file must be named <span style="color:red;">model</span> and must not be changed.
- Complete model preparation, inference code modification, and model configuration file modification according to the following steps.s

### Preparing Model Files

Use `ks-tools.exe` to train the model. `ks-tools.exe` is responsible for connecting to the smell data collection device, collecting samples, training the classification model, and exporting the model file.

**Collecting Data**

1. Open `ks-tools.exe`.
2. Enter the smell device IP address and test the connection.
3. After the connection succeeds, the tool displays 10-dimensional sensor data from `s0` to `s9`.
4. Set the class ID for the current odor. For example, `0` means air, `1` means alcohol, and `2` means coffee.
5. Select the class and start collecting samples.

The sample header is fixed as:

```text
label,s0,s1,s2,s3,s4,s5,s6,s7,s8,s9
```

**Data Recommendations**

- Collect enough samples for each class to avoid one class having significantly fewer samples than the others.
- For the same odor, collect samples across different distances, concentrations, and environments.
- When switching odors, avoid using transition-stage data as stable samples.
- During collection, observe the sensor curves and confirm that odor changes produce distinguishable numeric changes.

**Training and Exporting**

After the sample count meets the requirement, select `kernel` on the model training page of `ks-tools.exe` and start training. For first-time use, keep the default `rbf` setting.

After training is complete, download the model, rename the exported model file to `model`, and replace the file at:

```text
SmellRecognition/air_alcohol_coffee_recognition/model/custom_air_alcohol_coffee_recognition/model
```

## 2. Inference Code [zql_olfaction.py](./SmellRecognition/air_alcohol_coffee_recognition/model/zql_olfaction.py)

`zql_olfaction.py` is responsible for loading the model file exported by `ks-tools.exe` and performing smell classification inference.

The default input is 10-dimensional smell sensor data:

```text
[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]
```

Inference output example:

```json
{
  "label": "1",
  "conf": 0.932,
  "result": {
    "0": 0.041,
    "1": 0.932,
    "2": 0.027
  }
}
```

**Custom Algorithm Requirements:**

- If you still use the smell classification model exported by `ks-tools.exe`, `zql_olfaction.py` usually does not need to be modified.
- If you switch to another model format or custom inference logic, replace the inference code and update `type` in `model.yaml` accordingly.

## 3. Model Configuration File: [model.yaml](./SmellRecognition/air_alcohol_coffee_recognition/model/model.yaml)

```yaml
zql_air_alcohol_coffee_recognition:
  type: zql_olfaction
  args:
    conf_thres: 0.50
  infer_time: null
```

**Custom Algorithm Requirements:**

- `air_alcohol_coffee_recognition`: the model instance name. It must be consistent with the model folder name under `model`.
- `type`: the inference entry file name without the `.py` suffix. The current value means that `zql_olfaction.py` is used.
- `conf_thres`: the default recognition confidence threshold. A larger value makes recognition stricter.
- `infer_time`: the inference time field. Smell algorithms can currently keep this value as `null`.
