# 新项目接管提示词

```text
使用 Agentic SDLC OS 接管当前新项目。

1. 读取 .sdlc；不存在则按关键等级选择 lite / standard / high-assurance，并以 greenfield 初始化。
2. 从现有材料提取用户、问题、业务目标、约束和最大未知量，分离事实/推断/假设/决策。
3. 不机械运行全部 OS。先判断当前最早缺失且高价值的阶段。
4. 默认从 PM/DISCOVERY 开始，建立可证伪问题假设和证据计划。
5. 每完成一个关键制品就注册到 .sdlc，添加证据、风险和有向追踪关系。
6. Gate 未通过不得进入下一个 OS；不得自行豁免。
7. 持续执行直到形成当前可完成的最小闭环；每次输出 Current OS/Stage、Decision、Evidence、Artifact、Gate、Next。
```
