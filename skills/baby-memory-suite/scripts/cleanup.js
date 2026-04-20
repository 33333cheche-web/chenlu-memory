#!/usr/bin/env node
/**
 * cleanup.js - 生命周期管理，自动归档和清理
 * 
 * 安全原则：
 * 1. 先归档，后删除
 * 2. 保留30天可恢复
 * 3. 试运行模式验证后再执行
 * 
 * 用法：
 *   node cleanup.js --bot=baby --dry-run    # 试运行
 *   node cleanup.js --bot=baby              # 正式执行
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const BOT_NAME = process.argv.find(arg => arg.startsWith('--bot='))?.split('=')[1] || 'baby';
const DRY_RUN = process.argv.includes('--dry-run');
const HOME = os.homedir();

// 配置
const CONFIG = {
  p1_archive_days: 90,    // P1: 90天后归档
  p2_cleanup_days: 30,    // P2: 30天后删除
  archive_retention_days: 365  // 归档保留1年
};

// 路径
const PATHS = {
  daily: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory', 'daily'),
  archive: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory', 'archive'),
  privateAbstract: path.join(HOME, '.openclaw', `workspace-${BOT_NAME}`, 'memory', '.abstract')
};

// 日志
function log(level, message) {
  const timestamp = new Date().toISOString();
  const prefix = DRY_RUN ? '[试运行]' : '';
  console.log(`[${timestamp}] [${level}] ${prefix} ${message}`);
}

// 获取文件年龄（天）
function getFileAgeDays(filePath) {
  try {
    const stat = fs.statSync(filePath);
    const now = new Date();
    const mtime = new Date(stat.mtime);
    return Math.floor((now - mtime) / (1000 * 60 * 60 * 24));
  } catch (error) {
    return -1;
  }
}

// 解析文件名中的日期
function parseDateFromFilename(filename) {
  const match = filename.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (match) {
    return new Date(`${match[1]}-${match[2]}-${match[3]}`);
  }
  return null;
}

// 清理 daily 目录
function cleanupDaily() {
  log('INFO', '\n📁 清理 daily 目录...');
  
  if (!fs.existsSync(PATHS.daily)) {
    log('WARN', 'daily 目录不存在');
    return { archived: 0, deleted: 0 };
  }
  
  const files = fs.readdirSync(PATHS.daily).filter(f => f.endsWith('.md'));
  let archived = 0;
  let deleted = 0;
  
  // 确保 archive 目录存在
  if (!fs.existsSync(PATHS.archive)) {
    if (!DRY_RUN) {
      fs.mkdirSync(PATHS.archive, { recursive: true, mode: 0o700 });
    }
    log('INFO', '创建 archive 目录');
  }
  
  for (const file of files) {
    const filePath = path.join(PATHS.daily, file);
    const age = getFileAgeDays(filePath);
    
    if (age < 0) {
      log('WARN', `无法获取文件年龄: ${file}`);
      continue;
    }
    
    // 先判断 P1: 90天归档（必须在前面，否则会被 P2 覆盖）
    if (age > CONFIG.p1_archive_days) {
      const archiveFile = path.join(PATHS.archive, file);
      if (DRY_RUN) {
        log('INFO', `[将归档] ${file} (${age}天)`);
      } else {
        try {
          fs.renameSync(filePath, archiveFile);
          log('INFO', `📦 归档: ${file} (${age}天)`);
          archived++;
        } catch (error) {
          log('ERROR', `归档失败: ${file} - ${error.message}`);
        }
      }
    }
    // 再判断 P2: 30天删除（30-90天之间的）
    else if (age > CONFIG.p2_cleanup_days) {
      if (DRY_RUN) {
        log('INFO', `[将删除] ${file} (${age}天)`);
      } else {
        try {
          fs.unlinkSync(filePath);
          log('INFO', `🗑️  删除: ${file} (${age}天)`);
          deleted++;
        } catch (error) {
          log('ERROR', `删除失败: ${file} - ${error.message}`);
        }
      }
    }
  }
  
  return { archived, deleted };
}

// 清理归档目录（超过1年的删除）
function cleanupArchive() {
  log('INFO', '\n📁 清理 archive 目录...');
  
  if (!fs.existsSync(PATHS.archive)) {
    log('INFO', 'archive 目录不存在，跳过');
    return 0;
  }
  
  const files = fs.readdirSync(PATHS.archive).filter(f => f.endsWith('.md'));
  let deleted = 0;
  
  for (const file of files) {
    const filePath = path.join(PATHS.archive, file);
    const age = getFileAgeDays(filePath);
    
    if (age > CONFIG.archive_retention_days) {
      if (DRY_RUN) {
        log('INFO', `[将删除归档] ${file} (${age}天)`);
      } else {
        try {
          fs.unlinkSync(filePath);
          log('INFO', `🗑️  删除旧归档: ${file} (${age}天)`);
          deleted++;
        } catch (error) {
          log('ERROR', `删除归档失败: ${file}`);
        }
      }
    }
  }
  
  return deleted;
}

// 重构私有索引
function rebuildAbstract() {
  log('INFO', '\n📝 重构私有索引...');
  
  if (!fs.existsSync(PATHS.privateAbstract)) {
    log('WARN', '私有索引不存在，跳过');
    return false;
  }
  
  try {
    let abstract = fs.readFileSync(PATHS.privateAbstract, 'utf-8');
    const today = new Date().toISOString().split('T')[0];
    
    // 更新"最近更新"时间
    abstract = abstract.replace(
      /## 最近更新\n([\s\S]*?)(?=\n## |$)/,
      `## 最近更新\n- ${today}: 系统自动清理\n`
    );
    
    if (!DRY_RUN) {
      fs.writeFileSync(PATHS.privateAbstract, abstract);
    }
    log('INFO', '已更新索引时间戳');
    return true;
  } catch (error) {
    log('ERROR', `重构索引失败: ${error.message}`);
    return false;
  }
}

// 生成统计报告
function generateReport(stats) {
  log('INFO', '\n📊 清理统计报告');
  log('INFO', `归档: ${stats.archived} 个文件`);
  log('INFO', `删除: ${stats.deleted} 个文件`);
  log('INFO', `删除旧归档: ${stats.oldArchived} 个文件`);
  log('INFO', `模式: ${DRY_RUN ? '试运行（未实际执行）' : '正式执行'}`);
}

// 主函数
function cleanup() {
  log('INFO', `=== Cleanup for ${BOT_NAME} ===`);
  log('INFO', `模式: ${DRY_RUN ? '试运行' : '正式执行'}`);
  
  try {
    // 1. 清理 daily
    const dailyStats = cleanupDaily();
    
    // 2. 清理 archive
    const oldArchived = cleanupArchive();
    
    // 3. 重构索引
    rebuildAbstract();
    
    // 4. 生成报告
    generateReport({
      archived: dailyStats.archived,
      deleted: dailyStats.deleted,
      oldArchived
    });
    
    log('INFO', '\n=== ✅ 清理完成 ===');
    return 0;
    
  } catch (error) {
    log('ERROR', `\n❌ 清理失败: ${error.message}`);
    return 1;
  }
}

// 运行
cleanup();
