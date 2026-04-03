#!/usr/bin/env python3
import argparse

TEMPLATES = {
    "training": "你现在最想优先验证的单一变量是哪个（学习率、batch size、正则项）？",
    "writing": "你这段结论里，最缺的是证据、对比还是局限性说明？",
    "experiment": "当前现象最可能对应的两个假设是什么？你先验证哪一个？",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="shimei-lab question generator")
    parser.add_argument("--type", choices=sorted(TEMPLATES), default="experiment")
    args = parser.parse_args()
    print(TEMPLATES[args.type])


if __name__ == "__main__":
    main()
