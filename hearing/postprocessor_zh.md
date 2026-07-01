# postprocessor_zh

`postprocessor_zh` 包含听觉算法中文后处理配置，用于定义算法在中文界面中的显示名称、描述信息、模型输出类别映射、告警类别、语音播报和可配置参数。

当前示例路径：

```text
AED/hazardous_sound_detection/postprocessor_zh
```

该模块包含 2 部分内容：

- 前端配置文件：`postprocessor_zh/hazardous_sound_detection.json`
- 算法配置文件：`postprocessor_zh/postprocessor.yaml`

## 1. 前端配置文件：`hazardous_sound_detection.json`

该文件用于定义绑定算法时界面显示的参数和默认值。

关键配置：

```json
{
  "basicParams": {
    "alg_type": "aed",
    "model_args": {
      "hazardous_sound_detection": {
        "conf_thres": 0.8
      }
    },
    "reserved_args": {
      "display_name": "危险声音检测",
      "sound_text": "危险声音检测告警"
    }
  }
}
```

字段说明：

- `basicParams.alg_type`：算法类型。当前示例为 `aed`。
- `basicParams.model_args.hazardous_sound_detection.conf_thres`：默认置信度阈值。
- `reserved_args.display_name`：算法在界面显示的名称。
- `reserved_args.sound_text`：告警时浏览器语音播报内容。
- `renderParams.model_args.hazardous_sound_detection.conf_thres.label`：置信度参数在界面上的中文名称。
- `renderParams.model_args.hazardous_sound_detection.conf_thres.tooltip`：置信度参数说明。

自定义算法要求：

- 文件名建议与算法包名称保持一致，即 `hazardous_sound_detection.json`。
- `model_args` 下的模型实例名必须与 `model/model.yaml` 顶层模型实例名一致。
- 如果模型实例名从 `hazardous_sound_detection` 改为其他名称，这里的 `basicParams.model_args` 和 `renderParams.model_args` 都要同步修改。
- `display_name` 和 `sound_text` 应与实际业务场景一致。

## 2. 算法配置文件：`postprocessor.yaml`

该文件定义算法仓库展示信息、类别映射和告警类别。

当前配置示例：

```yaml
display_name: 危险声音检测
desc: 适用于任意场景危险声音检测;可识别拍手声、警报声、撞击声、人身异常声音、交通危险音
group_name: 声音事件
model:
  hazardous_sound_detection:
    label:
      class2label:
        0: Blast
        1: Alarm
        2: Crash
        3: Distress
        4: Skid
      label_map:
        Blast: 拍手声
        Alarm: 警报声
        Crash: 撞击声
        Distress: 异常人声
        Skid: 交通危险音
alert_label: [ 拍手声, 警报声, 撞击声, 异常人声, 交通危险音 ]
process_time: null
```

字段说明：

- `display_name`：算法显示名称，应与 `hazardous_sound_detection.json` 中的 `display_name` 一致。
- `desc`：算法描述，在算法仓库中显示。
- `group_name`：算法分组。
- `class2label`：模型输出类别 ID 到内部标签的映射。
- `label_map`：内部标签到中文显示名称的映射。
- `alert_label`：命中后触发告警的中文显示名称。
- `process_time`：后处理耗时字段。当前配置为 `null`。

注意事项：

- `class2label` 必须覆盖模型输出的全部类别。
- `alert_label` 中的值必须使用 `label_map` 后的中文显示名称，而不是模型内部标签。
- 如果类别顺序变化，必须同步更新 `class2label`、`label_map` 和 `alert_label`。

## 3. 常见修改点

自定义危险声音检测算法时，通常需要修改：

```text
postprocessor_zh/hazardous_sound_detection.json
postprocessor_zh/postprocessor.yaml
```

只换模型但类别不变时，通常只需要检查阈值和描述文本。

换类别时，必须同步修改：

- `postprocessor_zh/postprocessor.yaml` 中的 `class2label`
- `postprocessor_zh/postprocessor.yaml` 中的 `label_map`
- `postprocessor_zh/postprocessor.yaml` 中的 `alert_label`
- `postprocessor_zh/hazardous_sound_detection.json` 中的显示名称、播报文本和阈值文案

