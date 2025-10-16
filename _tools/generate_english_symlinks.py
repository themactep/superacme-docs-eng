#!/usr/bin/env python3
import os
import re
import sys
from typing import List
try:
    from pypinyin import lazy_pinyin
except Exception:
    lazy_pinyin = None

# Only treat these as true file extensions; otherwise, keep the dot as part of the name
KNOWN_EXTS = {
    'pdf','doc','docx','ppt','pptx','xls','xlsx','xlsm','txt','md','csv','json','yaml','yml',
    'zip','rar','7z','gz','bz2','xz','tar','tgz','tbz2',
    'deb','rpm','bin','exe','dll','so','a','o',
    'png','jpg','jpeg','gif','bmp','tiff','svg',
    'dsn','brd'
}

# Folder-specific overrides for exact filenames
GETTING_STARTED_CN = ["00.基础文档", "软件相关", "开箱上手指南"]
OVERRIDE_FILES = {
    # 00.Basic Documentation/Software/Getting Started/
    "EVB配置网络.pdf": "EVB Network Configuration.pdf",
    "Linux 编译 sample环境搭建指引v1.1.pdf": "Linux Compilation Sample Environment Setup Guide v1.1.pdf",
    "SA62105X2 Bring-Up应用指南v0.3.pdf": "SA62105X2 Bring-Up Application Guide v0.3.pdf",
    "SA62系列AI算法部署指南v1.0.pdf": "SA62 Series AI Algorithm Deployment Guide v1.0.pdf",
    "SA62系列_NorFlash固件烧录指南v1.5.pdf": "SA62 Series NorFlash Firmware Burning Guide v1.5.pdf",
    "SA62系列_V13功耗板_AI_Robot使用指南v0.5.pdf": "SA62 Series V13 Power Consumption Board AI Robot User Guide v0.5.pdf",
    "SA62系列  回板验证操作指南v0.2.pdf": "SA62 Series Board Verification Operation Guide v0.2.pdf",
    "！SA62系列 开箱上手指南v1.9.pdf": "SA62 Series Unboxing and Getting Started Guide v1.9.pdf",
    "Ubuntu 22.04 开发环境配置说明文档.pdf": "Ubuntu 22.04 Development Environment Configuration Instructions.pdf",
    "使能usb host的网络功能.pdf": "Enabling the USB Host Network Function.pdf",
}

# 00.Basic Documentation/Software/SDK overrides
SDK_CN = ["00.基础文档", "软件相关", "SDK"]
OVERRIDE_SDK = {
    "SA62系列 3A 软件开发参考v0.93.pdf": "SA62 Series 3A Software Development Reference v0.93.pdf",
    "SA62系列 AUDIO HAPI 软件开发参考_V0.9.pdf": "SA62 Series AUDIO HAPI Software Development Reference v0.9.pdf",
    "SA62系列 AUDIO 软件开发参考v2.5.3.pdf": "SA62 Series AUDIO Software Development Reference v2.5.3.pdf",
    "SA62系列 CRYPTO 密码算法库软件开发参考_V0.56.pdf": "SA62 Series CRYPTO Cryptographic Algorithm Library Software Development Reference v0.56.pdf",
    "SA62系列 FILTER 媒体处理软件开发参考_V0.6.pdf": "SA62 Series Filter Media Processing Software Development Reference v0.6.pdf",
    "SA62系列 ISP 软件开发参考v0.82.pdf": "SA62 Series ISP Software Development Reference v0.82.pdf",
    "SA62系列 MAPI整体函数列表.XLSX": "SA62 Series MAPI Function List.XLSX",
    "SA62系列 MEDIA HAPI 软件开发参考_V0.14.pdf": "SA62 Series MEDIA HAPI Software Development Reference v0.14.pdf",
    "SA62系列 MIPI使用指南_V0.6.pdf": "SA62 Series MIPI User Guide v0.6.pdf",
    "SA62系列 REGION 软件开发参考_V0.5.16.pdf": "SA62 Series REGION Software Development Reference v0.5.16.pdf",
    "SA62系列 SDK 整体说明v0.6.pdf": "SA62 Series SDK Overview v0.6.pdf",
    "SA62系列 Sensor添加与调试指南v0.81.pdf": "SA62 Series Sensor Adding and Debugging Guide v0.81.pdf",
    "SA62系列 Sensor调试注意事项.pdf": "SA62 Series Sensor Debugging Precautions.pdf",
    "SA62系列 SENSOR 软件开发参考_V0.55.pdf": "SA62 Series Sensor Software Development Reference V0.55.pdf",
    "SA62系列 SVP 软件开发参考_V0.5.9.pdf": "SA62 Series SVP Software Development Reference V0.5.9.pdf",
    "SA62系列 SYS HAPI 软件开发参考_V0.5.pdf": "SA62 Series SYS HAPI Software Development Reference V0.5.pdf",
    "SA62系列 SYS_软件开发参考_V0.5.19.pdf": "SA62 Series SYS Software Development Reference V0.5.19.pdf",
    "SA62系列_VIDEO_HAPI_软件开发参考_V3.0.pdf": "SA62 Series VIDEO HAPI Software Development Reference V3.0.pdf",
    "SA62系列 VIN 软件开发参考_V0.63.pdf": "SA62 Series VIN Software Development Reference V0.63.pdf",
    "SA62系列 VPSS 软件开发参考_V0.62.pdf": "SA62 Series VPSS Software Development Reference V0.62.pdf",
    "SA62系列 VPU 编码软件开发参考_V0.8.1.pdf": "SA62 Series VPU Encoding Software Development Reference V0.8.1.pdf",
    "SA62系列 VPU 解码软件开发参考0.5.3.pdf": "SA62 Series VPU Decoding Software Development Reference V0.5.3.pdf",
    "SA62系列 低功耗模式开发指南_v1.0.0.pdf": "SA62 Series Low Power Mode Development Guide v1.0.0.pdf",
    "SA62系列_双Sensor_mipi_switch方案调试注意事项.pdf": "SA62 Series Dual Sensor MIPI Switch Solution Debugging Notes.pdf",
    "SA62系列 快速启动优化指南_v1.8.0.pdf": "SA62 Series Quick Start Optimization Guide v1.8.0.pdf",
    "SA62系列音频算法参数调试指南_V0.2.pdf": "SA62 Series Audio Algorithm Parameter Debugging Guide v0.2.pdf",
    "SA62系列 音频设备树配置说明_v0.3.pdf": "SA62 Series Audio Device Tree Configuration Instructions v0.3.pdf",
}
# 00.Basic Documentation/Software/tools overrides
TOOLS_CN = ["00.基础文档", "软件相关", "tools"]
OVERRIDE_TOOLS = {
    "SA62系列 AWBTool工具使用指南.pdf": "SA62 Series AWBTool User Guide.pdf",
    "SA62_系列BSP工具说明v0.2.pdf": "SA62 Series BSP Tool Description v0.2.pdf",
    "SA62系列_BurnTool工具使用指南.pdf": "SA62 Series BurnTool User Guide.pdf",
    "SA62系列 streamer_media 离线仿真功能说明v0.4.pdf": "SA62 Series Streamer Media Offline Simulation Function Description v0.4.pdf",
    "SA62系列 UploadTool工具使用指南.pdf": "SA62 Series UploadTool User Guide.pdf",
    "SA62系列图像质量调试工具使用指南.pdf": "SA62 Series Image Quality Debugging Tool User Guide.pdf",
    "相机标定说明.pdf": "Camera Calibration Instructions.pdf",
    "研极微VNET虚拟网卡标准规范v0.3.pdf": "Yanji Micro VNET Virtual Network Card Standard Specification v0.3.pdf",
    "量产测试工具使用指南.pdf": "Mass Production Test Tool User Guide.pdf",
    "音频质量调试工具使用指南.pdf": "Audio Quality Debugging Tool User Guide.pdf",
}
# 00.Basic Documentation/Software/bsp overrides
BSP_CN = ["00.基础文档", "软件相关", "bsp"]
OVERRIDE_BSP = {
    "SA62系列 固件烧录与升级使用指南.pdf": "SA62 Series Firmware Flashing and Upgrade User Guide.pdf",
    "SA62系列 外围设备驱动开发指南_v1.0.pdf": "SA62 Series Peripheral Device Driver Development Guide v1.0.pdf",
    "SA62系列 开发环境用户指南.pdf": "SA62 Series Development Environment User Guide.pdf",
    "SA62系列 文件系统使用指南.pdf": "SA62 Series File System Usage Guide.pdf",
    "SA62系列 镜像打包工具使用指南.pdf": "SA62 Series Image Packaging Tool User Guide.pdf",
}

# 00.Basic Documentation/Hardware/Sub-board overrides
SUBBOARD_CN = ["00.基础文档", "硬件相关", "子板"]
OVERRIDE_SUBBOARD = {
    "EVB硬件参考设计_原理图_pcb.rar": "EVB Hardware Reference Design PCB Schematic.rar",
    "6920E2 V24 DEMO.tar": "6920E2 V24 DEMO.tar",
    "SA62105E_电源树V1.1.pdf": "SA62105E Power Tree V1.1.pdf",
    "V17_PowerTree.pdf": "SA62105X Power Tree V17.pdf",
}



# 00.Basic Documentation/Hardware/Chip overrides
CHIP_CN = ["00.基础文档", "硬件相关", "芯片"]
OVERRIDE_CHIP = {
    "SA62105E_pin_List_ver1.0.8.03.xlsx": "SA62105E_Pin_List_ver1.0.8.03.xlsx",
    "SA62105X_Pin定义_V1.2.xlsx": "SA62105X_Pin_Definition_V1.2.xlsx",
    "SA62105X芯片简介v1.2.pdf": "SA62105X Chip Overview v1.2.pdf",
    "SA62105系列_数据手册V0.32.pdf": "SA62105 Series_Datasheet V0.32.pdf",
    "研极SA62105E硬件用户指南V0.61.pdf": "Yanji SA62105E Hardware User Guide V0.61.pdf",
    "研极SA62105X硬件用户指南V0.87.pdf": "Yanji SA62105X Hardware User Guide V0.87.pdf",
    "研极SA62105芯片适配指南V0.44.pdf": "Yanji SA62105 Chip Adaptation Guide V0.44.pdf",
}

PHRASE_MAP = [
    # Prefer longer/specific phrases first
    ("环境搭建指引", "Environment Setup Guide"),
    ("环境搭建", "Environment Setup"),
    ("网络功能", "network function"),
    # Common words/terms
    ("编译", "Compilation"),
    ("环境", "Environment"),
    ("搭建", "Setup"),
    ("指引", "Guide"),
    ("功能", "function"),
    ("的", " "),
    # Existing mappings
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
    ("硬件参考设计", "Hardware Reference Design"),
    ("参考设计", "Reference Design"),
    ("设计", "Design"),
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
    ("指南", "Guide"),
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
    # If the extension is not a known file extension (e.g., '00.基础文档'), treat the dot as part of the name
    if ext and ext[1:].lower() not in KNOWN_EXTS:
        stem, ext = name, ''
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
    # Token normalization for common English words/abbreviations (run before spacing rules)
    # Normalize common tokens regardless of adjacency to non-ASCII
    s = re.sub(r'(?i)usb', 'USB', s)
    s = re.sub(r'(?i)sample', 'Sample', s)

    # Whitespace and visual separation improvements for Western readability
    # 1) Insert space between a letter and a CapitalizedWord (e.g., EHardware -> E Hardware)
    s = re.sub(r'([A-Za-z])([A-Z][a-z])', r'\1 \2', s)
    # 2) Insert space between lowerCase and any UpperCase (e.g., EnableUSB -> Enable USB)
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    # 3) Insert space between ALLCAPS and lowercase start (e.g., USBhost -> USB host)
    s = re.sub(r'([A-Z]{2,})([a-z])', r'\1 \2', s)
    # 4) Insert space between digit and letter (e.g., SA62105Series -> SA62105 Series)
    s = re.sub(r'(\d)([A-Za-z])', r'\1 \2', s)
    # 4) Insert space before version tokens like v1.2 or V1.2
    s = re.sub(r'(?i)(?<=\w)(v)(\d)', r' \1\2', s)

    # Collapse spaces in chip model tokens like SA62105E / SA62105X / SA62105X2
    s = re.sub(r'\b(SA\d{4,6})\s+([A-Z]\d?)\b', r'\1\2', s)
    # Collapse spaces for numeric prefix + letter+digits combos (e.g., 6920 E2 -> 6920E2)
    s = re.sub(r'(\d+)\s+([A-Z]\d+)\b', r'\1\2', s)

    # Prefer "USB host" styling
    s = re.sub(r'\bUSB\s+[Hh]ost\b', 'USB host', s)

    # Collapse and normalize spaces
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
        # Default translation for all components
        eng_parts = [translate_component(p) for p in parts]
        # Apply folder-specific overrides for filenames in Getting Started
        if len(parts) >= 4 and parts[0:3] == GETTING_STARTED_CN:
            orig_name = parts[-1]
            if orig_name in OVERRIDE_FILES:
                eng_parts = [translate_component(p) for p in parts[:-1]] + [OVERRIDE_FILES[orig_name]]
        # Apply folder-specific overrides for filenames in SDK
        if len(parts) >= 4 and parts[0:3] == SDK_CN:
            orig_name = parts[-1]
            if orig_name in OVERRIDE_SDK:
                eng_parts = [translate_component(p) for p in parts[:-1]] + [OVERRIDE_SDK[orig_name]]
        # Apply folder-specific overrides for filenames in tools
        if len(parts) >= 4 and parts[0:3] == TOOLS_CN:
            orig_name = parts[-1]
            if orig_name in OVERRIDE_TOOLS:
                eng_parts = [translate_component(p) for p in parts[:-1]] + [OVERRIDE_TOOLS[orig_name]]
        # Apply folder-specific overrides for filenames in bsp
        if len(parts) >= 4 and parts[0:3] == BSP_CN:
            orig_name = parts[-1]
            if orig_name in OVERRIDE_BSP:
                eng_parts = [translate_component(p) for p in parts[:-1]] + [OVERRIDE_BSP[orig_name]]
        # Apply folder-specific overrides for filenames in Hardware/Sub-board
        if len(parts) >= 4 and parts[0:3] == SUBBOARD_CN:
            orig_name = parts[-1]
            if orig_name in OVERRIDE_SUBBOARD:
                eng_parts = [translate_component(p) for p in parts[:-1]] + [OVERRIDE_SUBBOARD[orig_name]]
        # Apply folder-specific overrides for filenames in Hardware/Chip
        if len(parts) >= 4 and parts[0:3] == CHIP_CN:
            orig_name = parts[-1]
            if orig_name in OVERRIDE_CHIP:
                eng_parts = [translate_component(p) for p in parts[:-1]] + [OVERRIDE_CHIP[orig_name]]
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

