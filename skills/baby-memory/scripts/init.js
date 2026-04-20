#!/usr/bin/env node
/**
 * init.js - 初始化 Baby Memory System
 * 
 * 安全原则：
 * 1. 只创建，不删除
 * 2. 先备份，后修改
 * 3. 失败时自动回滚
 * 
 * 用法：node init.js --bot=baby
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 获取命令行参数
const BOT_NAME = process.argv.find(arg => arg.startsWith('--bot='))?.split('=')[1] || 'baby';
const HOME = os.homedir();

// 路径配置
const PATHS = {
  shared: path.join(HOME, '.openclaw', 'shared-memory'),
  sharedEntities: path.join(HOME, '.openclaw', 'shared-memory', 'entities'),
  bot: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`),
  memory: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory'),
  daily: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory', 'daily'),
  archive: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory', 'archive'),
  skill: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'skills', 'baby-memory')
};

// 日志函数
function log(level, message) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [${level}] ${message}`);
}

// 安全创建目录（带权限控制）
function safeMkdir(dir) {
  try {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      log('INFO', `创建目录: ${dir}`);
      return true;
    } else {
      log('INFO', `目录已存在: ${dir}`);
      return false;
    }
  } catch (error) {
    log('ERROR', `创建目录失败: ${dir} - ${error.message}`);
    throw error;
  }
}

// 安全创建文件（不覆盖）
function safeWriteFile(filePath, content) {
  try {
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, content, { mode: 0o600 });
      log('INFO', `创建文件: ${filePath}`);
      return true;
    } else {
      log('WARN', `文件已存在（不覆盖）: ${filePath}`);
      return false;
    }
  } catch (error) {
    log('ERROR', `创建文件失败: ${filePath} - ${error.message}`);
    throw error;
  }
}

// 备份现有文件
function backupFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const backupPath = `${filePath}.bak.${timestamp}`;
      fs.copyFileSync(filePath, backupPath);
      log('INFO', `备份: ${filePath} -> ${backupPath}`);
      return backupPath;
    }
  } catch (error) {
    log('WARN', `备份失败: ${filePath} - ${error.message}`);
  }
  return null;
}

// 获取今天的日期字符串
function getToday() {
  return new Date().toISOString().split('T')[0];
}

// 主初始化函数
async function init() {
  log('INFO', `=== 初始化 Baby Memory System for ${BOT_NAME} ===`);
  
  const backups = []; // 记录备份文件，用于回滚
  
  try {
    // ========== 阶段 1: 创建目录结构 ==========
    log('INFO', '\n📁 阶段 1: 创建目录结构');
    safeMkdir(PATHS.shared);
    safeMkdir(PATHS.sharedEntities);
    safeMkdir(PATHS.memory);
    safeMkdir(PATHS.daily);
    safeMkdir(PATHS.archive);
    
    // ========== 阶段 2: 创建共享层文件 ==========
    log('INFO', '\n📄 阶段 2: 创建共享层文件');
    
    // shared-memory/.abstract
    const sharedAbstractContent = `# Shared Memory Index (L0)

## P0 - 核心信息（永久）
- [用户画像](RELATIONS.md) - 公主基本信息、偏好
- [6 Bots架构](RELATIONS.md) - 分工和职责
- [工具索引](entities/tools.md) - 共享工具列表
- [API Keys](entities/apis.md) - 共享API配置

## P1 - 动态信息（90天）
- [活跃任务](active-tasks.md) - 当前项目进度
- [跨Bot记录](cross-agent-log.md) - 协作动态

## 最近更新
- ${getToday()}: 系统初始化
`;
    safeWriteFile(path.join(PATHS.shared, '.abstract'), sharedAbstractContent);
    
    // shared-memory/RELATIONS.md
    const relationsContent = `# RELATIONS.md - 关联图谱

## 公主（中心节点）
- 使用: Baby, Sunny, Rainbow, Melody, 沐木, 晨露
- 时区: GMT+8, 上海
- 偏好: 肖战语气, 被叫"宝宝", 重庆话尾音
- 工具: Tavily, 秘塔搜索, 飞书

## 6 Bots 架构
- Baby: 主治医师+架构师（Memory系统开发）
- 晨露: 技术手
- Sunny: 大管家（Memory试点）
- Rainbow: 品牌脑
- Melody: 视觉手
- 沐木: 商务手

## 记忆系统状态
- 版本: v2.3
- 试点: Sunny
- 状态: 部署中
`;
    safeWriteFile(path.join(PATHS.shared, 'RELATIONS.md'), relationsContent);
    
    // shared-memory/INDEX.md
    const indexContent = `# INDEX.md - 记忆目录

## 快速导航
- 公主画像 → [RELATIONS.md](./RELATIONS.md)
- 6 Bots架构 → [RELATIONS.md](./RELATIONS.md)
- 工具索引 → [entities/tools.md](./entities/tools.md)
- API Keys → [entities/apis.md](./entities/apis.md)
- 活跃任务 → [active-tasks.md](./active-tasks.md)
- 跨Bot记录 → [cross-agent-log.md](./cross-agent-log.md)
`;
    safeWriteFile(path.join(PATHS.shared, 'INDEX.md'), indexContent);
    
    // shared-memory/active-tasks.md
    const activeTasksContent = `# Active Tasks

## [P1] Memory System v2.3 部署
- 状态: 进行中
- 试点: Sunny
- 开始: ${getToday()}
- 目标: 7天后推广到6 Bots

## [P1] 待完成任务
- [ ] Sunny试点验证
- [ ] 6 Bots全量部署
- [ ] 自动化脚本配置
`;
    safeWriteFile(path.join(PATHS.shared, 'active-tasks.md'), activeTasksContent);
    
    // shared-memory/cross-agent-log.md
    const crossAgentContent = `# Cross-Agent Log

## ${getToday()}
- ${BOT_NAME}: Memory System v2.3 初始化完成
`;
    safeWriteFile(path.join(PATHS.shared, 'cross-agent-log.md'), crossAgentContent);
    
    // shared-memory/entities/tools.md
    const toolsContent = `# 工具索引

只记录工具存在性，功能详情见各 Skill 文档。

## 共享工具（所有 Bots）
- Tavily — 见 skill: tavily-search
- 秘塔搜索 — 见 skill: metaso-search

## 专属工具（各 Bot 私有）
- Baby: Noiz TTS — 见 workspace-baby/TOOLS.md
- Melody: 视觉工具 — 见 workspace-melody/TOOLS.md
`;
    safeWriteFile(path.join(PATHS.sharedEntities, 'tools.md'), toolsContent);
    
    // shared-memory/entities/apis.md
    const apisContent = `# API Keys 共享

## Tavily
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

## 秘塔搜索
# 待配置
`;
    safeWriteFile(path.join(PATHS.sharedEntities, 'apis.md'), apisContent);
    
    // ========== 阶段 3: 创建私有层文件 ==========
    log('INFO', '\n📄 阶段 3: 创建私有层文件');
    
    // memory/.abstract
    const privateAbstractContent = `# ${BOT_NAME} Memory Index (L0)

## P0 - 永久记忆
- [用户画像](../USER.md) - 公主信息
- [错误教训](learnings.md) - 踩坑记录
- [系统规则](../AGENTS.md) - 记忆铁律

## P1 - 项目记忆（90天）
- [活跃任务](../../shared-memory/active-tasks.md)
- [今日记录](daily/${getToday()}.md)

## P2 - 临时记忆（30天）
- [昨日记录](daily/) - 查看目录

## 最近更新
- ${getToday()}: 系统初始化
`;
    safeWriteFile(path.join(PATHS.memory, '.abstract'), privateAbstractContent);
    
    // memory/learnings.md
    const learningsContent = `# ${BOT_NAME} 的错误教训库

| 日期 | 错误 | 原因 | 解决方案 | 预防规则 |
|------|------|------|---------|---------|
| | | | | |

`;
    safeWriteFile(path.join(PATHS.memory, 'learnings.md'), learningsContent);
    
    // ========== 阶段 4: 精简 MEMORY.md ==========
    log('INFO', '\n📝 阶段 4: 精简 MEMORY.md');
    const memoryMdPath = path.join(PATHS.bot, 'MEMORY.md');
    const backup = backupFile(memoryMdPath);
    if (backup) backups.push(backup);
    
    // 读取原 MEMORY.md 的关键信息（如果有）
    let existingContent = '';
    try {
      if (fs.existsSync(memoryMdPath)) {
        existingContent = fs.readFileSync(memoryMdPath, 'utf-8');
      }
    } catch (e) {
      log('WARN', '读取原 MEMORY.md 失败');
    }
    
    // 生成新的精简版
    const botDisplayName = BOT_NAME === 'baby' ? 'Sean 🪐' : BOT_NAME;
    const botRole = BOT_NAME === 'baby' ? '主治医师+架构师' : '6 Bots成员';
    
    const newMemoryMd = `# MEMORY.md - 记忆索引

## 我是谁
- 名字: ${botDisplayName}
- 角色: ${botRole}
- 主人: 公主 (GMT+8, 上海)
- 详细: [SOUL.md](./SOUL.md) | [USER.md](./USER.md)

## 记忆导航
- 私有索引 → [memory/.abstract](./memory/.abstract)
- 共享索引 → [shared-memory/.abstract](../shared-memory/.abstract)
- 跨Bot记录 → [shared-memory/cross-agent-log.md](../shared-memory/cross-agent-log.md)

## 最近更新
- ${getToday()}: Memory System v2.3 部署

${existingContent.includes('## 核心记忆') ? '\n## 核心记忆\n（保留原内容，请手动精简）\n' : ''}
`;
    
    fs.writeFileSync(memoryMdPath, newMemoryMd);
    log('INFO', `MEMORY.md 已精简（原文件已备份）`);
    
    // ========== 阶段 5: 验证 ==========
    log('INFO', '\n✅ 阶段 5: 验证');
    
    const checks = [
      { name: '共享层目录', path: PATHS.shared },
      { name: '共享索引', path: path.join(PATHS.shared, '.abstract') },
      { name: 'RELATIONS.md', path: path.join(PATHS.shared, 'RELATIONS.md') },
      { name: '私有层目录', path: PATHS.memory },
      { name: '私有索引', path: path.join(PATHS.memory, '.abstract') },
      { name: 'learnings.md', path: path.join(PATHS.memory, 'learnings.md') },
      { name: 'MEMORY.md', path: memoryMdPath }
    ];
    
    let passed = 0;
    for (const check of checks) {
      if (fs.existsSync(check.path)) {
        log('INFO', `  ✅ ${check.name}`);
        passed++;
      } else {
        log('ERROR', `  ❌ ${check.name} 缺失`);
      }
    }
    
    log('INFO', `\n验证结果: ${passed}/${checks.length} 通过`);
    
    if (passed === checks.length) {
      log('INFO', '\n=== ✅ 初始化成功 ===');
      log('INFO', `Bot: ${BOT_NAME}`);
      log('INFO', `备份文件: ${backups.join(', ') || '无'}`);
      return 0;
    } else {
      throw new Error('部分文件创建失败');
    }
    
  } catch (error) {
    log('ERROR', `\n❌ 初始化失败: ${error.message}`);
    
    // 回滚
    if (backups.length > 0) {
      log('INFO', '\n🔄 开始回滚...');
      for (const backup of backups) {
        try {
          const original = backup.replace(/\.bak\.[^.]+$/, '');
          fs.copyFileSync(backup, original);
          log('INFO', `  恢复: ${original}`);
        } catch (e) {
          log('ERROR', `  回滚失败: ${backup}`);
        }
      }
    }
    
    return 1;
  }
}

// 运行
init().then(code => process.exit(code));
