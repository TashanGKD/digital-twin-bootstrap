"""从画像 Markdown 中提取结构化数据"""
import re


def _extract_section(md: str, heading: str) -> str:
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)"
    m = re.search(pattern, md, re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_field(text: str, label: str) -> str:
    pattern = rf"\*\*{re.escape(label)}\*\*[：:]\s*(.*?)(?:\n|$)"
    m = re.search(pattern, text)
    if not m:
        return ""
    val = m.group(1).strip()
    if val.startswith("<!--") or not val:
        return ""
    return val


def _extract_table_rows(text: str) -> list[dict]:
    rows = []
    lines = text.split("\n")
    headers: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if not headers:
            headers = cells
            continue
        row = {}
        for i, h in enumerate(headers):
            row[h] = cells[i] if i < len(cells) else ""
        rows.append(row)
    return rows


def _extract_number(text: str) -> float | None:
    m = re.search(r"[-+]?\d+\.?\d*", text)
    return float(m.group()) if m else None


def _is_filled(val) -> bool:
    if val is None:
        return False
    if isinstance(val, str):
        return bool(val.strip()) and not val.strip().startswith("<!--")
    if isinstance(val, (int, float)):
        return True
    if isinstance(val, dict):
        return any(_is_filled(v) for v in val.values())
    if isinstance(val, list):
        return len(val) > 0
    return bool(val)


def parse_profile(md: str) -> dict:
    result: dict = {
        "name": "",
        "meta": {"created_at": "", "updated_at": "", "stage": "", "source": ""},
        "identity": {},
        "capability": {"tech_stack": [], "process": {}, "outputs": ""},
        "needs": {"time_occupation": [], "pain_points": [], "want_to_change": ""},
        "cognitive_style": {},
        "motivation": {"dimensions": {}, "intrinsic_total": None, "extrinsic_total": None, "rai": None, "source": ""},
        "personality": {},
        "interpretation": {"core_driver": "", "risks": "", "path": ""},
        "completion": {},
    }

    title_m = re.search(r"^#\s+科研人员画像\s*[—–-]\s*(.+)", md, re.MULTILINE)
    if title_m:
        name = title_m.group(1).strip()
        if name and name not in ("[姓名/标识]", "姓名/标识"):
            result["name"] = name

    meta = _extract_section(md, "元信息")
    if meta:
        result["meta"]["created_at"] = _extract_field(meta, "创建时间")
        result["meta"]["updated_at"] = _extract_field(meta, "最后更新")
        result["meta"]["stage"] = _extract_field(meta, "采集阶段")
        result["meta"]["source"] = _extract_field(meta, "数据来源")

    identity_sec = _extract_section(md, "一、基础身份")
    if identity_sec:
        result["identity"] = {
            "research_stage": _extract_field(identity_sec, "研究阶段"),
            "primary_field": _extract_field(identity_sec, "一级领域"),
            "secondary_field": _extract_field(identity_sec, "二级领域"),
            "cross_field": _extract_field(identity_sec, "交叉方向"),
            "method": _extract_field(identity_sec, "方法范式"),
            "institution": _extract_field(identity_sec, "所在机构"),
            "network": _extract_field(identity_sec, "学术网络"),
        }

    cap_sec = _extract_section(md, "二、能力")
    if cap_sec:
        tech_m = re.search(r"###\s+2\.1\s+技术能力\s*\n(.*?)(?=###|\Z)", cap_sec, re.DOTALL)
        if tech_m:
            rows = _extract_table_rows(tech_m.group(1))
            tech_stack = []
            for row in rows:
                cat = row.get("类别", "")
                tech = row.get("具体技术", "")
                level = row.get("熟练程度（★☆）", row.get("熟练程度", ""))
                if tech:
                    tech_stack.append({"category": cat, "tech": tech, "level": level})
            result["capability"]["tech_stack"] = tech_stack

        outputs_m = re.search(r"\*\*代表性产出\*\*[：:]\s*(.*?)(?=###|\Z)", cap_sec, re.DOTALL)
        if outputs_m:
            val = outputs_m.group(1).strip()
            if not val.startswith("<!--"):
                result["capability"]["outputs"] = val

        proc_m = re.search(r"###\s+2\.2\s+科研流程能力\s*\n(.*?)(?=---|\Z)", cap_sec, re.DOTALL)
        if proc_m:
            proc_rows = _extract_table_rows(proc_m.group(1))
            mapping = {
                "问题定义": "problem_definition",
                "文献整合": "literature",
                "方案设计": "design",
                "实验执行": "execution",
                "论文写作": "writing",
                "项目管理": "management",
            }
            for row in proc_rows:
                label = row.get("环节", "").strip()
                score_str = row.get("评分", "").strip()
                desc = row.get("简要说明", "").strip()
                key = mapping.get(label)
                if key and score_str:
                    num = _extract_number(score_str)
                    result["capability"]["process"][key] = {
                        "score": num,
                        "description": desc if desc and not desc.startswith("<!--") else "",
                    }

    needs_sec = _extract_section(md, "三、当前需求")
    if needs_sec:
        occ_m = re.search(r"###\s+3\.1\s+主要时间占用\s*\n(.*?)(?=###|\Z)", needs_sec, re.DOTALL)
        if occ_m:
            rows = _extract_table_rows(occ_m.group(1))
            items = [{"item": r.get("事项", ""), "desc": r.get("描述", ""), "feeling": r.get("感受", "")} for r in rows if r.get("事项")]
            result["needs"]["time_occupation"] = items

        pain_m = re.search(r"###\s+3\.2\s+核心难点与卡点\s*\n(.*?)(?=###|\Z)", needs_sec, re.DOTALL)
        if pain_m:
            rows = _extract_table_rows(pain_m.group(1))
            items = [{"issue": r.get("难点", ""), "detail": r.get("具体表现", ""), "help_type": r.get("期望获得的帮助类型", "")} for r in rows if r.get("难点")]
            result["needs"]["pain_points"] = items

        change_m = re.search(r"###\s+3\.3\s+近期最想改变的一件事\s*\n(.*?)(?=---|\Z)", needs_sec, re.DOTALL)
        if change_m:
            val = change_m.group(1).strip()
            if not val.startswith("<!--"):
                result["needs"]["want_to_change"] = val

    cog_sec = _extract_section(md, "四、认知风格（RCSS）")
    if cog_sec:
        source_m = re.search(r"数据来源[：:]\s*`?([^`\n]+)`?", cog_sec)
        cog_source = source_m.group(1).strip() if source_m else ""

        summary_rows = _extract_table_rows(cog_sec)
        cog_data: dict = {"source": cog_source}
        for row in summary_rows:
            indicator = row.get("指标", "")
            score_str = row.get("得分", row.get("", ""))
            num = _extract_number(score_str) if score_str else None
            if "横向整合分" in indicator and num is not None:
                cog_data["integration"] = num
            elif "垂直深度分" in indicator and num is not None:
                cog_data["depth"] = num
            elif "认知风格指数" in indicator and num is not None:
                cog_data["csi"] = num
            elif "认知风格类型" in indicator:
                cog_data["type"] = score_str.strip() if score_str else ""
        result["cognitive_style"] = cog_data

    mot_sec = _extract_section(md, "五、学术动机（AMS-GSR 28）")
    if mot_sec:
        source_m = re.search(r"数据来源[：:]\s*`?([^`\n]+)`?", mot_sec)
        result["motivation"]["source"] = source_m.group(1).strip() if source_m else ""

        dim_mapping = {
            "求知内在动机": "know",
            "成就内在动机": "accomplishment",
            "体验刺激内在动机": "stimulation",
            "认同调节": "identified",
            "内摄调节": "introjected",
            "外部调节": "external",
            "无动机": "amotivation",
        }
        dim_rows = _extract_table_rows(mot_sec)
        for row in dim_rows:
            label = row.get("维度", row.get("指标", "")).strip()
            score_str = row.get("平均分（1–7）", row.get("数值", row.get("得分", ""))).strip()
            num = _extract_number(score_str) if score_str else None
            key = dim_mapping.get(label)
            if key and num is not None:
                result["motivation"]["dimensions"][key] = num
            elif "内在动机总分" in label and num is not None:
                result["motivation"]["intrinsic_total"] = num
            elif "外在动机总分" in label and num is not None:
                result["motivation"]["extrinsic_total"] = num
            elif "自主动机指数" in label and num is not None:
                result["motivation"]["rai"] = num

    per_sec = _extract_section(md, "六、人格（Mini-IPIP）")
    if per_sec:
        source_m = re.search(r"数据来源[：:]\s*`?([^`\n]+)`?", per_sec)
        per_source = source_m.group(1).strip() if source_m else ""

        per_mapping = {
            "外向性": "extraversion",
            "宜人性": "agreeableness",
            "尽责性": "conscientiousness",
            "神经质": "neuroticism",
            "开放性/智力": "openness",
        }
        per_rows = _extract_table_rows(per_sec)
        per_data: dict = {"source": per_source}
        for row in per_rows:
            label = row.get("维度", "").strip()
            for zh, en in per_mapping.items():
                if zh in label:
                    score_str = row.get("平均分（1–5）", "").strip()
                    num = _extract_number(score_str) if score_str else None
                    desc = row.get("水平描述", "").strip()
                    if num is not None:
                        per_data[en] = {"score": num, "level": desc}
                    break
        result["personality"] = per_data

    interp_sec = _extract_section(md, "七、综合解读")
    if interp_sec:
        driver_m = re.search(r"###\s+核心驱动模式\s*\n(.*?)(?=###|\Z)", interp_sec, re.DOTALL)
        risks_m = re.search(r"###\s+潜在风险与发展建议\s*\n(.*?)(?=###|\Z)", interp_sec, re.DOTALL)
        path_m = re.search(r"###\s+适合的发展路径\s*\n(.*?)(?=---|\Z)", interp_sec, re.DOTALL)
        result["interpretation"]["core_driver"] = driver_m.group(1).strip() if driver_m else ""
        result["interpretation"]["risks"] = risks_m.group(1).strip() if risks_m else ""
        result["interpretation"]["path"] = path_m.group(1).strip() if path_m else ""

    result["completion"] = {
        "identity": _is_filled(result["identity"]),
        "capability": _is_filled(result["capability"]["process"]),
        "needs": _is_filled(result["needs"]["time_occupation"]) or _is_filled(result["needs"]["want_to_change"]),
        "cognitive_style": _is_filled(result["cognitive_style"].get("csi")),
        "motivation": _is_filled(result["motivation"]["dimensions"]),
        "personality": any(k != "source" and _is_filled(v) for k, v in result["personality"].items()),
        "interpretation": _is_filled(result["interpretation"]["core_driver"]),
    }

    return result
