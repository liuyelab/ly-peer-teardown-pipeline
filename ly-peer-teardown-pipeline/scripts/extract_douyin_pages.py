#!/usr/bin/env python3
"""从抖音「重点视频原始页面文本」批量提取结构化字段（编码自动检测）。

用法: python extract_douyin_pages.py <页面文本目录> [输出.json路径]
输出: JSON 列表 [{file,url,title,chapters,data,pub,comments}, ...]  UTF-8

页面文本为 UTF-8/GBK 混合（read_file 会把 GBK/UTF-16 误判为 binary），
本脚本按 utf-8-sig -> utf-8 -> gbk 依次尝试解码。
互动数据行正则解析「赞/评/藏/享」（位于「举报」前，数字可能带「万」）。
"""
import os, re, sys, json


def read_any(path):
    for enc in ['utf-8-sig', 'utf-8', 'gbk']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(path, 'rb') as f:
        return f.read().decode('utf-8', errors='replace')


def extract(fn_text):
    lines = [l.strip() for l in fn_text.split('\n')]
    url = title = ''
    for l in lines:
        if l.startswith('URL: '):
            url = l[5:]
        elif l.startswith('TITLE: '):
            title = l[7:]
    out = {'url': url, 'title': title}
    # 章节要点：'章节要点' 到 '全部评论' 之间
    try:
        start = lines.index('章节要点')
        end = lines.index('全部评论')
        out['chapters'] = '\n'.join(lines[start + 1:end])
    except ValueError:
        out['chapters'] = '(无章节要点)'
    # 互动数据：举报 前一行组 = 赞/评/藏/享
    m = re.search(r'(\d[\d.,万]*)\s*\n(\d+)\s*\n(\d+)\s*\n(\d+)\s*\n举报', fn_text)
    out['data'] = f"赞{m.group(1)} 评{m.group(2)} 藏{m.group(3)} 享{m.group(4)}" if m else ''
    pm = re.search(r'发布时间：([\d\-]+ [\d:]+)', fn_text)
    out['pub'] = pm.group(1) if pm else ''
    # 评论区：'全部评论' 到 '暂时没有更多评论' / '推荐视频' 之间
    try:
        cstart = lines.index('全部评论')
        cend = None
        for cand in ['暂时没有更多评论', '推荐视频']:
            try:
                idx = lines.index(cand, cstart)
                if cend is None or idx < cend:
                    cend = idx
            except ValueError:
                pass
        out['comments'] = '\n'.join(lines[cstart + 1:cend]) if cend else '\n'.join(lines[cstart + 1:])
    except ValueError:
        out['comments'] = ''
    return out


def main():
    base = sys.argv[1]
    out_json = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), 'extracted.json')
    results = []
    for fn in sorted(os.listdir(base)):
        if not fn.endswith('.txt'):
            continue
        r = extract(read_any(os.path.join(base, fn)))
        r['file'] = fn
        results.append(r)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f'{len(results)} files -> {out_json}')


if __name__ == '__main__':
    main()
