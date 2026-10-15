#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ml-math-tutor 自检脚本（R22）。

用法（在 Math 仓库根或 ml-math-tutor 内均可）：
    python3 系统/工具/自检.py

校验项：
  1. progress.json / habits.jsonl 合法性
  2. 概念登记表 ↔ progress.json 一致（id / 优先级 / 状态 / 顺序）
  3. 无残留旧路径（重构前的 0X_ / 1X_ 顶层路径）
  4. 板书索引 / 概念笔记索引 指向的文件确实存在
  5. 会话ID 单调、唯一，current_session_id 合法
  6. 版本号一致（SKILL.md ↔ skill_metadata.yaml）
  7. 受保护文件存在

退出码：0 = 全绿；1 = 有错。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ROOT = .../ml-math-tutor

errors = []
warns = []


def p(*parts):
    return os.path.join(ROOT, *parts)


def err(msg):
    errors.append(msg)


def warn(msg):
    warns.append(msg)


def rel(path):
    return os.path.relpath(path, ROOT)


# ---- 1. JSON / JSONL -------------------------------------------------------
progress_path = p("系统", "05_学习进度", "progress.json")
reg_path = p("学习内容", "01_学习计划", "概念登记表.md")
habits_path = p("系统", "06_学习习惯", "habits.jsonl")

progress = None
try:
    with open(progress_path, encoding="utf-8") as f:
        progress = json.load(f)
except Exception as e:
    err(f"progress.json 无法解析: {e}")

if os.path.exists(habits_path):
    with open(habits_path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                try:
                    json.loads(line)
                except Exception as e:
                    err(f"habits.jsonl 第 {i} 行非法 JSON: {e}")
else:
    warn("habits.jsonl 不存在（可接受，首次运行）")


# ---- 2. 登记表 ↔ progress ------------------------------------------------
def parse_registry(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(
                r"\|\s*([a-z_]+)\s*\|\s*([^|]+?)\s*\|\s*(必学|掌握|了解)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|",
                line,
            )
            if m:
                rows.append(
                    {
                        "id": m.group(1),
                        "name": m.group(2),
                        "priority": m.group(3),
                        "status": m.group(5).strip(),
                    }
                )
    return rows


if progress is not None and os.path.exists(reg_path):
    reg = parse_registry(reg_path)
    pid = [c["id"] for c in progress.get("concepts", [])]
    rid = [r["id"] for r in reg]
    if set(pid) != set(rid):
        err(
            "概念集合不一致: 仅登记表=%s；仅progress=%s"
            % (sorted(set(rid) - set(pid)), sorted(set(pid) - set(rid)))
        )
    if pid != rid:
        warn("概念顺序不一致（登记表 vs progress）")
    pcmap = {c["id"]: c for c in progress.get("concepts", [])}
    for r in reg:
        c = pcmap.get(r["id"])
        if not c:
            continue
        if c.get("priority") != r["priority"]:
            err(
                "优先级不一致 %s: 登记表=%s progress=%s"
                % (r["id"], r["priority"], c.get("priority"))
            )
        # 状态：progress 允许更细（学习中），登记表须与 progress 相同
        if c.get("status") != r["status"]:
            err(
                "状态不一致 %s: 登记表=%s progress=%s"
                % (r["id"], r["status"], c.get("status"))
            )


# ---- 3. 残留旧路径 --------------------------------------------------------
FORBIDDEN = [
    re.compile(r"ml-math-tutor/0[0-9]_"),
    re.compile(r"ml-math-tutor/1[01]_"),
]
SCAN_EXT = (".md", ".yaml", ".yml", ".json")
for base, dirs, files in os.walk(ROOT):
    if ".git" in dirs:
        dirs.remove(".git")
    for fn in files:
        if not fn.endswith(SCAN_EXT):
            continue
        fp = os.path.join(base, fn)
        try:
            with open(fp, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    for pat in FORBIDDEN:
                        if pat.search(line):
                            err(f"残留旧路径 {rel(fp)}:{i}: {line.strip()[:80]}")
        except (UnicodeDecodeError, OSError):
            pass


# ---- 4. 索引指向存在 ------------------------------------------------------
def check_board_index():
    idx = p("学习内容", "10_板书", "00_索引.md")
    if not os.path.exists(idx):
        warn("板书索引不存在")
        return
    with open(idx, encoding="utf-8") as f:
        for line in f:
            m = re.search(r"`([^`]+\.md)`", line)
            if m and re.match(r"^S\d+_", m.group(1)):
                target = p("学习内容", "10_板书", m.group(1))
                if not os.path.exists(target):
                    err(f"板书索引指向的文件不存在: {m.group(1)}")


def check_concept_index():
    idx = p("学习内容", "03_概念笔记", "00_索引.md")
    if not os.path.exists(idx):
        warn("概念笔记索引不存在")
        return
    with open(idx, encoding="utf-8") as f:
        txt = f.read()
    # 只校验"已创建："那一行里列出的 id
    for m in re.finditer(r"已创建：([^\n]+)", txt):
        for cid in re.findall(r"[a-z][a-z_]+", m.group(1)):
            found = any(
                os.path.exists(p("学习内容", "03_概念笔记", lvl, cid + ".md"))
                for lvl in ("必学", "掌握", "了解")
            )
            if not found:
                err(f"概念笔记索引声称已创建但文件不存在: {cid}")


check_board_index()
check_concept_index()


# ---- 5. 会话ID ------------------------------------------------------------
if progress is not None:
    counter = progress.get("session_counter")
    cur = progress.get("current_session_id")
    idx = progress.get("session_index", [])
    ids = [s.get("id") for s in idx]
    if len(ids) != len(set(ids)):
        err("session_index 存在重复会话ID")
    if cur not in ids:
        err(f"current_session_id={cur} 不在 session_index 中")
    else:
        item = next(s for s in idx if s.get("id") == cur)
        if item.get("status") != "进行中":
            warn(f"当前会话 {cur} 状态非'进行中': {item.get('status')}")
    for sid in ids:
        m = re.match(r"S(\d+)$", sid or "")
        if not m:
            err(f"会话ID 格式非法: {sid}")
        elif int(m.group(1)) > counter:
            err(f"会话ID {sid} 超过 session_counter={counter}")
    if cur and cur not in ("", None):
        m = re.match(r"S(\d+)$", cur)
        if m and int(m.group(1)) != counter:
            warn(f"current_session_id={cur} 与 session_counter={counter} 不一致")


# ---- 6. 版本号一致 --------------------------------------------------------
skill_md = p("系统", "09_辅导老师", "SKILL.md")
meta = p("系统", "09_辅导老师", "skill_metadata.yaml")


def read_frontmatter_version(path):
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r"^version:\s*(\S+)", txt, re.MULTILINE)
    return m.group(1) if m else None


if os.path.exists(skill_md) and os.path.exists(meta):
    v1 = read_frontmatter_version(skill_md)
    v2 = read_frontmatter_version(meta)
    if v1 and v2 and v1 != v2:
        err(f"版本号不一致: SKILL.md={v1} skill_metadata.yaml={v2}")


# ---- 7. 受保护文件存在 ----------------------------------------------------
PROTECTED = [
    ("系统", "09_辅导老师", "SKILL.md"),
    ("系统", "09_辅导老师", "startup_protocol.md"),
    ("系统", "09_辅导老师", "rules.md"),
    ("系统", "09_辅导老师", "skill_metadata.yaml"),
    ("系统", "05_学习进度", "progress.json"),
    ("学习内容", "01_学习计划", "概念登记表.md"),
    ("系统", "05_学习进度", "系统变更记录.md"),
]
for parts in PROTECTED:
    if not os.path.exists(p(*parts)):
        err("受保护文件缺失: " + "/".join(parts))


# ---- 输出 -----------------------------------------------------------------
print("=== ml-math-tutor 自检 ===")
if warns:
    print("\n[警告]")
    for w in warns:
        print("  ! " + w)
if errors:
    print("\n[错误]")
    for e in errors:
        print("  x " + e)
    print(f"\n结果: 失败（{len(errors)} 个错误，{len(warns)} 个警告）")
    sys.exit(1)
print(f"\n结果: 通过（0 个错误，{len(warns)} 个警告）")
