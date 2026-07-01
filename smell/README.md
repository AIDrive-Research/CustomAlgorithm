# Complete Production Process for Smell Recognition Algorithm Packages

To create a smell recognition algorithm package, you need to prepare model files, inference code, post-processing configuration, and algorithm metadata. This document uses the `Air Alcohol Coffee Recognition` algorithm as an example to describe the production, training, configuration, encryption, and import process for a smell algorithm package.

The biggest difference between smell algorithms and visual object detection algorithms is that model training does not depend on YOLO, ONNX, or RKNN conversion workflows. Instead, `ks-tools.exe` is used to connect to the smell data collection device, collect data, train the model, and export the model file.

In total, you need to prepare three parts of files, or four parts if both Chinese and English are required:
- Model file, inference code, and model configuration: `model`
- Chinese post-processing configuration: `postprocessor_zh`
- English post-processing configuration: `postprocessor_en`
- Algorithm name, version number, and category definition: `metadata.json`

## QuickStart

Before learning the detailed algorithm package production process, you can first use the existing `air_alcohol_coffee_recognition` sample algorithm package to complete one full workflow: training, model replacement, encryption, and import.

For details, see: [QuickStart.md](./QuickStart.md)

## Model Files and Inference Code

The `model` directory of a smell algorithm package contains the model file exported by `ks-tools.exe`, smell inference code, and model configuration file. The inference code receives sensor data and outputs the odor classification result.

For details, see: [model.md](./model.md)

## Chinese Post-Processing Configuration

This part mainly completes the following tasks:
- Define the algorithm display name, description, and group in the Chinese interface.
- Define the mapping from model output classes to Chinese display names.
- Define display colors and alert labels for different odor classes.
- Define configurable alert window, voice broadcast, and recognition confidence threshold parameters during algorithm binding.

For details, see: [postprocessor_zh.md](./postprocessor_zh.md)

## English Post-Processing Configuration

This part has the same meaning as the Chinese post-processing configuration and is used for display in the English interface. If the project only requires a Chinese interface, `postprocessor_en` can be removed.

For details, see: [postprocessor_en.md](./postprocessor_en.md)

## Algorithm Name, Version Number, and Category Definition

Only three fields in `metadata.json` need attention here: the English algorithm package name, version number, and algorithm category. The category of smell algorithms is fixed as `olfaction`.

For details, see: [metadata.md](./metadata.md)
