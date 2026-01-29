# 🐱 小红书宠物内容自动化系统

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-blue)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

基于GitHub Actions的全自动化小红书宠物内容生成系统，每天自动生成2篇高互动宠物测试类图文，结合热点追踪，助你快速涨粉！

## 🎯 系统特色

### 🤖 智能内容生成
- **AI文案**：GPT-4生成小红书风格文案
- **AI配图**：DALL-E生成大字报风格配图
- **问题设计**：基于知识、行为、趣味三大类别的测试题
- **热点结合**：自动追踪并融入热门话题

### ⏰ 定时自动化
- **每天2篇**：早上6点 + 晚上8点（北京时间）
- **零运维**：GitHub Actions免费托管，无需服务器
- **自动记录**：所有内容自动保存，可追溯

### 🎨 爆款内容模式
- **测试类内容**：高互动、高评论
- **福利诱饵**：送宠物试用装提升参与度
- **时效性**：次日揭晓答案，持续引流
- **大字报风格**：视觉冲击力强，容易被点击

## 📁 项目结构

```
media-automation/
├── .github/
│   └── workflows/
│       └── daily-publish.yml    # GitHub Actions定时工作流
├── scripts/
│   ├── content_generator.py     # 🐱 宠物内容生成器
│   ├── hot_topics.py            # 热点话题追踪器
│   ├── publisher.py             # 平台发布器
│   └── save_records.py          # 记录保存器
├── content/                      # 生成的内容存储
│   └── xiaohongshu/            # 小红书内容
│       └── YYYY-MM-DD/         # 按日期分类
├── data/
│   ├── records/                 # 发布记录
│   ├── hot_topics/              # 热点话题记录
│   └── statistics/              # 统计数据
├── logs/                        # 运行日志
├── config.py                    # 配置文件
├── requirements.txt             # Python依赖
└── README.md                    # 项目说明
```

## 🚀 快速开始

### 1. Fork并克隆项目

```bash
# Fork本项目到你的GitHub账号
# 然后克隆到本地
git clone https://github.com/你的用户名/media-automation.git
cd media-automation
```

### 2. 配置GitHub Secrets

在GitHub仓库的 **Settings → Secrets and variables → Actions** 中添加：

| Secret Name | 说明 | 获取方式 |
|------------|------|---------|
| `OPENAI_API_KEY` | OpenAI API密钥 | [OpenAI Platform](https://platform.openai.com/api-keys) |
| `OPENAI_MODEL` | GPT模型 | 默认为 `gpt-4o` |
| `IMAGE_API_KEY` | DALL-E API密钥 | 可使用OpenAI的DALL-E |
| `XIAOHONGSHU_COOKIE` | 小红书Cookie | 浏览器登录后复制 |

### 3. 启用GitHub Actions

1. 进入 **Actions** 标签
2. 找到 **"小红书宠物内容自动化"** 工作流
3. 点击 **Enable workflow**

### 4. 测试运行

在Actions页面手动触发，观察生成效果。

## 📝 内容格式示例

### 每篇包含4张图片

1. **主图** - 大字报风格
   ```
   测测你是不是合格铲屎官？送宠物试用装了！
   ```

2. **问题图×3** - 大字报+卡通搞笑风格
   - 每张1个宠物问题（基础知识/行为解读/趣味挑战）
   - A/B双选题
   - 可爱卡通背景

### 正文结构

```
🐱 各位铲屎官们看过来！今天给大家准备了一份猫咪/狗狗知识测试卷...

📋 测试规则：
❓ 第1题：以下哪种食物猫咪绝对不能吃？
   A. 鸡肉  B. 巧克力

❓ 第2题：猫咪对你露出肚皮说明什么？
   A. 想让你摸  B. 完全信任你

❓ 第3题：猫咪快速摇尾巴代表什么？
   A. 开心  B. 烦躁

📝 评分标准：
✅ 答对3个 = 优秀铲屎官 🌟
✅ 答对2个 = 合格铲屎官 💪
✅ 答对1个 = 差劲铲屎官 😅

💬 请在评论区留下你的答案，明天揭晓正确答案！

🎁 福利时间！
随机抽取1-3名优秀铲屎官送出宠物试用装！

🏷️ 标签: #猫咪 #铲屎官 #宠物测试 #养宠知识 #宠物试用装
```

## ⚙️ 自定义配置

### 修改发布频率

编辑 `.github/workflows/daily-publish.yml`：

```yaml
on:
  schedule:
    # 早间内容 (UTC时间22点 = 北京时间6点)
    - cron: '0 22 * * *'
    # 晚间内容 (UTC时间12点 = 北京时间20点)
    - cron: '0 12 * * *'
```

### 修改宠物类型

编辑 `config.py`：

```python
# 宠物类型（混合模式）
PET_TYPES = ["猫咪", "狗狗", "猫咪和狗狗"]
```

### 修改问题类型

编辑 `config.py` 中的问题库：

```python
PET_TOPIC_CATEGORIES = {
    "基础知识": [
        "猫咪不能吃的食物",
        "狗狗不能吃的食物",
        # 添加更多...
    ],
    "行为解读": [
        "猫咪摇尾巴代表什么",
        "狗狗拆家原因",
        # 添加更多...
    ],
    "趣味挑战": [
        "猫咪能看懂电视吗",
        "狗狗的梦境",
        # 添加更多...
    ]
}
```

### 修改图片风格

编辑 `config.py`：

```python
PET_IMAGE_STYLES = {
    "main_poster": {
        "style": "大字报风格，简洁有力...",
        "colors": ["#FF6B6B", "#4ECDC4", "#FFE66D"]
    },
    "question_card": {
        "style": "大字报+卡通搞笑风格...",
        "colors": ["#FFE4E1", "#E6E6FA", "#FFF0F5"]
    }
}
```

## 📊 发布计划

### 早间内容（6:00）
- **类型**：知识测试
- **热点权重**：30%
- **目标**：抢占用户早起时间

### 晚间内容（20:00）
- **类型**：趣味挑战
- **热点权重**：50%
- **目标**：晚间流量高峰

## 🔧 本地测试

### 安装依赖

```bash
pip install -r requirements.txt
```

### 生成早间内容

```bash
python scripts/content_generator.py --type morning
```

### 生成晚间内容

```bash
python scripts/content_generator.py --type evening
```

### 生成两篇内容

```bash
python scripts/content_generator.py --type both
```

### 查看热点话题

```bash
python scripts/hot_topics.py
```

## 📈 内容策略

### 为什么选择测试类内容？

1. **高互动**：用户喜欢参与测试
2. **易传播**：分享欲强
3. **持续性**：次日揭晓答案，持续引流
4. **低门槛**：答题不需要专业知识

### 福利诱饵设计

- **试用装**：成本低，用户愿意参与
- **时效性**：次日开奖，保持互动
- **随机性**：增加不确定性和期待感

### 热点结合策略

- 节假日话题
- 季节性话题
- 社会热点
- 时间节点（周一、周五等）

## ⚠️ 注意事项

### API限制

- OpenAI API有速率限制
- DALL-E生成图片需要1-2分钟
- 建议使用gpt-4o和dall-e-3

### 发布建议

- 初期测试模式，确认内容质量
- 注意平台内容审核规则
- 建议每天2篇，不要过度发布

### 安全提醒

- **不要**将API密钥写在代码中
- **不要**在公开仓库暴露凭证
- 定期轮换API密钥

## 🛠️ 故障排除

### 内容生成失败

1. 检查OpenAI API密钥
2. 查看GitHub Actions日志
3. 确认API配额

### 图片生成失败

1. 检查DALL-E API配置
2. 降低图片质量或尺寸
3. 确认API配额

### 发布失败

小红书目前需要手动发布或对接真实API。

## 📝 更新日志

### v2.0.0 (2024-01)
- ✨ 全新宠物内容专家模式
- 🎨 大字报风格配图
- ❓ 3道测试题+评分系统
- 🔥 热点话题自动追踪
- ⏰ 每天2篇定时发布
- 📊 完整的记录和统计

### v1.0.0 (2024-01)
- 🚀 初始版本发布
- 🤖 GPT内容生成
- 📱 小红书+公众号发布

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 感谢

- [OpenAI](https://openai.com/) - AI能力支持
- [GitHub](https://github.com/) - Actions托管

---

**⭐ 如果对你有帮助，请给个Star支持一下！**
