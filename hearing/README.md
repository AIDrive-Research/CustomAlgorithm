# Complete Workflow for Creating Hearing Recognition Algorithm Packages

This document uses the `hazardous_sound_detection` hazardous sound detection algorithm package as an example to describe the complete workflow for a custom hearing algorithm package, including model training, ONNX/RKNN conversion, algorithm package model replacement, post-processing configuration, encryption, and device import.

Current example algorithm package path:

```text
AED/hazardous_sound_detection
```

A complete hearing algorithm package usually contains three parts, or four parts when both Chinese and English UI configurations are required:

- `model`: model files, audio feature extraction, and RKNN inference code; also includes documentation for model training, inference validation, ONNX/RKNN conversion, and model replacement.
- `postprocessor_zh`: Chinese post-processing configuration and frontend parameter configuration.
- `postprocessor_en`: English post-processing configuration and frontend parameter configuration.
- `metadata.json`: algorithm package name, version, and algorithm category.

## QuickStart

If you only need to encrypt and import the current `hazardous_sound_detection` example algorithm package, start with QuickStart:

[QuickStart.md](./QuickStart.md)

QuickStart covers the following steps:

1. Check the algorithm package structure.
2. Obtain the encryption tool.
3. Encrypt the `hazardous_sound_detection` algorithm package.
4. Import the generated `.bin` file into the device algorithm repository.
5. Perform basic validation after import.

## Model Files and Inference Code

The `model` directory of a hearing algorithm package is responsible for loading the RKNN model, converting audio streams into Fbank features, and running inference.

For the model directory structure, inference code, and `model.yaml` configuration, see:

[model.md](./model.md)

For model training, dataset splitting, feature extraction, single-file inference, ONNX export, RKNN conversion, and model file replacement, see:

[model_training_conversion.md](./model_training_conversion.md)

## Chinese Post-Processing Configuration

`postprocessor_zh` defines the algorithm display name, algorithm description, alarm categories, confidence parameters, and voice broadcast content for the Chinese UI.

For details, see:

[postprocessor_zh.md](./postprocessor_zh.md)

## English Post-Processing Configuration

`postprocessor_en` defines the algorithm display name, algorithm description, alarm categories, confidence parameters, and voice broadcast content for the English UI.

For details, see:

[postprocessor_en.md](./postprocessor_en.md)

## Algorithm Name, Version, and Category Definition

`metadata.json` defines the English algorithm package name, version, and algorithm category. The algorithm package name should usually match the algorithm package folder name.

For details, see:

[metadata.md](./metadata.md)
