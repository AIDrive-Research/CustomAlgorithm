# Model Training and Conversion

This document describes the complete workflow for the `hazardous_sound_detection` hazardous sound detection model, including training data preparation, model training, evaluation and inference, ONNX export, ONNX simplification, RKNN conversion, and replacing the model file in the algorithm package.

## 1. Prepare the Training Project

Training project reference:

```text
https://github.com/yeyupiaoling/AudioClassification-Pytorch
```

It is recommended to create a dedicated training environment. The historical workflow used `py310-audio`, but the actual environment name can be customized.

```bash
conda create -n py310-audio python=3.10 -y
conda activate py310-audio

# Install PyTorch according to the CUDA version on the server. This is only an example.
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

git clone https://github.com/yeyupiaoling/AudioClassification-Pytorch.git
cd AudioClassification-Pytorch
pip install .
```

If you do not want to install from source, you can install the published package instead:

```bash
python -m pip install macls -U
```

For formal training, source installation is recommended because it makes it easier to modify configurations and export scripts.

## 2. Organize Data and Split the Training/Test Sets

The recommended directory structure is as follows:

```text
dataset/hazardous_sound_detection/audioset/
  0_Blast/
    xxx.wav
  1_Alarm/
    xxx.wav
  2_Crash/
    xxx.wav
  3_Distress/
    xxx.wav
  4_Skid/
    xxx.wav
  5_Normal/
    xxx.wav
```

It is recommended to add numeric prefixes to directory names to keep the category order stable. The script below sorts category directories, generates label IDs, and writes `label_list.txt`. If the directory name is `0_Blast`, it will automatically be written as `Blast`.

The data list generation script is provided in the `scripts` directory:

[generate_audio_dataset_lists.py](../docs/scripts/hearing/generate_audio_dataset_lists.py)

Copy `generate_audio_dataset_lists.py` to the root directory of the `AudioClassification-Pytorch` training project, or run it from the training project root directory with an absolute path.

Run the command:

```bash
python generate_audio_dataset_lists.py \
  --audio_path dataset/hazardous_sound_detection/audioset \
  --list_path dataset/hazardous_sound_detection
```

After execution, the following 3 files are generated:

```text
dataset/hazardous_sound_detection/train_list.txt
dataset/hazardous_sound_detection/test_list.txt
dataset/hazardous_sound_detection/label_list.txt
```

The generated data list format is fixed: the audio path comes first, followed by the label ID corresponding to the audio. Labels start from 0, and the path and label are separated by `\t`.

Example:

```shell
dataset/hazardous_sound_detection/audioset/0_Blast/class0_old1_YG9M3de5mISY.wav	0
dataset/hazardous_sound_detection/audioset/0_Blast/class0_old1_YHn7kIz6Z0ZI.wav	0
dataset/hazardous_sound_detection/audioset/2_Crash/class2_old5_YA8-9RIidXLo_aug101.wav	2
dataset/hazardous_sound_detection/audioset/2_Crash/class2_old5_YATAF6Wp31ZE_aug182.wav	2
```

Data requirements:

- Use a unified sample rate of `16000Hz` where possible.
- Use mono audio where possible.
- Training clips should cover the complete target sound event. The default maximum training duration is usually handled as `3s`.
- Keep the number of samples in each class as balanced as possible, and avoid having too few samples for any hazardous sound category.
- Category IDs must correspond one-to-one with the category order in the post-processing `class2label` configuration.

## 3. Modify the Training Configuration

Modify the configuration based on `configs/panns.yml`. The model save path corresponds to `models/PANNS_CNN10_Fbank`.

Key configuration:

```yaml
dataset_conf:
  dataset:
    min_duration: 0.4
    max_duration: 3
    sample_rate: 16000
    use_dB_normalization: True
    target_dB: -20
  train_list: 'dataset/hazardous_sound_detection/train_list.txt'
  test_list: 'dataset/hazardous_sound_detection/test_list.txt'
  label_list_path: 'dataset/hazardous_sound_detection/label_list.txt'

preprocess_conf:
  use_hf_model: False
  feature_method: 'Fbank'
  method_args:
    sample_frequency: 16000
    num_mel_bins: 80

model_conf:
  model: 'PANNS_CNN10'
  model_args:
    num_class: null
```

Notes:

- `num_class: null` means the number of classes is automatically inferred from `label_list.txt`.
- If GPU memory is insufficient, reduce `dataset_conf.dataLoader.batch_size` first.
- Training and deployment must keep `sample_rate=16000`, `feature_method=Fbank`, and `num_mel_bins=80` consistent.

## 4. Extract Features (Optional)

```bash
python extract_features.py --configs=configs/panns.yml --save_dir=dataset/hazardous_sound_detection/features
```

After feature extraction is complete, switch the data lists in the configuration to the feature lists:

```yaml
dataset_conf:
  train_list: 'dataset/hazardous_sound_detection/train_list_features.txt'
  test_list: 'dataset/hazardous_sound_detection/test_list_features.txt'
```

If the dataset is not large, you can also skip pre-extracting features and train directly with the raw audio lists.

## 5. Train the Model

Single-GPU training:

```bash
CUDA_VISIBLE_DEVICES=0 python train.py --configs=configs/panns.yml
```

After training is complete, focus on checking:

```text
models/PANNS_CNN10_Fbank/best_model/
```

This directory usually contains the best model weights and the training configuration.

## 6. Single-File Inference Verification

```bash
python infer.py \
  --configs=configs/panns.yml \
  --model_path models/PANNS_CNN10_Fbank/best_model \
  --audio_path dataset/hazardous_sound_detection/audioset/4_Skid/sample.wav
```

If the predicted labels do not match the post-processing categories, check the following issues first:

- Whether the category order used for training, evaluation, and export is consistent.
- Whether the category order generated by the data splitting script is stable.

## 7. Export ONNX

Use a fixed input length, consistent with the default inference parameters in the algorithm package `model/zql_aed.py`:

```text
num_frames=300
feature_dim=80
```

The ONNX export scripts are provided in the `scripts` directory:

- [export_onnx.py](../docs/scripts/hearing/export_onnx.py)

- [simplify_onnx.py](../docs/scripts/hearing/simplify_onnx.py)

Example commands:

```bash
python export_onnx.py \
  --configs configs/panns.yml \
  --model_path models/PANNS_CNN10_Fbank/best_model \
  --onnx_path models/PANNS_CNN10_Fbank/best_model/model_rknn.onnx \
  --num_frames 300 \
  --opset 11

python simplify_onnx.py \
  --onnx_in models/PANNS_CNN10_Fbank/best_model/model_rknn.onnx \
  --onnx_out models/PANNS_CNN10_Fbank/best_model/model_rknn_simplified.onnx \
  --num_frames 300 \
  --feature_dim 80
```

## 8. Convert RKNN

RKNN conversion usually requires switching to a dedicated RKNN environment.

```bash
conda activate py38-rk2.2.0
```

The RKNN conversion script is provided in the `scripts` directory:

- [export_rknn.py](../docs/scripts/hearing/export_rknn.py)

Conversion command:

```bash
python export_rknn.py \
  --onnx_path models/PANNS_CNN10_Fbank/best_model/model_rknn_simplified.onnx \
  --rknn_path models/PANNS_CNN10_Fbank/best_model/model_rknn.rknn \
  --target rk3588 \
  --num_frames 300 \
  --feature_dim 80
```

## 9. Replace the Model File in the Algorithm Package

Rename the generated RKNN file to:

```text
model
```

Replace it at:

```text
AED/hazardous_sound_detection/model/hazardous_sound_detection/model
```

If the model categories change, the following fields must be updated together:

- `postprocessor_zh/postprocessor.yaml -> model -> hazardous_sound_detection -> label -> class2label`
- `postprocessor_zh/postprocessor.yaml -> model -> hazardous_sound_detection -> label -> label_map`
- `postprocessor_zh/postprocessor.yaml -> alert_label`
- `postprocessor_en/postprocessor.yaml -> model -> hazardous_sound_detection -> label -> class2label`
- `postprocessor_en/postprocessor.yaml -> model -> hazardous_sound_detection -> label -> label_map`
- `postprocessor_en/postprocessor.yaml -> alert_label`
- `postprocessor_zh/hazardous_sound_detection.json -> basicParams/reserved_args/display_name`
- `postprocessor_en/hazardous_sound_detection.json -> basicParams/reserved_args/display_name`

