<div align="center">
  <p>
    <a align="center" href="https://github.com/AIDrive-Research/CustomAlgorithm" target="">
      <img
        width="100%"
        src="docs/assets/banner.png"
      >
    </a>
  </p>

  <a href="https://www.aidrive-tech.com/">
    <img alt="AIDrive-Tech" src="https://img.shields.io/badge/Official Website-AIDrive%20Tech-0088FF?style=flat&logo=car&logoSize=13&border=0" style="height: 20px; vertical-align: middle;">
  </a> 
  <a href="https://bbs.aidrive-tech.com/">
    <img alt="BBS" src="https://img.shields.io/badge/BBS-Forum-4299E1?style=flat&logo=discourse&logoSize=14&border=0" style="height: 20px; vertical-align: middle;">
  </a> 
  <a href="https://github.com/AIDrive-Research/CustomAlgorithm">
    <img alt="GitHub Stars" src="https://img.shields.io/github/stars/AIDrive-Research/CustomAlgorithm" style="height: 20px; vertical-align: middle;">
  </a>
  <a href="https://github.com/AIDrive-Research/CustomAlgorithm/blob/main/LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/License-Custom%20Proprietary-4299E1?style=flat&border=0" style="height: 20px; vertical-align: middle;">
  </a>
</div>

# 🔥 Custom Algorithm

## 📑 Project Introduction

This project provides multimodal algorithm training source code and an algorithm toolchain for edge AI devices. It covers three algorithm directions: **Vision**, **Hearing**, and **Smell**, helping developers quickly complete algorithm training, algorithm packaging, and model deployment on cost-effective edge devices for real-world use.

It should be noted that “running” here does not simply mean making an algorithm run on a certain operating system or chip. That is only a laboratory validation stage.

This project focuses more on the complete workflow from algorithm training to engineering deployment:  
**from data preparation, model training, model conversion, and algorithm packaging, to edge device import, inference scheduling, alarm linkage, and on-site application.**

Through this project, you can combine your self-trained algorithm models with a complete software and hardware system, and quickly deploy them in real commercial scenarios.

## 🚀 Project Goal

This open-source project has only one goal:

> **To help you directly commercialize the algorithm models you have trained.**

We hope developers can not only complete model training, but also understand how algorithms are deployed on real edge devices, including:

- How to organize the algorithm package structure;
- How to configure algorithm parameters;
- How to adapt the model format;
- How to import algorithms into edge devices;
- How to keep algorithms running continuously in real business scenarios.

## 🧩 Three Modal Algorithm Directions

This project is divided into three core modules according to algorithm perception modalities:

### 👁️ Vision: Visual Intelligent Analysis

The Vision module mainly focuses on image and video analysis scenarios, including but not limited to:

- Object detection
- Image classification
- Instance segmentation
- Object Tracking

It is suitable for visual intelligent applications such as camera video stream analysis, industrial site supervision, park security, fire safety, traffic scenarios, and personnel behavior analysis.

### 👂 Hearing: Audio Intelligent Analysis

The Hearing module mainly focuses on audio signal analysis scenarios, including but not limited to:

- Sound event recognition

It is suitable for abnormal sound recognition in on-site scenarios.

### 👃 Smell: Olfactory Intelligent Analysis

The Smell module mainly focuses on sensor data analysis scenarios, including but not limited to:

- Gas sensor data access
- Abnormal odor recognition

It is suitable for scenarios such as gas leakage detection and abnormal odor monitoring.

## 🖥️ Edge Devices and Commercial Deployment

We provide a complete software and hardware system based on the RK3588 chip, supporting direct deployment and operation of algorithms on edge devices.

Device-side capabilities include:

- Camera video stream decoding and analysis;
- Audio signal sampling and access;
- Olfactory sensor data access;
- NPU inference computing power scheduling;
- Multi-algorithm load balancing;
- Multi-model collaborative inference;
- Visual configuration of algorithm confidence thresholds;
- Algorithm package import and management;
- Network configuration and device operation and maintenance;
- Alarm records, alarm push, and business linkage.

Therefore, this project is not just a simple model training example repository, but an engineering reference for real project delivery.

## 📦 Quick Start

The overall usage process is as follows:

1. Select the corresponding modality module according to the business scenario:
   - `vision`
   - `hearing`
   - `smell`

2. Enter the corresponding module directory and select the appropriate algorithm type or sample project.

3. Follow the documentation in the module to complete:
   - Data preparation;
   - Model training;
   - Model conversion;
   - Algorithm package structure organization;
   - Algorithm package compression and packaging.

4. Import the generated algorithm package into the edge device backend.

5. Complete algorithm configuration, channel binding, confidence threshold setting, and alarm linkage in the device backend.

6. The algorithm takes effect on the edge device and enters the actual business operation stage.

## 📂 Directory Structure

```text
CustomAlgorithm/
├── vision/              # Vision algorithm module
├── hearing/             # Hearing algorithm module
├── smell/               # Smell algorithm module
├── docs/                # General documentation, FAQ, and deployment instructions
├── tools/               # General tools, dependency files, and auxiliary scripts
├── LICENSE
└── README.md
```

### [Tools](./Tools)
This directory provides tools and some dependency files used in the process of customizing algorithms.

# 💜 [FAQ](./docs/FAQ.md)
Common issues encountered during the development and debugging of custom algorithm packages are provided here. If you have any doubts during development, you can find answers in the FAQ document.

# 📬 Contact Information
- 🌐 Official Website: https://www.aidrive-tech.com
- 💭 BBS: https://bbs.aidrive-tech.com/  
- 📧 Email: support@aidrive-tech.com

# License

This repository is licensed under a custom proprietary license by Shandong Zhiquli Artificial Intelligence Technology Co., Ltd.

It is not open source and is intended only for authorized customers to develop and deploy custom algorithms on Zhiquli devices.

See [LICENSE](LICENSE) for details.