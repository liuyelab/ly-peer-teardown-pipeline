# -*- coding: utf-8 -*-
"""抖音视频页面文本解析器（实测于 2026-08 三个账号 × 20 条 = 60 文件）。

输入：同行素材库/{账号名}/原始资料/重点视频原始页面文本/{video_id}-{赞数}{标题}.txt
页面文本结构：
- URL: / TITLE: 前缀行
- TITLE 行后紧跟 4 个纯数字 = 赞/评论/收藏/分享
- `发布时间：YYYY-MM-DD HH:MM`
- 评论区：`全部评论` 开始；`加载中`/`暂时没有更多评论`/`认证徽章`/`粉丝X获赞Y` 结束
- 单条评论：用户名 → `...` → 内容 → 时间行(如 `2年前·天津`) → 赞数(纯数字) → `分享`/`回复`
- 作者评论：用户名行后跟 `作者` 行（内容行前仍有 `...` 行）
- 账号信息在页面尾部：`粉丝12.3万获赞55.7万`

用法：
    from parse_douyin_page_text import read_any, extract
    url, title, pub, nums, comments = extract(txt_path)
    # nums = [赞, 评论, 收藏, 分享]（TITLE 行匹配失败时可能为 []，赞数兜底用文件名前缀 + manifest like）
    # comments = [(用户名, 内容, 赞数字符串), ...]

注意：execute_code stdout 上限 50KB，按账号分批打印，评论内容截断 ~100-120 字。
"""
import os
import re


def read_any(path):
    """UTF-8/UTF-16/GBK 混合编码自动探测读取（read_file 对 UTF-16 会误判 binary）。"""
    with open(path, 'rb') as f:
        raw = f.read()
    for enc in ['utf-8-sig', 'utf-8', 'utf-16', 'gbk']:
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode('latin-1')


def extract(path):
    c = read_any(path)
    lines = [l.strip() for l in c.split('\n') if l.strip()]
    url = next((l[4:].strip() for l in lines if l.startswith('URL:')), '')
    title = next((l[6:].strip() for l in lines if l.startswith('TITLE:')), '')
    pub = ''
    for l in lines:
        m = re.search(r'发布时间：(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', l)
        if m:
            pub = m.group(1)
            break
    # TITLE 行后紧跟的纯数字 = 赞/评论/收藏/分享
    nums = []
    for idx, l in enumerate(lines):
        if l == title and idx + 1 < len(lines):
            j = idx + 1
            while j < len(lines) and re.match(r'^\d+$', lines[j]):
                nums.append(lines[j])
                j += 1
            break
    # 评论区
    comments = []
    start = False
    i = 0
    while i < len(lines):
        l = lines[i]
        if l == '全部评论':
            start = True
            i += 1
            continue
        if not start:
            i += 1
            continue
        if l in ('加载中', '暂时没有更多评论', '认证徽章'):
            break
        if l.startswith('粉丝') and re.search(r'获赞', l):
            break
        if l in ('...', '作者', '分享', '回复', '留下你的精彩评论吧', '大家都在搜：') or l.startswith('展开'):
            i += 1
            continue
        if re.match(r'^\d+$', l) or ('·' in l and ('前' in l or 'IP未知' in l)):
            i += 1
            continue
        # 用户名行：下一行必为 '...'，再下一行是内容
        if i + 1 < len(lines) and lines[i + 1] == '...':
            content = lines[i + 2] if i + 2 < len(lines) else ''
            like = ''
            for j in range(i + 3, min(i + 7, len(lines))):
                if re.match(r'^\d+$', lines[j]):
                    like = lines[j]
                    break
            if content and not content.startswith('展开'):
                comments.append((l, content, like))
            i += 3
            continue
        i += 1
    return url, title, pub, nums, comments


def account_stats(folder):
    """从目录内全部 txt 尾部抽取账号粉丝/获赞（去重）。"""
    stats = set()
    for f in os.listdir(folder):
        c = read_any(os.path.join(folder, f))
        for m in re.finditer(r'粉丝([\d.]+万?)\s*获赞([\d.]+万?)', c):
            stats.add(f"粉丝{m.group(1)} 获赞{m.group(2)}")
    return stats


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    url, title, pub, nums, comments = extract(p)
    print(f"URL: {url}\nTITLE: {title}\n发布: {pub}\n互动(赞/评/藏/享): {nums}")
    for name, content, like in comments:
        print(f"[{like}] {name}: {content[:100]}")
