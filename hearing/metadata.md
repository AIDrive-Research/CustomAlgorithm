# metadata.json

Current `hazardous_sound_detection` example:

```json
{
  "name": "hazardous_sound_detection",
  "version": "968-20260415",
  "category": "aed"
}
```

Field description:

- `name`: English name of the algorithm package. It is recommended to keep it consistent with the algorithm package folder name.
- `version`: Algorithm package version. It is recommended to define it based on the device model and date, for example `968-20260415`.
- `category`: Algorithm category. The current hearing hazardous sound detection algorithm uses `aed`.

**Custom Algorithm Requirements:**

- `name` must not conflict with built-in algorithms on the device or with other custom algorithms.
- If the algorithm package folder is changed from `hazardous_sound_detection` to another name, update this field accordingly.
- Update `version` whenever the model is replaced, categories are changed, or post-processing logic is modified.
- `metadata.json` must be placed in the root directory of the algorithm package:

```text
AED/hazardous_sound_detection/metadata.json
```
