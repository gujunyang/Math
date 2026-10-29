#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ml-math-tutor 自检脚本（R22，通用版）。

用法（在 Math 仓库根或 ml-math-tutor 内均可）：
    python -X utf8 系统/工具/自检.py

校验项（课程无关）：
  1. progress.json / habits.jsonl 合法性
  2. 概念登记表 ↔ progress.json 一致（id / 优先级 / 状态 / 顺序）
  3. 板书索引 / 概念笔记索引 指向的文件存在
  4. 会话 ID 合法、唯一、不超过计数器；current_session_id 允许为 null
  5. SKILL.md 与 skill_metadata.yaml 版本号一致
  6. 受保护文件存在
  7. 作业索引里的 PDF 路径存在
  8. 复习队列里的 concept id 在登记表中；日期可解析
  9. 活跃 学习内容/** 不出现旧课关键词
 10. 新课配置文件存在
 11. 课表课号不重复；若课程信息声明总课数，则行数一致
 12. git 未跟踪关键文件提醒（通用版）
 13. 冷存储：活跃 学习内容/** 不链接 _archive/；progress 只在 legacy 中保留归档路径
 14. 归档隔离：_archive/ 不进入板书索引、概念笔记索引、复习队列、作业索引

退出码：0 = 全绿；1 = 有错。
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ROOT = .../ml-math-tutor
REPO_ROOT = os.path.dirname(ROOT)

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


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


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


reg = []
if progress is not None and os.path.exists(reg_path):
    reg = parse_registry(reg_path)
    concepts = progress.get("concepts", [])
    if not isinstance(concepts, list):
        err("progress.json 的 concepts 不是列表")
        concepts = []
    pid = [c.get("id") for c in concepts if isinstance(c, dict)]
    rid = [r["id"] for r in reg]
    if set(pid) != set(rid):
        err(
            "概念集合不一致: 仅登记表=%s；仅progress=%s"
            % (sorted(set(rid) - set(pid)), sorted(set(pid) - set(rid)))
        )
    if pid != rid:
        warn("概念顺序不一致（登记表 vs progress）")
    pcmap = {c.get("id"): c for c in concepts if isinstance(c, dict)}
    for r in reg:
        c = pcmap.get(r["id"])
        if not c:
            continue
        if c.get("priority") != r["priority"]:
            err(
                "优先级不一致 %s: 登记表=%s progress=%s"
                % (r["id"], r["priority"], c.get("priority"))
            )
        if c.get("status") != r["status"]:
            err(
                "状态不一致 %s: 登记表=%s progress=%s"
                % (r["id"], r["status"], c.get("status"))
            )


# ---- 3. 索引指向存在 ------------------------------------------------------
def check_board_index():
    idx = p("学习内容", "10_板书", "00_索引.md")
    if not os.path.exists(idx):
        warn("板书索引不存在")
        return
    for line in read_text(idx).splitlines():
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
    txt = read_text(idx)
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


# ---- 4. 会话 ID -----------------------------------------------------------
if progress is not None:
    counter = progress.get("session_counter")
    cur = progress.get("current_session_id")
    idx = progress.get("session_index", [])
    if not isinstance(idx, list):
        err("session_index 不是列表")
        idx = []
    ids = [s.get("id") for s in idx if isinstance(s, dict)]
    if not isinstance(counter, int):
        err("session_counter 缺失或不是整数")
        counter = -1
    if len(ids) != len(set(ids)):
        err("session_index 存在重复会话ID")
    for sid in ids:
        m = re.match(r"S(\d{3})$", sid or "")
        if not m:
            err(f"会话ID 格式非法: {sid}")
        elif int(m.group(1)) > counter:
            err(f"会话ID {sid} 超过 session_counter={counter}")
    if cur in (None, ""):
        if any(s.get("status") == "进行中" for s in idx if isinstance(s, dict)):
            err("current_session_id 为空，但 session_index 中存在“进行中”会话")
    else:
        m = re.match(r"S(\d{3})$", cur)
        if not m:
            err(f"current_session_id 格式非法: {cur}")
        elif cur not in ids:
            err(f"current_session_id={cur} 不在 session_index 中")
        else:
            item = next(s for s in idx if s.get("id") == cur)
            if item.get("status") != "进行中":
                err(f"current_session_id={cur} 状态不是“进行中”: {item.get('status')}")
            if int(m.group(1)) != counter:
                warn(f"current_session_id={cur} 与 session_counter={counter} 不一致")


# ---- 5. 版本号一致 --------------------------------------------------------
skill_md = p("系统", "09_辅导老师", "SKILL.md")
meta = p("系统", "09_辅导老师", "skill_metadata.yaml")


def read_version(path):
    m = re.search(r"^version:\s*(\S+)", read_text(path), re.MULTILINE)
    return m.group(1) if m else None


if os.path.exists(skill_md) and os.path.exists(meta):
    v1 = read_version(skill_md)
    v2 = read_version(meta)
    if v1 and v2 and v1 != v2:
        err(f"版本号不一致: SKILL.md={v1} skill_metadata.yaml={v2}")


# ---- 6. 受保护文件存在 ----------------------------------------------------
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


# ---- 7. 作业索引 PDF 路径存在 ---------------------------------------------
hw_idx = p("学习内容", "07_学校作业", "学校作业索引.md")
if os.path.exists(hw_idx):
    for m in re.finditer(r"`([^`]+\.pdf)`", read_text(hw_idx)):
        relp = m.group(1)
        if not os.path.exists(os.path.join(REPO_ROOT, relp)):
            err(f"作业索引 PDF 路径不存在: {relp}")


# ---- 8. 复习队列 concept id / 日期 ----------------------------------------
def check_date(s, where):
    try:
        datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        err(f"{where} 日期无法解析: {s}")


if progress is not None:
    rq = progress.get("review_queue", [])
    if not isinstance(rq, list):
        err("progress.json 的 review_queue 不是列表")
        rq = []
    rid_set = {r["id"] for r in reg}
    for item in rq:
        if not isinstance(item, dict):
            continue
        if "concept" in item:
            cid = item.get("concept")
            if cid not in rid_set:
                err(f"review_queue 的 concept id 不在登记表: {cid}")
            if item.get("next_review"):
                check_date(item["next_review"], f"review_queue({cid})")
        if item.get("date"):
            check_date(item["date"], "review_queue(date)")

# 人读复习队列表：| concept | ... | next |
rq_md = p("系统", "05_学习进度", "复习队列.md")
if os.path.exists(rq_md):
    for line in read_text(rq_md).splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.match(r"^[a-z][a-z_]+$", cells[0]):
            if cells[0] not in {r["id"] for r in reg}:
                err(f"复习队列.md 的 concept id 不在登记表: {cells[0]}")
            if re.match(r"^\d{4}-\d{2}-\d{2}$", cells[2]):
                check_date(cells[2], f"复习队列.md({cells[0]})")


# ---- 9. 活跃学习内容不出现旧课关键词 --------------------------------------
OLD_KEYWORDS = [
    "AISC5000",
    "2026-10-29",
    "30 课冲刺",
    "30课冲刺",
    "压缩10课",
    "压缩 10 课",
    "期中冲刺",
]
content_root = p("学习内容")
if os.path.isdir(content_root):
    for base, dirs, files in os.walk(content_root):
        dirs[:] = [d for d in dirs if d not in ("_archive", ".git", "__pycache__")]
        for fn in files:
            if not fn.endswith((".md", ".json", ".yaml", ".yml", ".txt")):
                continue
            fp = os.path.join(base, fn)
            try:
                txt = read_text(fp)
            except (UnicodeDecodeError, OSError):
                continue
            for kw in OLD_KEYWORDS:
                if kw in txt:
                    err(f"活跃学习内容出现旧课关键词「{kw}」: {rel(fp)}")


# ---- 10. 新课配置文件存在 -------------------------------------------------
CONFIG_FILES = [
    ("学习内容", "01_学习计划", "课程信息.md"),
    ("学习内容", "01_学习计划", "学习路线.md"),
    ("学习内容", "01_学习计划", "概念登记表.md"),
    ("学习内容", "01_学习计划", "概念优先级.md"),
    ("学习内容", "01_学习计划", "第01–NN课_课表.md"),
    ("学习内容", "02_知识图谱", "知识图谱.md"),
    ("学习内容", "07_学校作业", "学校作业索引.md"),
    ("学习内容", "10_板书", "00_索引.md"),
]
for parts in CONFIG_FILES:
    if not os.path.exists(p(*parts)):
        err("新课配置文件缺失: " + "/".join(parts))


# ---- 11. 课表行数 / 课号 --------------------------------------------------
course_info = p("学习内容", "01_学习计划", "课程信息.md")
course_tbl = p("学习内容", "01_学习计划", "第01–NN课_课表.md")
declared_total = None
if os.path.exists(course_info):
    for line in read_text(course_info).splitlines():
        m = re.match(r"\|\s*总课数\s*\|\s*(\d+)\s*\|", line)
        if m:
            declared_total = int(m.group(1))
            break
        m = re.search(r"总课数\s*[：:]\s*(\d+)", line)
        if m:
            declared_total = int(m.group(1))
            break
if os.path.exists(course_tbl):
    lesson_ids = []
    for line in read_text(course_tbl).splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        m = re.match(r"^(?:第\s*)?(\d{1,3})(?:\s*课)?$", cells[0])
        if m:
            lesson_ids.append(int(m.group(1)))
    if len(lesson_ids) != len(set(lesson_ids)):
        err("课表存在重复课号")
    if declared_total is not None and len(lesson_ids) != declared_total:
        err(f"课表行数({len(lesson_ids)}) 与课程信息声明总课数({declared_total}) 不一致")


# ---- 12. git 未跟踪关键文件提醒（通用） -----------------------------------
try:
    out = subprocess.run(
        ["git", "-c", "core.quotepath=false", "-C", REPO_ROOT, "status", "--porcelain"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
    )
    for line in out.stdout.splitlines():
        if not line.startswith("?? "):
            continue
        path = line[3:].strip().strip('"')
        if path.startswith(("ml-math-tutor/学习内容/", "ml-math-tutor/系统/09_辅导老师/")):
            warn("关键文件尚未纳入 git: " + path)
except Exception:
    pass


# ---- 13. 冷存储：活跃内容不链接归档 --------------------------------------
if os.path.isdir(content_root):
    for base, dirs, files in os.walk(content_root):
        dirs[:] = [d for d in dirs if d not in ("_archive", ".git", "__pycache__")]
        for fn in files:
            if not fn.endswith((".md", ".json", ".yaml", ".yml", ".txt")):
                continue
            fp = os.path.join(base, fn)
            try:
                txt = read_text(fp)
            except (UnicodeDecodeError, OSError):
                continue
            if "_archive/" in txt:
                err(f"活跃学习内容链接了归档目录: {rel(fp)}")

if progress is not None:
    def walk_archive_paths(obj, path=()):
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from walk_archive_paths(v, path + (k,))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from walk_archive_paths(v, path + (i,))
        elif isinstance(obj, str) and "_archive/" in obj:
            yield path

    for path in walk_archive_paths(progress):
        if not path or path[0] != "legacy":
            err("progress.json 在 legacy 之外出现归档路径: " + "/".join(map(str, path)))

# .ignore 必须排除 _archive/
ignore_path = os.path.join(REPO_ROOT, ".ignore")
if os.path.exists(ignore_path):
    if "_archive/" not in read_text(ignore_path):
        err(".ignore 未包含 _archive/（日常检索会命中归档）")
else:
    warn(".ignore 不存在（建议加入 _archive/）")


# ---- 14. 归档隔离：索引/复习/作业不出现 _archive --------------------------
for label, path in [
    ("板书索引", p("学习内容", "10_板书", "00_索引.md")),
    ("概念笔记索引", p("学习内容", "03_概念笔记", "00_索引.md")),
    ("复习队列", p("系统", "05_学习进度", "复习队列.md")),
    ("作业索引", p("学习内容", "07_学校作业", "学校作业索引.md")),
]:
    if os.path.exists(path) and "_archive/" in read_text(path):
        err(f"{label} 出现了归档路径（归档必须隔离）: {rel(path)}")


# ---- 输出 -----------------------------------------------------------------
print("=== ml-math-tutor 自检（通用版）===")
if progress is not None:
    status = (progress.get("course") or {}).get("status", "未声明")
    print(f"课程状态: {status}")
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
