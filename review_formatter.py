#!/usr/bin/env python3
import json, sys

with open('/tmp/review_response.json') as f:
    d = json.load(f)

content = d.get('choices', [{}])[0].get('message', {}).get('content', '')
if content:
    print(content)
else:
    print('审查失败:', json.dumps(d, ensure_ascii=False))
print()
print('---')
print('✅ 自动审查完成')
