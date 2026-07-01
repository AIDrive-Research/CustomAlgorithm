import argparse
import os

import onnx
from onnxsim import simplify


def _parse_args():
    parser = argparse.ArgumentParser(description="Simplify ONNX model with onnxsim")
    parser.add_argument(
        "--onnx_in",
        type=str,
        required=True,
        help="输入ONNX路径",
    )
    parser.add_argument(
        "--onnx_out",
        type=str,
        required=True,
        help="输出ONNX路径",
    )
    parser.add_argument(
        "--num_frames",
        type=int,
        default=300,
        help="静态时间维度长度",
    )
    parser.add_argument(
        "--feature_dim",
        type=int,
        default=80,
        help="特征维度，Fbank默认80",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    if not os.path.exists(args.onnx_in):
        raise FileNotFoundError(f"ONNX不存在：{args.onnx_in}")

    model = onnx.load(args.onnx_in)
    input_shapes = {"input": [1, args.num_frames, args.feature_dim]}
    model_simp, check = simplify(model, input_shapes=input_shapes)
    if not check:
        raise RuntimeError("onnxsim 校验失败")

    os.makedirs(os.path.dirname(args.onnx_out) or ".", exist_ok=True)
    onnx.save(model_simp, args.onnx_out)
    print(f"ONNX已简化：{args.onnx_out}")


if __name__ == "__main__":
    main()
