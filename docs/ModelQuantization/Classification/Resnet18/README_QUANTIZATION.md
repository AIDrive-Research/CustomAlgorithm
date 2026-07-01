# Resnet18

## Quantization Environment Setup
Note: This process applies to the Xiaozhi Genie `ks968` product. It is not required for `ks988`.

- System Requirements
    - Operating System: Ubuntu

- The `Tools/rknn-toolkit2` directory provides the quantization environment `.whl` file for `Python 3.8`:

  ```bash
    cd Tools/rknn-toolkit2
    conda create -n py38-rk2.2 python=3.8
    conda activate py38-rk2.2
    pip3 install rknn_toolkit2-2.2.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
  ```

## Model Quantization
**Note**: This operation applies to the ks968 product. It is not required for ks988.

1. [**Environment Setup**](../../README.md)

2. Randomly select images from the training set for model quantization and calibration.
The recommended number of images is 80–120.  
Directory structure:

   ```
    images:
    	xxx.jpg
   ```

3. Save the image paths to `xxx.txt`

   ```
    find ./images/ -name "*.jpg">custom.txt
   ```

4. Model Quantization

   Modify `convert.py`：

   - DATASET_PATH: path to the quantization images

   Run: 

   ```
    python convert.py onnx_model_path platform i8/fp output_rknn_path
   ```

   Where:

   - onnx_model_path：path to the exported `ONNX` model
   - platform：rk3588
   - i8/fp：
      - i8 = image-based INT8 quantization  
      - fp = no quantization
   - output_rknn_path：save path for the quantized `RKNN` model