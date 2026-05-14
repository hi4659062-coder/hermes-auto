#!/usr/bin/env python3
"""AI Code Review Script - runs in GitHub Actions, posts comment on PR"""
import json, os, subprocess, sys, urllib.request


def _post_comment(body):
    """Post comment on the PR using gh CLI"""
    pr_num = os.environ.get('PR_NUMBER')
    if not pr_num:
        return
    gh_cmd = ['gh', 'pr', 'comment', pr_num, '--body', f"## 🤖 AI Code Review\n\n{body}"]
    subprocess.run(gh_cmd, capture_output=True)


diff = subprocess.run(
    ['git', 'diff', 'origin/main...HEAD'],
    capture_output=True, text=True
).stdout[:5000]

if not diff.strip():
    comment = "没有代码变更需要审查。"
    print(comment)
    _post_comment(comment)
    sys.exit(0)

print(f"审查 {len(diff)} 字符的变更...")

payload = json.dumps({
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "messages": [
        {"role": "system", "content": "你是一个代码审查助手。审查代码变更，找出bug、安全问题、代码质量问题、缺少类型标注。用中文回复。"},
        {"role": "user", "content": f"请审查以下代码变更：\n```diff\n{diff}\n```"}
    ],
    "temperature": 0.1,
    "max_tokens": 2000
}).encode()

req = urllib.request.Request(
    "https://api.modelscope.cn/v1/chat/completions",
    data=payload,
    headers={
        "Authorization": f"Bearer {os.environ['API_KEY']}",
        "Content-Type": "application/json"
    }
)

try:
    resp = urllib.request.urlopen(req, timeout=90)
    data = json.loads(resp.read())
    content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
    if content:
        print(content)
        _post_comment(content)
    else:
        msg = f"审查失败: {json.dumps(data, ensure_ascii=False)}"
        print(msg)
        _post_comment(msg)
except Exception as e:
    msg = f"API Error: {e}"
    print(msg)
    _post_comment(msg)
    sys.exit(1)
