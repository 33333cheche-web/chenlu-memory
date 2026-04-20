#!/usr/bin/env node
/**
 * capture.js - 实时捕获对话关键信息
 * 
 * 安全原则：
 * 1. try-catch 包裹所有操作
 * 2. 错误不影响主流程
 * 3. 日志记录便于排查
 * 
 * 用法：node capture.js --bot=baby "对话摘要内容"
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const BOT_NAME = process.argv.find(arg => arg.startsWith('--bot='))?.split('=')[1] || 'baby';
const CONTENT = process.argv.find((arg, index) => index > 1 && !arg.startsWith('--')) || '';
const HOME = os.homedir();

// 路径
const PATHS = {
  daily: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory', 'daily'),
  privateAbstract: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory', '.abstract'),
  sharedLog: path.join(HOME, '.openclaw', 'shared-memory', 'cross-agent-log.md')
};

// 日志
function log(level, message) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [${level}] ${message}`);
}

// 确保目录存在
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  }
}

// 获取今天日期
function getToday() {
  return new Date().toISOString().split('T')[0];
}

// 获取当前时间
function getNow() {
  return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
}

// 写入 daily log (v3.0 格式)
function writeDailyLog(content) {
  try {
    const today = getToday();
    const dailyPath = path.join(PATHS.daily, `${today}.md`);
    
    ensureDir(PATHS.daily);
    
    // 自动判断优先级
    const p0Keywords = ['完成', '部署', '修复', '上线', '通过', '验收'];
    const p2Keywords = ['测试', '对话', '闲聊', '确认', '今日无需要记录的事件', '无事件'];
    let priority = '#P1';
    if (p0Keywords.some(kw => content.includes(kw))) priority = '#P0';
    else if (p2Keywords.some(kw => content.includes(kw))) priority = '#P2';
    
    const entry = `${priority} ${content}\n`;
    
    fs.appendFileSync(dailyPath, entry);
    log('INFO', `已记录到 daily log: ${dailyPath}`);
    return true;
  } catch (error) {
    log('ERROR', `写入 daily log 失败: ${error.message}`);
    return false;
  }
}

// 更新私有索引
function updatePrivateAbstract(content) {
  try {
    if (!fs.existsSync(PATHS.privateAbstract)) {
      log('WARN', '私有索引不存在，跳过更新');
      return false;
    }
    
    // 简单更新最近记录部分
    let abstract = fs.readFileSync(PATHS.privateAbstract, 'utf-8');
    const today = getToday();
    const time = getNow();
    
    // 检查是否已有今日记录
    if (!abstract.includes(`- ${today}:`)) {
      // 在"最近更新"部分添加
      const updateLine = `- ${today} ${time}: ${content.substring(0, 50)}${content.length > 50 ? '...' : ''}`;
      
      // 找到"最近更新"部分并添加
      const lines = abstract.split('\n');
      const updateIndex = lines.findIndex(line => line.includes('## 最近更新'));
      if (updateIndex >= 0) {
        lines.splice(updateIndex + 1, 0, updateLine);
        abstract = lines.join('\n');
        fs.writeFileSync(PATHS.privateAbstract, abstract);
        log('INFO', '已更新私有索引');
        return true;
      }
    }
    return false;
  } catch (error) {
    log('ERROR', `更新私有索引失败: ${error.message}`);
    return false;
  }
}

// 写入跨 Bot 日志（重要事件）
function writeCrossAgentLog(content) {
  try {
    // 只记录重要事件（简单判断：长度>20 或包含关键词）
    const importantKeywords = ['完成', '部署', '修复', '错误', '教训', '关键'];
    const isImportant = content.length > 20 || importantKeywords.some(kw => content.includes(kw));
    
    if (!isImportant) {
      return false;
    }
    
    if (!fs.existsSync(PATHS.sharedLog)) {
      log('WARN', '跨Bot日志不存在，跳过');
      return false;
    }
    
    const today = getToday();
    const time = getNow();
    const entry = `- ${today} ${time} ${BOT_NAME}: ${content.substring(0, 80)}${content.length > 80 ? '...' : ''}\n`;
    
    fs.appendFileSync(PATHS.sharedLog, entry);
    log('INFO', '已记录到跨Bot日志');
    return true;
  } catch (error) {
    log('ERROR', `写入跨Bot日志失败: ${error.message}`);
    return false;
  }
}

// 主函数
function capture() {
  log('INFO', `=== Capture for ${BOT_NAME} ===`);
  
  if (!CONTENT) {
    log('WARN', '没有提供内容，跳过');
    return 0;
  }
  
  try {
    // 1. 写入 daily log
    writeDailyLog(CONTENT);
    
    // 2. 更新私有索引
    updatePrivateAbstract(CONTENT);
    
    // 3. 写入跨Bot日志（如果是重要事件）
    writeCrossAgentLog(CONTENT);
    
    log('INFO', '✅ 捕获完成');
    return 0;
    
  } catch (error) {
    log('ERROR', `捕获失败: ${error.message}`);
    // 不中断主流程，返回 0
    return 0;
  }
}

// 运行
capture();
process.exit(0);
