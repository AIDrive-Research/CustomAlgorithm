# Resnet18

## Environment setup

   1. Clone repo and install [requirements.txt](./requirements.txt) in a python>=3.8.0 environment, including pytorch>=1.8

      ```bash
      git clone https://github.com/AIDrive-Research/CustomAlgorithm.git
      cd CustomAlgorithm/docs/ModelQuantization/Classification/Resnet18
      pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
      ```

## Model export

Modify `input_path` and `output_path` in `convert_onnx.py` to your own model weight path and `ONNX` file export path respectively. Execute the following code.

```bash
python convert_onnx.py
```
