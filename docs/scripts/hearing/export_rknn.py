import argparse
import os

from rknn.api import RKNN


def _parse_args():
    parser = argparse.ArgumentParser(description="Export RKNN model from ONNX")
    parser.add_argument(
        "--onnx_path",
        type=str,
        required=True,
        help="ONNX模型路径",
    )
    parser.add_argument(
        "--rknn_path",
        type=str,
        required=True,
        help="输出RKNN模型路径",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="rk3588",
        help="目标平台，如rk3588",
    )
    parser.add_argument(
        "--num_frames",
        type=int,
        default=300,
        help="输入帧数，与导出ONNX时一致",
    )
    parser.add_argument(
        "--feature_dim",
        type=int,
        default=80,
        help="特征维度，Fbank默认80",
    )
    parser.add_argument(
        "--do_quant",
        action="store_true",
        help="是否开启量化（需要--dataset）",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="",
        help="量化数据集文本路径（每行一个样本路径）",
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    if not os.path.exists(args.onnx_path):
        raise FileNotFoundError(f"ONNX不存在：{args.onnx_path}")

    rknn = RKNN(verbose=True)
    rknn.config(
        target_platform=args.target,
    )

    ret = rknn.load_onnx(
        model=args.onnx_path,
        input_size_list=[[1, args.num_frames, args.feature_dim]],
    )
    if ret != 0:
        raise RuntimeError("load_onnx失败")

    if args.do_quant:
        if not args.dataset:
            raise ValueError("开启量化时必须提供--dataset")
        ret = rknn.build(do_quantization=True, dataset=args.dataset)
    else:
        ret = rknn.build(do_quantization=False)
    if ret != 0:
        raise RuntimeError("build失败")

    os.makedirs(os.path.dirname(args.rknn_path) or ".", exist_ok=True)
    ret = rknn.export_rknn(args.rknn_path)
    if ret != 0:
        raise RuntimeError("export_rknn失败")

    rknn.release()
    print(f"RKNN已导出：{args.rknn_path}")


if __name__ == "__main__":
    main()
