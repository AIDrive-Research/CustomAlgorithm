# model

The `model` directory stores the RKNN model file, inference code, and model configuration file required for running the hearing algorithm. For model training, evaluation and inference, ONNX/RKNN conversion, and model file replacement, see `model_training_conversion.md`.

Current example path:

```text
AED/hazardous_sound_detection/model
```

This module contains 3 parts:

- Model folder: `model/hazardous_sound_detection`
- Inference code: `model/zql_aed.py`
- Model configuration file: `model/model.yaml`

## 1. Model Folder: `hazardous_sound_detection`

Current content:

```text
model/hazardous_sound_detection/model
```

Description:

- `model`: RKNN model file. The file name must be fixed as `model`; do not add the `.rknn` suffix.
- The current model folder name `hazardous_sound_detection` is the model instance name. It must be consistent with the model instance name in `model.yaml`, the Chinese and English `postprocessor.yaml` files, and the Chinese and English front-end JSON files.

The current example model output categories are configured in the Chinese and English post-processing configurations:

```text
0: Blast
1: Alarm
2: Crash
3: Distress
4: Skid
```

The current Chinese display names are:

```text
Blast -> 拍手声
Alarm -> 警报声
Crash -> 撞击声
Distress -> 异常人声
Skid -> 交通危险音
```

**Custom Algorithm Requirements:**

- If the number of categories, category order, or category meanings are changed, the Chinese and English post-processing configurations must be updated together.
- This algorithm package is an example package. When creating a custom algorithm package based on it, rename the package as required to avoid conflicts with built-in or existing algorithm packages.
- If the model folder is renamed, update the model instance name in `model.yaml`, `postprocessor_zh/hazardous_sound_detection.json`, `postprocessor_en/hazardous_sound_detection.json`, and the Chinese and English `postprocessor.yaml` files together.

Model training, evaluation and inference, ONNX/RKNN conversion, and model file replacement are not expanded in this document. For detailed steps, see:

[model_training_conversion.md](./model_training_conversion.md)

## 2. Inference Code: `zql_aed.py`

`zql_aed.py` is responsible for the following work:

1. Load the RKNN model file.
2. Receive audio stream data.
3. Convert audio into Fbank features.
4. Crop or zero-pad the features to a fixed number of frames.
5. Run RKNN inference.
6. Output the classification label and confidence score.

Default parameters:

```python
{
    'num_frames': 300,
    'model_sample_rate': 16000,
    'min_duration': 0.4,
    'use_dB_normalization': True,
    'target_dB': -20,
    'feature_method': 'Fbank',
    'use_hf_model': False,
    'num_mel_bins': 80,
}
```

These parameters must stay consistent with the training configuration:

| Parameter | Training Configuration Location | Deployment Meaning |
| --- | --- | --- |
| `model_sample_rate=16000` | `dataset_conf.dataset.sample_rate` | Input audio sample rate |
| `num_mel_bins=80` | `preprocess_conf.method_args.num_mel_bins` | Fbank dimension |
| `num_frames=300` | ONNX/RKNN export parameter | Fixed number of input frames |
| `target_dB=-20` | `dataset_conf.dataset.target_dB` | Target value for volume normalization |
| `min_duration=0.4` | `dataset_conf.dataset.min_duration` | Filtering threshold for overly short audio |

Inference input supports two forms:

- `bytes` / `bytearray`: Parsed as `int16 PCM` and normalized to `[-1, 1]`.
- `numpy.ndarray`: Processed as a `float32` audio sample array.

Inference output example:

```json
{
  "label": "Alarm",
  "conf": 0.87
}
```

If the model architecture is replaced but the input remains Fbank features in the shape `[1, 300, 80]`, usually only the RKNN model file needs to be replaced. If the feature method, sample rate, or input shape changes, `zql_aed.py` must be updated accordingly.

## 3. Model Configuration File: `model.yaml`

Current configuration:

```yaml
hazardous_sound_detection:
  type: zql_aed
  args:
    conf_thres: 0.3
  infer_time: null
```

Field description:

- `hazardous_sound_detection`: Model instance name. It must be consistent with the model folder name under `model`.
- `type`: Inference code file name without the `.py` suffix. The current value means `zql_aed.py` is used.
- `args.conf_thres`: Default confidence threshold. It will be overridden by the parameter with the same name in the front-end configuration.
- `infer_time`: Model inference time field. The current configuration uses `null`.

**Custom Algorithm Requirements:**

- If the model folder is renamed, the top-level key in `model.yaml` must be updated together.
- If the inference code is renamed, `type` must be updated together.
- It is recommended to set `conf_thres` first to a threshold that balances false alarms and missed detections on the validation set. Users can adjust it later on the interface.
