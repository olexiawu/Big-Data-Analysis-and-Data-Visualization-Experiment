#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把国家统计局导出的原始季度数据（宽表）转换为驾驶舱可直接使用的数据文件。

输入: data/raw/quarterly_raw.csv   （国家统计局"季度数据"原始导出，UTF-8 BOM）
输出: data/gdp_quarterly.csv       （整洁长表，Excel 友好）
      data/gdp_quarterly.json      （结构化数据，便于二次开发）
      assets/js/data.js            （前端直接引用的数据脚本）

用法: python tools/prepare_data.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "quarterly_raw.csv"
OUT_CSV = ROOT / "data" / "gdp_quarterly.csv"
OUT_JSON = ROOT / "data" / "gdp_quarterly.json"
OUT_JS = ROOT / "assets" / "js" / "data.js"

CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4}

# 指标 -> (key, 简称, 层级)
META = {
    "国内生产总值": ("gdp", "GDP", "total"),
    "第一产业": ("primary", "第一产业", "sector"),
    "第二产业": ("secondary", "第二产业", "sector"),
    "第三产业": ("tertiary", "第三产业", "sector"),
    "农林牧渔业": ("agriculture", "农林牧渔", "industry"),
    "工业": ("industry", "工业", "industry"),
    "制造业": ("manufacturing", "制造业", "industry"),
    "建筑业": ("construction", "建筑业", "industry"),
    "批发和零售业": ("wholesale", "批发零售", "industry"),
    "交通运输、仓储和邮政业": ("transport", "交通运输", "industry"),
    "住宿和餐饮业": ("catering", "住宿餐饮", "industry"),
    "金融业": ("finance", "金融业", "industry"),
    "房地产业": ("realestate", "房地产业", "industry"),
    "信息传输、软件和信息技术服务业": ("infotech", "信息软件", "industry"),
    "租赁和商务服务业": ("leasing", "租赁商务", "industry"),
    "其他行业": ("other", "其他行业", "industry"),
}

LABEL_RE = re.compile(r"^(?P<name>.+?)(?:增加值)?(?P<kind>当季值|累计值)\s*\(亿元\)$")


def parse_quarters(header: str) -> list[str]:
    quarters = []
    for year, cn in re.findall(r"(\d{4})年第([一二三四])季度", header):
        quarters.append(f"{year}Q{CN_NUM[cn]}")
    return quarters  # 原始文件为“最新季度在前”


def parse_rows(text: str) -> tuple[list[str], list[tuple[str, dict[str, float]]]]:
    quarters: list[str] = []
    records: list[tuple[str, dict[str, float]]] = []

    for line in text.splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        if line.lstrip("\ufeff").startswith("指标"):
            quarters = parse_quarters(line)
            continue
        if not quarters:
            continue
        if re.match(r"^(注[:：]|数据来源|数据库[:：]|时间[:：])", line.strip()):
            break

        parts = [p.strip() for p in line.split(",")]
        label = parts[0].strip()
        values = [p for p in parts[1:] if p]
        match = LABEL_RE.match(label)
        if not match or len(values) != len(quarters):
            break

        name = match.group("name").strip()
        kind = match.group("kind")
        if name not in META:
            raise SystemExit(f"未知指标: {name}")
        nums = {q: float(v) for q, v in zip(quarters, values)}
        records.append((name, {"kind": kind, "values": nums}))
    return quarters, records


def main() -> None:
    text = RAW.read_text(encoding="utf-8")
    quarters_newest_first, records = parse_rows(text)
    if not quarters_newest_first:
        raise SystemExit("未能解析季度表头，请检查原始文件格式")
    quarters = list(reversed(quarters_newest_first))

    indicators: dict[str, dict] = {}
    for name, rec in records:
        key, short, level = META[name]
        item = indicators.setdefault(
            key,
            {"key": key, "name": name, "short": short, "level": level, "q": [], "cum": []},
        )
        item["q" if rec["kind"] == "当季值" else "cum"] = [
            rec["values"][q] for q in quarters
        ]

    ordered = sorted(indicators.values(), key=lambda d: list(META).index(d["name"]))

    # 一致性自检：三次产业当季值之和应等于 GDP 当季值（四舍五入到 0.1 亿元）
    gdp = indicators["gdp"]["q"]
    for i, q in enumerate(quarters):
        total = sum(indicators[k]["q"][i] for k in ("primary", "secondary", "tertiary"))
        if abs(total - gdp[i]) > 0.6:
            raise SystemExit(f"{q} 三次产业合计 {total} 与 GDP {gdp[i]} 不一致")

    payload = {
        "meta": {
            "source": "国家统计局",
            "title": "国民经济核算 · 季度数据",
            "unit": "亿元",
            "price": "按当年价格计算",
            "updated": "2026-11-12",
            "range": f"{quarters[0]} — {quarters[-1]}",
        },
        "quarters": quarters,
        "indicators": ordered,
    }

    # 1) 整洁长表
    lines = ["季度,指标,类型,数值(亿元)"]
    for item in ordered:
        for i, q in enumerate(quarters):
            lines.append(f"{q},{item['name']},当季值,{item['q'][i]:.1f}")
            lines.append(f"{q},{item['name']},累计值,{item['cum'][i]:.1f}")
    OUT_CSV.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8-sig", newline="")

    # 2) JSON
    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    # 3) 前端数据脚本
    OUT_JS.write_text(
        "/* 本文件由 tools/prepare_data.py 自动生成，请勿手工修改。 */\n"
        "window.GDP_DATA = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"OK  quarters={len(quarters)}  indicators={len(ordered)}")
    print(f"    {quarters[0]} ~ {quarters[-1]}  GDP当季最新={gdp[-1]:,.1f} 亿元")


if __name__ == "__main__":
    main()
