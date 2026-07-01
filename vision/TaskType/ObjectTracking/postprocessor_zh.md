# postprocessor_zh

`postprocessor_zh`：包含算法后处理相关代码。例如，当模型识别到人体时不直接触发告警，而是在人体框跨线时才告警，这类功能便在此实现。此外，该文件夹内容还会决定前端页面的展示效果（如目标框颜色、语言等）。当需要制作中文版算法包时，需包含该文件夹，否则可将其删除。

*若不需中文版算法包，可跳过该章节*  

该模块包含3部分内容：  
- 前端配置文件：[person_counting_demo.json](./person_counting_demo/postprocessor_zh/person_counting_demo.json)
- 算法配置文件：[postprocessor.yaml](./person_counting_demo/postprocessor_zh/postprocessor.yaml)
- 后处理代码：[person_counting_demo.py](./person_counting_demo/postprocessor_zh/person_counting_demo.py) 

## 1. 前端配置文件：[person_counting_demo.json](./person_counting_demo/postprocessor_zh/person_counting_demo.json)

用于定义在配置算法时，界面显示的参数及默认值。如下图： 

![](../../../docs/assets/person_counting_demo_1.png)  

**自定义算法要求：**  

- `person_counting_demo.json` 修改为 算法包名称.json，如：`custom_counting.json`；

- 将 `basicParams` -> `model_args` -> `custom_person_demo` 修改为 `model` 文件夹中模型名称；

- 将 `basicParams` -> `reserved_args` -> `display_name` 修改为显示的算法名称；

- 将 `basicParams` -> `reserved_args` -> `sound_text` 修改为语音播报名称；

- 将 `renderParams` -> `model_args` -> `custom_person_demo` 修改为 `model` 文件夹中模型名称；

- 将 `renderParams` -> `model_args` -> `custom_person_demo` -> `conf_thres` -> `label` 修改为 `conf_thres`参数的中文名称；

- 将 `renderParams` -> `model_args` -> `custom_person_demo` -> `conf_thres` -> `tooltip` 修改为对该参数的解释说明；

完整的前端配置文件参数说明，详见 [参数说明](../../../docs/Postprocessor/README_JSON_zh.md)

## 2. 算法配置文件：[postprocessor.yaml](./person_counting_demo/postprocessor_zh/postprocessor.yaml)

部分参数用于算法展示。如下图：  
![](../../../docs/assets/person_counting_demo_2.png)  

```bash
display_name: 人员计数(样例)
desc: "适用于园区、商场场景下人员计数与流量统计;需标记虚拟直线，并确定人员跨线的方向;可标记多条虚拟直线;画面清晰，可辨别人员特征;人员目标不小于画面大小5%;识别距离小于20m最佳（200万@6mm）;建议检测频率：不低于2次/秒"
group_name: 人员管理
model:
  custom_person_demo:                  # 模型名称，model内模型文件夹名字
    label:
      class2label:
        0: person
      label_map:
        person: 人
      label2color:
        人: [ 0, 255, 0 ]
alert_label: []
process_time: 30
```

**自定义算法要求：**  
- `display_name`: 如图【3】，算法名称，与 `person_counting_demo.json` 中 `display_name` 保持一致；

- `desc`：如图【4】，算法描述；

- `group_name`：如图【2】，算法分组；

- `model`：模型参数；  
    - `class2label`：指定模型的输出类别、名称，需修改为自训练模型的输出类别和名称；
    - `label_map`：输出对应的界面显示名称；
    - `label2color`：不同类别默认的矩形框颜色。

- `alert_label`：指定告警类别，也可在后处理文件中定义。

- `process_time`：后处理所需的时间，用于计算抽帧间隔。

## 3. 后处理代码：[person_counting_demo.py](./person_counting_demo/postprocessor_zh/person_counting_demo.py) 

负责解析推理输出、筛选目标并生成最终检测结果。包含2个核心函数：`_filter`、`_process`。

**自定义算法要求：**  

- `person_counting_demo.py` 修改为 算法包名称.py，如：`custom_counting.py`。  
- 若需要对检测结果做其他逻辑处理，需自行修改代码。

`person_counting_demo.py`实现的功能：

**`_filter`**

该函数用于初步处理模型推理的结果，完成对目标的多条件过滤，包括：置信度低于阈值的目标、不在配置列表中的目标、不在指定多边形内的目标。 

**`_process`**

该函数判断模型检测结果是是否按标记的方向跨线，若有则产生告警。