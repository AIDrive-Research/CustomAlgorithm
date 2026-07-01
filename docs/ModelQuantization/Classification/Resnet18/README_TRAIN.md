# Resnet18

## Environment setup

   1. Clone repo and install [requirements.txt](./requirements.txt) in a python>=3.8.0 environment, including pytorch>=1.8

      ```bash
      git clone https://github.com/AIDrive-Research/Custom-Algorithm.git
      cd Custom-Algorithm/docs/ModelQuantization/Classification/Resnet18
      pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
      ```

## Data Preparation

The dataset structure is as follows:

```bash
|-dataset
   |-images
      |- 0
         |-xxxxx.jpg
         |-xxxxx.jpg
         |...
      |- 1
         |-xxxxx.jpg
         |-xxxxx.jpg
         |...
      |...
   |-train
      |- 0
         |-xxxxx.jpg
         |-xxxxx.jpg
         |...
      |- 1
         |-xxxxx.jpg
         |-xxxxx.jpg
         |...
      |...
   |-test
      |- 0
         |-xxxxx.jpg
         |-xxxxx.jpg
         |...
      |- 1
         |-xxxxx.jpg
         |-xxxxx.jpg
         |...
      |...
```

## Data Partition

Place the `dataset` in the `images` folder under dataset, and organize it by category: the `0` folder represents the first category, the `1` folder represents the second category, and so on. Execute the following code to partition the dataset and obtain the training set and validation set.   
Note: Modify `src_path`, `train_path`, and `test_path` to your own dataset paths.

```bash
python split_train_test.py
```

## Model Training

Modify  `n_classes` in the configuration parameters of `train.py` to the number of categories in your own dataset, and update `train_dataset` and `test_dataset` to your own data paths. Execute the following code.

```
python train.py
```