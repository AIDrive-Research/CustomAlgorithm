# Complete Production Process of Instance Segmentation Algorithm Package

Creating an instance segmentation algorithm package is a very simple process. As long as you are a qualified algorithm engineer, proficient in the Python language, and work carefully and patiently, you can get it done in one day.

In total, you need to prepare three (or four if both Chinese and English are required) parts of files, which are:
- Model files and inference code: `model`
- Chinese post-processing configuration: `postprocessor_zh`
- English post-processing configuration: `postprocessor_en`
- Algorithm name and version number definition: `metadata.json`

## QuickStart
Before delving into the detailed process of creating an algorithm package, let's first take an existing algorithm package, simply package and upload it, to gain experience of success.

For detailed content, please refer to: [QuickStart.md](./QuickStart.md) 

## Model Files and Inference Code
The algorithm package imported into the device includes not only model files but also supporting model inference code. Therefore, we require that the name of your folder and the corresponding python file follow certain rules, so that the inference code can be properly embedded into the data flow. Simply put, the python file you `import` should be importable by the code in the data flow context, so that the image matrix data decoded from the video stream can be correctly fed into your algorithm model for inference.

For detailed content, please refer to: [model.md](./model.md) 

## 中文后处理配置
该部分的内容，主要完成以下工作：
- 对模型推理出来的结果做后处理，如过滤低置信度、根据多个目标的位置关系来决策等。
- 定义你的自定义算法在 `算法仓库` UI上的显示名称、描述信息。
- 定义你的自定义算法在 `实时画面` UI上目标框的颜色、显示内容等。
- 定义你的自定义算法在 `算法绑定摄像头` UI上的设置项，包含统计投票告警、默认语音播报的声音内容、检测置信度等。

详细内容请参考：[postprocessor_zh.md](./postprocessor_zh.md) 

## English Post-Processing Configuration
This part mainly accomplishes the following tasks:
- Perform post-processing on the results inferred by the model, such as filtering low-confidence results, making decisions based on the positional relationships of multiple targets, etc.
- Define the display name and description information of your custom algorithm on the `Algorithm` UI.
- Define the color of the target frame and the displayed content of your custom algorithm on the `Real-time Screen` UI.
- Define the settings of your custom algorithm on the `Data Access` UI, including statistical voting alarms, the default voice broadcast content, detection confidence, etc.

For detailed content, please refer to: [postprocessor_en.md](./postprocessor_en.md) 

## Algorithm Name and Version Number Definition

Only two lines of content need to be modified here:

- Give your algorithm package an English name, ensuring it does not duplicate existing names in the device. Therefore, we recommend adding a unique and distinctive prefix or suffix to the name, such as `fire_0001`.

- Define the version number of your algorithm package. We suggest using the current date as the version number, such as `ks968-20251110`.

For detailed content, please refer to: [metadata.md](./metadata.md) 