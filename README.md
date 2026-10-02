# 同行拆解流水线（LY Peer Teardown Pipeline）

**English** · An AI agent skill that tears down any short-video creator account (Douyin / TikTok-style) and turns it into a reusable content library: a full research report, a one-page cheat sheet, and a 5-section swipe file (titles, hooks, quotes, cases, structure templates) — every item sourced and backed by real engagement data. Works with Claude Code, Codex and other file-capable agents. [Jump to English section ↓](#english)

---

一个给 AI 用的技能（Skill）：把任意一个短视频同行账号扒透，自动产出三件套——

1. **完整同行研究报告**：定位、核心方法论、爆款规律、评论区信号、作品全列表、能抄的和别学的
2. **蒸馏卡**：一页速查，核心公式、标题公式、爆款规律
3. **五区素材库**：A 标题 / B 开场钩子 / C 观点金句 / D 案例 / E 结构模板，每一条都标来源、数据和"怎么套"

适合做短视频、知识付费、自媒体的人，用来研究对标账号、攒自己的选题和话术素材。

## 怎么装

看 [安装指南.md](安装指南.md)，三步，不用懂代码。

支持能读写文件的 AI 工具：Claude Code、Codex、Hermes、WorkBuddy 等。

## 怎么用

装好后对 AI 说：

> 用同行拆解流水线，帮我拆一下抖音账号「xxx」

AI 有浏览器控制能力时会自己抓视频页面；没有的话，你手动把视频页面文字复制成 txt 给它也一样。

## 文件说明

- `SKILL.md`：技能本体（流程和规则）
- `references/`：报告模板、抖音页面文本解析方法
- `scripts/`：可选的 Python 加速脚本

## 注意

- 引用别人的内容请标来源；金句可以借鉴，别搬原画面。
- 互动数据以页面实际为准，技能要求 AI 不编造数据。

## 作者

刘野老师｜抖音号 **liuyelab**（用 AI 做内容、做事、赚钱）

## 许可

CC BY-NC 4.0（署名-非商业性使用），© 2026 刘野。可免费使用、修改、分享，需署名，禁止商用（包括出售、打包卖、放进付费课程或付费社群）。详见 [LICENSE](LICENSE)。

---

## English

**LY Peer Teardown Pipeline** is a skill (prompt + workflow + helper scripts) for AI agents. Point it at a competitor's short-video account and it produces three deliverables:

1. **Full research report** — positioning, core methodology, viral-content patterns, comment-section signals, complete video list, and what to copy vs. what to avoid.
2. **Distillation card** — a one-page cheat sheet with the core formula, title formulas and viral patterns.
3. **Five-section swipe file** — A. Titles / B. Opening hooks / C. Quotes / D. Cases / E. Structure templates. Each item lists its source, engagement data, and how to adapt it.

Built for short-video creators, educators and solo media businesses who want to study benchmark accounts systematically instead of scrolling.

**Install** — download this repo as ZIP, then tell your agent: *"Install the skill in this zip into your skills directory."* Works with Claude Code, Codex, Hermes, WorkBuddy and any agent that can read/write files.

**Use** — *"Use the peer teardown pipeline to analyze Douyin account XXX."* Agents with browser control fetch the video pages themselves; otherwise paste page text into .txt files.

**Rules baked in** — never fabricate engagement numbers; mark evidence ✅ (verified) vs ⚠️ (inferred); credit sources; borrow ideas, not footage.

**Author** — Liu Ye (刘野老师), Douyin ID: liuyelab

**License** — CC BY-NC 4.0 © 2026 Liu Ye (刘野). Free to use, modify and share with attribution; **no commercial use** (no reselling, bundling, or inclusion in paid courses/communities).

> The skill's prompts and outputs are in Chinese and tuned for Douyin page structure; the method itself applies to any short-video platform.
