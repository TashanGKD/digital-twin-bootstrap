"""将画像 Markdown 转为 PDF（纯 Python，无需系统依赖）"""
import io
import markdown
from xhtml2pdf import pisa

CSS = """
@page {
    size: A4;
    margin: 2cm 1.8cm;
}
body {
    font-family: STSong, SimSun, serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #111;
}
h1 { font-size: 18pt; border-bottom: 2px solid #000; padding-bottom: 4pt; margin-top: 20pt; }
h2 { font-size: 14pt; border-bottom: 1px solid #ccc; padding-bottom: 3pt; margin-top: 18pt; }
h3 { font-size: 12pt; margin-top: 14pt; }
table { width: 100%; border-collapse: collapse; margin: 8pt 0; font-size: 10pt; }
th, td { border: 1px solid #ccc; padding: 4pt 6pt; text-align: left; }
th { background: #f5f5f5; font-weight: bold; }
blockquote { border-left: 3px solid #000; margin: 8pt 0; padding: 4pt 12pt; color: #555; }
code { background: #f3f4f6; padding: 1pt 3pt; font-size: 9pt; }
pre { background: #f3f4f6; padding: 8pt; font-size: 9pt; }
hr { border: none; border-top: 1px solid #ddd; margin: 14pt 0; }
strong { color: #000; }
"""


def profile_md_to_pdf(md_content: str) -> bytes:
    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code"],
    )
    full_html = f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_body}</body>
</html>"""

    buf = io.BytesIO()
    pisa.CreatePDF(io.StringIO(full_html), dest=buf, encoding="utf-8")
    return buf.getvalue()
