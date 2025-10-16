#!/usr/bin/env python3
import os
import re
import sys
from typing import List
try:
    from pypinyin import lazy_pinyin
except Exception:
    lazy_pinyin = None

PHRASE_MAP = [
    ("开箱上手指南", "Getting Started"),
    ("快速启动优化指南", "Quick Start Optimization Guide"),
    ("快速启动", "Quick Start"),
    ("优化指南", "Optimization Guide"),
    ("软件开发包", "Software Development Kit"),
    ("基础文档", "Basic Documentation"),
    ("调优参考文档", "Optimization Reference"),
    ("测试报告", "Test Reports"),
    ("配套芯片资料", "Supporting Chip Documentation"),
    ("软件相关", "Software"),
    ("硬件相关", "Hardware"),
    ("工具链", "Toolchain"),
    ("工具", "Tools"),
    ("配置类", "Configurations"),
    ("典型场景", "Typical Scenarios"),
    ("模型", "Model"),
    ("芯片", "Chip"),
    ("子板", "Sub-board"),
    ("图像", "Image"),
    ("功耗", "Power Consumption"),
    ("外设", "Peripherals"),
    ("硬件", "Hardware"),
    ("音频", "Audio"),
    ("视频", "Video"),
    ("颜色", "Color"),
    ("畸变矫正", "Distortion Correction"),
    ("防抖", "Stabilization"),
    ("标定", "Calibration"),
    ("矫正", "Correction"),
    ("参考原理图", "Reference Schematics"),
    ("参考PCB", "Reference PCB"),
    ("原理图", "Schematics"),
    ("参考", "Reference"),
    ("使用指南", "User Guide"),
    ("开发参考", "Development Reference"),
    ("开发指南", "Development Guide"),
    ("整体说明", "Overview"),
    ("说明文档", "Documentation"),
    ("说明", "Guide"),
    ("接口协议", "Interface Specification"),
    ("详细设计", "Detailed Design"),
    ("调试", "Debugging"),
    ("添加与调试", "Adding and Debugging"),
    ("注意事项", "Notes"),
    ("参数", "Parameters"),
    ("调用规则", "Invocation Rules"),
    ("效果", "Quality"),
    ("介绍", "Introduction"),
    ("说明书", "Manual"),
    ("用户指南", "User Guide"),
    ("升级", "Upgrade"),
    ("烧录", "Burning"),
    ("镜像", "Image"),
    ("打包", "Packaging"),
    ("文件系统", "File System"),
    ("开发环境", "Development Environment"),
    ("外围设备驱动", "Peripheral Drivers"),
    ("驱动", "Driver"),
    ("使用", "Usage"),
    ("配置", "Configuration"),
    ("参数设置", "Parameter Settings"),
    ("性能统计", "Performance Statistics"),
    ("模型编译", "Model Compilation"),
    ("拉流工具", "Streaming Tools"),
    ("上传工具", "Upload Tool"),
    ("图像质量", "Image Quality"),
    ("离线仿真", "Offline Simulation"),
    ("量产", "Mass Production"),
    ("质量", "Quality"),
    ("兼容性", "Compatibility"),
    ("测试", "Test"),
    ("报告", "Report"),
    ("可靠性报告", "Reliability Report"),
    ("可靠性", "Reliability"),
    ("防护设计", "Protection Design"),
    ("失效引脚汇总", "Failed Pins Summary"),
    ("芯片简介", "Chip Introduction"),
    ("数据手册", "Datasheet"),
    ("适配指南", "Adaptation Guide"),
    ("引脚", "Pin"),
    ("定义", "Definition"),
    ("系列", "Series"),
    ("整体函数列表", "Overall Function List"),
    ("低功耗模式", "Low Power Mode"),
    ("场景样例", "Scene Samples"),
    ("图像调优", "Image Tuning"),
    ("死机问题定位", "Crash Debugging"),
    ("流程", "Process"),
    ("网络", "Network"),
    ("使能", "Enable"),
    ("ISP", "ISP"), ("ISPLite", "ISPLite"), ("AIISP", "AIISP"), ("VIN", "VIN"), ("VPSS", "VPSS"), ("VPU", "VPU"), ("HAPI", "HAPI"), ("SVP", "SVP"), ("PMIC", "PMIC"), ("AWB", "AWB"), ("MIPI", "MIPI"), ("NorFlash", "NorFlash"), ("Ubuntu", "Ubuntu")
]

PUNCT_MAP = {
    '（': '(', '）': ')', '：': '-', '；': ',', '、': ',', '，': ',', '。': '.', '！': '!', '？': '?',
    '【': '[', '】': ']', '《': ' ', '》': ' ', '“': '"', '”': '"', '‘': "'", '’': "'",
    '—': '-', '–': '-', '·': '-', '\u00A0': ' ', '　': ' ',
}

re_non_ascii = re.compile(r'[^\x00-\x7F]')
PHRASE_PATTERNS = [(re.compile(re.escape(k)), v) for k, v in PHRASE_MAP]

def translate_component(name: str) -> str:
    stem, ext = os.path.splitext(name)
    s = stem
    for k, v in PUNCT_MAP.items():
        s = s.replace(k, v)
    for pat, repl in PHRASE_PATTERNS:
        s = pat.sub(repl, s)
    if re_non_ascii.search(s):
        if lazy_pinyin:
            out = []
            for ch in s:
                if ord(ch) < 128:
                    out.append(ch)
                else:
                    out.append(lazy_pinyin(ch)[0])
            s = ''.join(out)
        else:
            s = re_non_ascii.sub('', s)
    s = re.sub(r'[\s]+', ' ', s).strip()
    s = s.replace('_', ' ')
    s = re.sub(r'\s+', ' ', s)
    s = s.replace('/', '-')
    s = re.sub(r'[\\:*?"<>|]', '-', s)
    if not s:
        s = 'item'
    return s + ext

def collect_files(base: str) -> List[str]:
    files: List[str] = []
    for root, dirs, fs in os.walk(base):
        # Prune version-control and virtualenv/cache directories
        dirs[:] = [d for d in dirs if d not in ('.git', '.svn', '.hg', '.venv', '__pycache__')]
        for f in fs:
            files.append(os.path.join(root, f))
    return files

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--dest', default='.')
    ap.add_argument('--prefix', default='')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    src_base = os.path.abspath(args.src)
    dest_base = os.path.abspath(args.dest)
    rel_from_dest_to_src = os.path.relpath(src_base, dest_base)

    created = 0
    planned = 0
    files = collect_files(src_base)

    for full in files:
        rel = os.path.relpath(full, src_base)
        parts = rel.split(os.sep)
        eng_parts = [translate_component(p) for p in parts]
        eng_rel = os.path.join(args.prefix, *eng_parts)
        eng_path = os.path.join(dest_base, eng_rel)
        parent = os.path.dirname(eng_path)
        if not args.dry_run:
            os.makedirs(parent, exist_ok=True)
        target = os.path.join(rel_from_dest_to_src, rel)
        planned += 1
        if args.dry_run:
            print(f"LINK: {eng_rel} -> {target}")
            continue
        if os.path.lexists(eng_path):
            try:
                if os.path.islink(eng_path) and os.readlink(eng_path) == target:
                    continue
                base, ext = os.path.splitext(os.path.basename(eng_path))
                i = 1
                while True:
                    alt = os.path.join(parent, f"{base}_{i}{ext}")
                    if not os.path.exists(alt) and not os.path.islink(alt):
                        eng_path = alt
                        break
                    i += 1
            except OSError:
                pass
        try:
            if os.path.lexists(eng_path):
                os.remove(eng_path)
            os.symlink(target, eng_path)
            created += 1
        except FileExistsError:
            pass
    print(f"Planned: {planned}, Created: {created}")

if __name__ == '__main__':
    main()

