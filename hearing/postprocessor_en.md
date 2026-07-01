# postprocessor_en

`postprocessor_en` contains the English post-processing configuration for hearing algorithms. It defines the algorithm display name, description, model output label mapping, alarm labels, browser voice broadcast text, and configurable parameters shown in the English UI.

*If an English version of the algorithm package is not required, this folder can be omitted.*

Current example path:

```text
AED/hazardous_sound_detection/postprocessor_en
```

The `postprocessor_en` folder contains 2 parts:

- Front-end configuration file: [hazardous_sound_detection.json](./AED/hazardous_sound_detection/postprocessor_en/hazardous_sound_detection.json)
- Algorithm configuration file: [postprocessor.yaml](./AED/hazardous_sound_detection/postprocessor_en/postprocessor.yaml)

## 1. Front-end Configuration File: [hazardous_sound_detection.json](./AED/hazardous_sound_detection/postprocessor_en/hazardous_sound_detection.json)

This file defines the parameters and default values displayed on the English interface when binding the algorithm.

Key configuration:

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
      "display_name": "Hazardous Sound Detection",
      "sound_text": "Hazardous sound detection alert"
    }
  }
}
```

Field description:

- `basicParams.alg_type`: Algorithm type. The current example uses `aed`.
- `basicParams.model_args.hazardous_sound_detection.conf_thres`: Default confidence threshold.
- `basicParams.reserved_args.display_name`: Algorithm name displayed on the interface.
- `basicParams.reserved_args.sound_text`: Browser voice broadcast text when an alarm is triggered.
- `renderParams.model_args.hazardous_sound_detection.conf_thres.label`: English label of the confidence threshold parameter.
- `renderParams.model_args.hazardous_sound_detection.conf_thres.tooltip`: English explanation of the confidence threshold parameter.

**Custom Algorithm Requirements:**

- Rename `hazardous_sound_detection.json` to `[algorithm_package_name].json`, for example: `custom_sound_detection.json`.
- The model instance name under `basicParams.model_args` must be consistent with the top-level model instance name in `model/model.yaml`.
- If the model instance name is changed from `hazardous_sound_detection` to another name, update both `basicParams.model_args` and `renderParams.model_args` accordingly.
- Modify `basicParams.reserved_args.display_name` to the English algorithm display name.
- Modify `basicParams.reserved_args.sound_text` to the English browser voice broadcast text.
- Modify `renderParams.model_args.[model_instance_name].conf_thres.label` and `tooltip` to match the custom algorithm scenario.

For a detailed explanation of front-end configuration parameters, see [Parameter Description](../docs/Postprocessor/README_JSON_en.md).

## 2. Algorithm Configuration File: [postprocessor.yaml](./AED/hazardous_sound_detection/postprocessor_en/postprocessor.yaml)

This file defines the algorithm repository display information, model label mapping, and alarm labels.

Current configuration example:

```yaml
display_name: Hazardous Sound Detection
desc: Suitable for hazardous sound detection in various scenarios; capable of identifying claps, alarms, crashes, distress sounds, and traffic hazard sounds
group_name: Sound Events
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
        Blast: Clap
        Alarm: Alarm
        Crash: Crash
        Distress: Distress
        Skid: Skid
alert_label: [ Clap, Alarm, Crash, Distress, Skid ]
process_time: null
```

Field description:

- `display_name`: English algorithm display name. It should be consistent with `display_name` in `hazardous_sound_detection.json`.
- `desc`: English algorithm description shown in the algorithm repository.
- `group_name`: English algorithm group name.
- `model`: Model-related post-processing configuration.
- `class2label`: Mapping from model output class IDs to internal labels.
- `label_map`: Mapping from internal labels to English display names.
- `alert_label`: English display names that trigger alarms after label mapping.
- `process_time`: Post-processing time field. The current example uses `null`.

**Custom Algorithm Requirements:**

- The model instance name under `model` must be consistent with the top-level model instance name in `model/model.yaml`.
- `class2label` must cover all output classes of the model.
- `label_map` should use stable internal labels as keys and English UI display names as values.
- Values in `alert_label` must use the English display names after `label_map`, not the internal model labels.
- If the category order changes, update `class2label`, `label_map`, and `alert_label` together.
- Keep the category IDs and internal labels consistent with `postprocessor_zh/postprocessor.yaml`; only the display names should differ by language.

## 3. Common Modification Points

When customizing a hazardous sound detection algorithm, the following files usually need to be modified:

```text
postprocessor_en/hazardous_sound_detection.json
postprocessor_en/postprocessor.yaml
```

If only the model file is replaced and the categories remain unchanged, usually only the threshold, display name, description, and voice broadcast text need to be checked.

If the categories are changed, update all of the following fields together:

- `postprocessor_en/postprocessor.yaml` -> `class2label`
- `postprocessor_en/postprocessor.yaml` -> `label_map`
- `postprocessor_en/postprocessor.yaml` -> `alert_label`
- `postprocessor_en/hazardous_sound_detection.json` -> display name, voice broadcast text, and threshold-related UI text
