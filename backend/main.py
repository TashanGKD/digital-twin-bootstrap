"""FastAPI 入口：Block 协议 SSE、画像、量表、模型列表"""
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel

from agent import run_agent
from config import AVAILABLE_MODELS
from sessions import get_or_create, get, reset, save_scales

app = FastAPI(title="他山数字分身 Web API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str
    model: str | None = None


class ScaleSubmitRequest(BaseModel):
    session_id: str
    scale_name: str
    answers: dict
    scores: dict
    result_summary: dict | None = None


@app.post("/chat", response_class=StreamingResponse)
async def chat_stream(req: ChatRequest):
    """Block 协议 SSE：每个 Block 作为一个 SSE 事件发送"""
    session_id, session = get_or_create(req.session_id)
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")

    def generate():
        try:
            blocks = run_agent(req.message, session, model=req.model)
            for block in blocks:
                yield f"data: {json.dumps(block, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'text', 'content': f'服务器错误: {e}'}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-Id": session_id,
        },
    )


@app.get("/profile/{session_id}")
async def get_profile(session_id: str):
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    return {
        "profile": session["profile"],
        "forum_profile": session.get("forum_profile", ""),
    }


@app.get("/profile/{session_id}/structured")
async def get_structured_profile(session_id: str):
    from profile_parser import parse_profile

    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    return parse_profile(session["profile"])


@app.get("/profile/{session_id}/scientists/famous")
async def get_famous_matches(session_id: str):
    """知名科学家匹配（纯计算，瞬间返回）"""
    from profile_parser import parse_profile
    from scientist_match import match_famous_scientists

    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    parsed = parse_profile(session["profile"])
    return match_famous_scientists(parsed)


@app.get("/profile/{session_id}/scientists/field")
async def get_field_recommendations(session_id: str):
    """领域相关科学家推荐（LLM 调用，可能较慢）"""
    from profile_parser import parse_profile
    from scientist_match import recommend_field_scientists

    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    parsed = parse_profile(session["profile"])
    return {"recommendations": recommend_field_scientists(parsed)}


@app.get("/download/{session_id}")
async def download_profile(session_id: str):
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    return Response(
        content=session["profile"].encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="profile.md"'},
    )


@app.get("/download/{session_id}/pdf")
async def download_profile_pdf(session_id: str):
    from pdf_export import profile_md_to_pdf

    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    try:
        pdf_bytes = profile_md_to_pdf(session["profile"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 生成失败: {e}")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="profile.pdf"'},
    )


@app.get("/download/{session_id}/forum")
async def download_forum_profile(session_id: str):
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    content = session.get("forum_profile", "")
    if not content:
        raise HTTPException(status_code=404, detail="尚未生成论坛分身")
    return Response(
        content=content.encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="forum-profile.md"'},
    )


@app.get("/models")
async def list_models():
    return {"models": AVAILABLE_MODELS}


@app.post("/scales/submit")
async def submit_scale(req: ScaleSubmitRequest):
    session = get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    save_scales(session, req.scale_name, {
        "answers": req.answers,
        "scores": req.scores,
        "result_summary": req.result_summary,
    })
    return {"ok": True, "scale_name": req.scale_name}


@app.get("/scales/{session_id}")
async def get_scales(session_id: str):
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    return {"scales": session.get("scales", {})}


@app.get("/session")
async def session_get(session_id: str | None = None):
    sid, _ = get_or_create(session_id)
    return {"session_id": sid}


@app.post("/session/reset/{session_id}")
async def session_reset(session_id: str):
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    reset(session_id)
    return {"ok": True, "session_id": session_id}
