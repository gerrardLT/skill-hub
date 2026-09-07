# 安装并初始化 Agentic SDLC OS 的提示词

把下面内容交给你的 Coding Agent，并把 `<仓库路径>`、`<项目路径>`、`<agent>` 替换掉。

```text
请把 Agentic SDLC Operating System 安装到当前软件项目，并完成可验证初始化。

输入：
- SDLC OS 仓库：<仓库路径>
- 目标项目：<项目路径>
- Agent：<agent>，可选 generic / claude / cursor / codex / copilot / opencode
- 项目类型：greenfield；已有项目改为 brownfield
- 关键等级：medium；涉及资金、医疗、隐私或核心生产数据时改为 high
- 流程档位：standard；低风险可逆试验可用 lite，高风险项目必须用 high-assurance

执行要求：
1. 先检查 Python 3、Node.js、npx、Git 和目标目录权限；不要修改生产环境。
2. 在 SDLC OS 仓库运行：
   python scripts/validate_all.py
   python -m unittest discover -s tests -v
3. 安装 7 个本地 Orchestrator Skills：
   python scripts/install_local_skills.py --agent <agent> --project <项目路径>
4. 找到已安装的 agentic-sdlc-os/scripts/sdlc.py，并初始化目标项目：
   python <sdlc.py路径> init <项目路径> --name <项目名> --type greenfield --criticality medium --profile standard
   若已经存在 .sdlc，不覆盖；先读取并验证。
5. 只预览第三方 Skills，不立即全部安装：
   python <install_external_skills.py路径> --os all --profile core
6. 根据目标项目实际技术栈和当前阶段，给出需要安装的最小第三方 Skill 集。逐个审查 SKILL.md、脚本、Hook、网络/写权限、依赖和许可证。只有审查通过后，才使用：
   python <install_external_skills.py路径> --os <os> --profile core --execute --acknowledge-review
   自定义安装器还必须显式增加 --allow-custom。
7. 如果目标是已有项目中的单个 bounded change/defect，初始化后先运行：
   python <sdlc.py路径> work-start <项目路径> --id WORK-001 --title "<变更>" --bounded --affected-path <受影响路径>
   以 Work Item Profile 决定实际 Gate 深度；不要用项目级 high-assurance 给无关小修复制造文档负担。
8. 运行：
   python <sdlc.py路径> audit <项目路径>
   python <sdlc.py路径> health <项目路径>
   python <sdlc.py路径> validate <项目路径>
   python <sdlc.py路径> status <项目路径>
   python <sdlc.py路径> next <项目路径>
9. 最后输出：安装目录、已安装 Skills、未安装及原因、项目当前 OS/Stage、验证结果、下一步。不得声称安装成功而不检查文件和命令退出码。
```
