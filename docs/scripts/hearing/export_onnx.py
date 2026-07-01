# AudioClassification-Pytorch-master/export_onnx.py
import argparse
import os

import torch
import yaml

from macls.data_utils.featurizer import AudioFeaturizer
from macls.models import build_model
from macls.utils.utils import dict_to_object, print_arguments


def _load_configs(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        configs = yaml.load(f.read(), Loader=yaml.FullLoader)
    return dict_to_object(configs)


def _resolve_model_path(model_path):
    if os.path.isdir(model_path):
        model_path = os.path.join(model_path, "model.pth")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"{model_path} 模型不存在！")
    return model_path


def _resolve_num_class(configs):
    if configs.model_conf.model_args.get("num_class", None) is None:
        with open(configs.dataset_conf.label_list_path, "r", encoding="utf-8") as f:
            labels = [l.strip() for l in f.readlines()]
        configs.model_conf.model_args.num_class = len(labels)


def main():
    parser = argparse.ArgumentParser(description="Export MACls model to ONNX")
    parser.add_argument("--configs", type=str, default="configs/resnet_se.yml", help="配置文件路径")
    parser.add_argument("--model_path", type=str, default="models/ResNetSE_Fbank/best_model", help="模型文件夹路径或model.pth路径")
    parser.add_argument("--onnx_path", type=str, default="models/ResNetSE_Fbank/best_model/model_rknn.onnx", help="导出ONNX路径")
    parser.add_argument("--num_frames", type=int, default=300, help="虚拟输入的帧数（时间维度长度）")
    parser.add_argument("--opset", type=int, default=11, help="ONNX opset版本")
    parser.add_argument("--dynamic", action="store_true", help="是否开启动态输入维度（batch与时间维度）")
    args = parser.parse_args()

    configs = _load_configs(args.configs)
    print_arguments(configs=configs, title="配置文件参数")
    _resolve_num_class(configs)

    featurizer = AudioFeaturizer(
        feature_method=configs.preprocess_conf.feature_method,
        use_hf_model=configs.preprocess_conf.get("use_hf_model", False),
        method_args=configs.preprocess_conf.get("method_args", {}),
    )
    input_size = featurizer.feature_dim

    model = build_model(input_size=input_size, configs=configs)
    model_path = _resolve_model_path(args.model_path)
    state_dict = torch.load(model_path, weights_only=False, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    dummy_input = torch.randn(1, args.num_frames, input_size, dtype=torch.float32)

    input_names = ["input"]
    output_names = ["logits"]
    dynamic_axes = None
    if args.dynamic:
        dynamic_axes = {"input": {0: "batch", 1: "frames"}, "logits": {0: "batch"}}

    os.makedirs(os.path.dirname(args.onnx_path) or ".", exist_ok=True)
    torch.onnx.export(
        model,
        dummy_input,
        args.onnx_path,
        export_params=True,
        opset_version=args.opset,
        do_constant_folding=True,
        input_names=input_names,
        output_names=output_names,
        dynamic_axes=dynamic_axes,
    )
    print(f"ONNX已导出：{args.onnx_path}")


if __name__ == "__main__":
    main()
