"""LLM Agent 循环：后端工具 + UI 工具（Block 协议）"""
import json
from datetime import date

from config import LLM_API_KEY
from llm_client import create_client, get_model
from prompts import META_SYSTEM_PROMPT
from sessions import save_forum_profile, save_profile
from tools import read_skill, read_doc, SKILL_NAMES, DOC_NAMES

# ── 后端工具定义（执行后结果喂回 LLM）──────────────────────────────

BACKEND_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": "读取指定 Skill 文件，获取具体任务的操作指南。",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "enum": SKILL_NAMES,
                        "description": "Skill 名称",
                    }
                },
                "required": ["skill_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_doc",
            "description": "读取参考文档（量表原题等）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "enum": DOC_NAMES,
                        "description": "文档名称",
                    }
                },
                "required": ["doc_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_profile",
            "description": "获取当前会话中的科研数字分身内容。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_profile",
            "description": "将科研数字分身内容写入会话并保存。每获得一轮信息后都应立即调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "完整的科研数字分身 Markdown 内容",
                    }
                },
                "required": ["content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_forum_profile",
            "description": "将他山论坛分身写入会话并保存。",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "完整的他山论坛分身 Markdown",
                    }
                },
                "required": ["content"],
            },
        },
    },
]

# ── UI 工具定义（收集为 Block 发送给前端）─────────────────────────

UI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ask_choice",
            "description": "向用户展示一个单选题。前端会渲染为可点击的按钮组。每次只能问一个问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "问题文本"},
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "label": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "required": ["id", "label"],
                        },
                        "description": "选项列表",
                    },
                },
                "required": ["question", "options"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_text",
            "description": "向用户提一个开放式问题。前端会渲染为输入框。每次只能问一个问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "问题文本"},
                    "placeholder": {"type": "string", "description": "输入框提示文字"},
                    "multiline": {"type": "boolean", "description": "是否多行输入"},
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_rating",
            "description": "请用户对某项进行评分。前端渲染为评分按钮行。每次只能问一个问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "评分问题"},
                    "min_val": {"type": "integer", "description": "最小分值"},
                    "max_val": {"type": "integer", "description": "最大分值"},
                    "min_label": {"type": "string", "description": "最低分标签"},
                    "max_label": {"type": "string", "description": "最高分标签"},
                },
                "required": ["question", "min_val", "max_val"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "show_profile_chart",
            "description": "展示画像可视化图表（雷达图或柱状图）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "chart_type": {
                        "type": "string",
                        "enum": ["radar", "bar"],
                        "description": "图表类型",
                    },
                    "title": {"type": "string", "description": "图表标题"},
                    "dimensions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "维度名称列表",
                    },
                    "values": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "各维度数值",
                    },
                    "max_value": {"type": "number", "description": "最大值（用于归一化）"},
                },
                "required": ["chart_type", "title", "dimensions", "values"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "show_copyable",
            "description": "展示一段需要用户复制的固定文本（如提示词模板）。前端渲染为带「一键复制」按钮的内容框。",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "标题（可选）"},
                    "content": {"type": "string", "description": "需要用户复制的完整文本内容"},
                },
                "required": ["content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "show_actions",
            "description": "展示操作按钮，如跳转到画像页或量表测试。在完成关键步骤后使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "提示文字"},
                    "buttons": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "label": {"type": "string"},
                                "href": {"type": "string"},
                                "style": {
                                    "type": "string",
                                    "enum": ["primary", "secondary"],
                                },
                            },
                            "required": ["id", "label"],
                        },
                    },
                },
                "required": ["buttons"],
            },
        },
    },
]

ALL_TOOLS = BACKEND_TOOLS + UI_TOOLS
UI_TOOL_NAMES = {t["function"]["name"] for t in UI_TOOLS}

INTERACTIVE_UI_TOOLS = {"ask_choice", "ask_text", "ask_rating"}
DISPLAY_UI_TOOLS = {"show_copyable", "show_profile_chart", "show_actions"}


def _execute_backend_tool(name: str, args: dict, session: dict) -> str:
    if name == "read_skill":
        return read_skill(args.get("skill_name", ""))
    if name == "read_doc":
        return read_doc(args.get("doc_name", ""))
    if name == "read_profile":
        return session["profile"]
    if name == "write_profile":
        content = args.get("content", "")
        path = save_profile(session, content)
        return f"已写入科研数字分身并保存到 {path.name}，共 {len(content)} 字符。"
    if name == "write_forum_profile":
        content = args.get("content", "")
        path = save_forum_profile(session, content)
        return f"已写入他山论坛分身并保存到 {path.name}，共 {len(content)} 字符。"
    return f"未知工具: {name}"


def _ui_tool_to_block(name: str, args: dict) -> dict:
    """将 UI 工具调用转换为前端 Block"""
    if name == "ask_choice":
        return {
            "type": "choice",
            "id": args.get("question", "")[:20],
            "question": args.get("question", ""),
            "options": args.get("options", []),
        }
    if name == "ask_text":
        return {
            "type": "text_input",
            "id": args.get("question", "")[:20],
            "question": args.get("question", ""),
            "placeholder": args.get("placeholder", ""),
            "multiline": args.get("multiline", False),
        }
    if name == "ask_rating":
        return {
            "type": "rating",
            "id": args.get("question", "")[:20],
            "question": args.get("question", ""),
            "min_val": args.get("min_val", 1),
            "max_val": args.get("max_val", 5),
            "min_label": args.get("min_label", ""),
            "max_label": args.get("max_label", ""),
        }
    if name == "show_profile_chart":
        return {
            "type": "chart",
            "chart_type": args.get("chart_type", "radar"),
            "title": args.get("title", ""),
            "dimensions": args.get("dimensions", []),
            "values": args.get("values", []),
            "max_value": args.get("max_value", 5),
        }
    if name == "show_copyable":
        return {
            "type": "copyable",
            "title": args.get("title", ""),
            "content": args.get("content", ""),
        }
    if name == "show_actions":
        return {
            "type": "actions",
            "message": args.get("message", ""),
            "buttons": args.get("buttons", []),
        }
    return {"type": "text", "content": f"[未知UI工具: {name}]"}


def _format_tool_call(tc) -> dict:
    return {
        "id": tc.id,
        "type": "function",
        "function": {
            "name": tc.function.name,
            "arguments": tc.function.arguments or "{}",
        },
    }


def run_agent(
    user_message: str,
    session: dict,
    *,
    model: str | None = None,
) -> list[dict]:
    """
    运行 agent 循环。返回 Block 列表供前端渲染。
    Block 类型：text / choice / text_input / rating / chart / actions
    """
    if not LLM_API_KEY:
        return [{"type": "text", "content": "错误：未配置 API Key。"}]

    client = create_client()
    if not client:
        return [{"type": "text", "content": "错误：无法创建 LLM 客户端。"}]

    today_str = date.today().strftime("%Y-%m-%d")
    system_content = (
        META_SYSTEM_PROMPT
        + f"\n\n**当前日期**：{today_str}"
    )

    messages = session["messages"].copy()
    messages.append({"role": "user", "content": user_message})
    response_blocks: list[dict] = []

    max_iterations = 20
    for _ in range(max_iterations):
        try:
            response = client.chat.completions.create(
                model=get_model(model),
                messages=[{"role": "system", "content": system_content}] + messages,
                tools=ALL_TOOLS,
                tool_choice="auto",
            )
        except Exception as e:
            response_blocks.append({"type": "text", "content": f"LLM 调用失败: {e}"})
            break

        msg = response.choices[0].message
        tool_calls = getattr(msg, "tool_calls", None) or []

        if not tool_calls:
            if msg.content and msg.content.strip():
                response_blocks.append({"type": "text", "content": msg.content.strip()})
            break

        if msg.content and msg.content.strip():
            response_blocks.append({"type": "text", "content": msg.content.strip()})

        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [_format_tool_call(tc) for tc in tool_calls],
            }
        )

        has_interactive_ui = False
        for tc in tool_calls:
            try:
                args = json.loads(tc.function.arguments) if tc.function.arguments else {}
            except json.JSONDecodeError:
                args = {}

            if tc.function.name in INTERACTIVE_UI_TOOLS:
                block = _ui_tool_to_block(tc.function.name, args)
                response_blocks.append(block)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": "已展示给用户，请等待用户回复后再继续。不要在本轮继续提问。",
                })
                has_interactive_ui = True
            elif tc.function.name in DISPLAY_UI_TOOLS:
                block = _ui_tool_to_block(tc.function.name, args)
                response_blocks.append(block)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": "已展示给用户。",
                })
            else:
                result = _execute_backend_tool(tc.function.name, args, session)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

        if has_interactive_ui:
            break

    session["messages"] = messages
    if response_blocks:
        last_assistant = ""
        for b in response_blocks:
            if b["type"] == "text":
                last_assistant += b["content"]
        if last_assistant:
            session["messages"].append({"role": "assistant", "content": last_assistant})

    return response_blocks
