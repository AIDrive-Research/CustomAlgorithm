# postprocessor_zh

`postprocessor_zh`：包含嗅觉算法中文后处理配置，用于定义算法在中文界面中的显示名称、描述、分类映射、显示颜色、告警类别和页面可配置参数。需要制作中文版算法包时，应保留该文件夹。

该模块包含 2 部分内容：
- 前端配置文件：[air_alcohol_coffee_recognition.json](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_zh/air_alcohol_coffee_recognition.json)
- 算法配置文件：[postprocessor.yaml](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_zh/postprocessor.yaml)

## 1. 前端配置文件：[air_alcohol_coffee_recognition.json](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_zh/air_alcohol_coffee_recognition.json)

该文件用于定义配置算法时界面显示的参数及默认值。

关键配置示例：

```json
{
  "basicParams": {
    "alg_type": "olfaction",
    "model_args": {
      "zql_air_alcohol_coffee_recognition": {
        "conf_thres": 0.55
      }
    },
    "reserved_args": {
      "display_name": "空气酒精咖啡识别",
      "sound_text": "检测到异常气味"
    }
  }
}
```

**自定义算法要求：**

- `air_alcohol_coffee_recognition.json` 修改为算法包名称 `.json`。
- `basicParams -> alg_type`：嗅觉算法固定为 `olfaction`。
- `basicParams -> model_args -> zql_air_alcohol_coffee_recognition`：需要修改为 `model.yaml` 中的模型实例名称。
- `basicParams -> reserved_args -> display_name`：算法在界面中的显示名称。
- `basicParams -> reserved_args -> sound_text`：告警时浏览器语音播报内容。
- `renderParams -> model_args -> 模型实例名 -> conf_thres -> label`：识别置信度阈值在中文界面中的名称。
- `renderParams -> model_args -> 模型实例名 -> conf_thres -> tooltip`：识别置信度阈值的中文说明。

完整的前端配置文件参数说明，详见 [参数说明](../../../docs/Postprocessor/README_JSON_zh.md)

## 2. 算法配置文件：[postprocessor.yaml](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_zh/postprocessor.yaml)

```yaml
display_name: 空气酒精咖啡识别
desc: 基于嗅觉传感器的气味识别算法;可识别空气、酒精、咖啡等气味;采用SVM分类模型;通过10个传感器采集数据;置信度阈值可调节;适用于环境监测、安全检测等场景
group_name: 嗅觉识别
model:
  zql_air_alcohol_coffee_recognition:
    label:
      class2label:
        0: air
        1: alcohol
        2: coffee
      label_map:
        air: 空气
        alcohol: 酒精
        coffee: 咖啡
      label2color:
        空气: [0, 255, 0]
        酒精: [255, 0, 0]
        咖啡: [139, 69, 19]
alert_label: [酒精, 咖啡]
process_time: null
```

**自定义算法要求：**

- `display_name`：算法名称，与前端配置文件中的 `display_name` 保持一致。
- `desc`：算法说明，在算法仓库的算法描述中显示。
- `group_name`：算法分组，在算法仓库中显示。
- `class2label`：将模型输出的数字分类映射为内部标签。
- `label_map`：将内部标签映射为中文显示名称。
- `label2color`：不同显示名称对应的界面颜色。
- `alert_label`：指定哪些中文显示名称命中后触发告警。
- `process_time`：后处理耗时字段，嗅觉算法当前可保持为 `null`。

当前规则是：`空气` 为正常类别，不告警；`酒精` 和 `咖啡` 为目标气味，命中后告警。
