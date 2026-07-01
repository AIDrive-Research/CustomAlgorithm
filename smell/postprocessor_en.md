# postprocessor_en

`postprocessor_en`: Contains the English post-processing configuration for smell algorithms. It defines the algorithm display name, description, class mapping, display colors, alert labels, and configurable UI parameters for the English interface. If the project only requires a Chinese interface, this folder can be removed.

This module contains 2 parts:
- Front-end configuration file: [air_alcohol_coffee_recognition.json](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_en/air_alcohol_coffee_recognition.json)
- Algorithm configuration file: [postprocessor.yaml](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_en/postprocessor.yaml)

## 1. Front-end Configuration File: [air_alcohol_coffee_recognition.json](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_en/air_alcohol_coffee_recognition.json)

**Custom Algorithm Requirements:**

- Rename `air_alcohol_coffee_recognition.json` to the algorithm package name with the `.json` suffix.
- `basicParams -> alg_type`: smell algorithms must use `olfaction`.
- `basicParams -> model_args -> air_alcohol_coffee_recognition`: change this key to the model instance name defined in `model.yaml`.
- `basicParams -> reserved_args -> display_name`: the algorithm name displayed in the English interface.
- `basicParams -> reserved_args -> sound_text`: the English voice broadcast text.
- `renderParams -> model_args -> model instance name -> conf_thres -> label`: the English label for the recognition confidence threshold.
- `renderParams -> model_args -> model instance name -> conf_thres -> tooltip`: the English description for the recognition confidence threshold.

For the complete front-end configuration parameter reference, see [Parameter Description](../docs/Postprocessor/README_JSON_en.md).

## 2. Algorithm Configuration File: [postprocessor.yaml](./SmellRecognition/air_alcohol_coffee_recognition/postprocessor_en/postprocessor.yaml)

```yaml
display_name: Air Alcohol Coffee Recognition
desc: Odor recognition algorithm based on smell sensors;Can identify air, alcohol, coffee and other odors;Uses SVM classification model;Collects data through 10 sensors;Adjustable confidence threshold;Suitable for environmental monitoring, safety detection and other scenarios
group_name: Odor Recognition
model:
  zql_air_alcohol_coffee_recognition:
    label:
      class2label:
        0: air
        1: alcohol
        2: coffee
      label_map:
        air: Air
        alcohol: Alcohol
        coffee: Coffee
      label2color:
        Air: [0, 255, 0]
        Alcohol: [255, 0, 0]
        Coffee: [139, 69, 19]
alert_label: [Alcohol, Coffee]
process_time: null
```

**Custom Algorithm Requirements:**

- `display_name`: the algorithm name. It should be consistent with `display_name` in the front-end configuration file.
- `desc`: the algorithm description shown in the algorithm repository.
- `group_name`: the algorithm group shown in the algorithm repository.
- `class2label`: maps numeric model output classes to internal labels.
- `label_map`: maps internal labels to English display names.
- `label2color`: defines the default display color for each English display name.
- `alert_label`: specifies which English display names should trigger alerts.
- `process_time`: post-processing time. Smell algorithms can currently keep this value as `null`.

The default rule is: `Air` is the normal class and does not trigger alerts; `Alcohol` and `Coffee` are target odor classes and trigger alerts when detected.
