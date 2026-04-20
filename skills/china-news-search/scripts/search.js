#!/usr/bin/env node
/**
 * 国内新闻搜索 - 使用 Tavily API 搜索中文新闻
 */

const https = require('https');

// 国内新闻域名列表
const CHINA_DOMAINS = [
  'sina.com.cn',
  '163.com',
  'sohu.com',
  'qq.com',
  'ifeng.com',
  'people.com.cn',
  'xinhuanet.com',
  'china.com',
  'huanqiu.com',
  'guancha.cn'
];

// 从环境变量或配置文件获取 API Key
function getApiKey() {
  // 优先从环境变量获取
  if (process.env.TAVILY_API_KEY) {
    return process.env.TAVILY_API_KEY;
  }
  
  // 默认 key
  return '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';
}

// 搜索函数
async function searchChinaNews(query, options = {}) {
  const count = options.count || 5;
  const days = options.days || 1;
  
  const postData = JSON.stringify({
    api_key: getApiKey(),
    query: query,
    search_depth: 'advanced',
    max_results: count,
    time_range: days === 1 ? 'day' : days === 7 ? 'week' : 'month',
    include_domains: CHINA_DOMAINS
  });

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'api.tavily.com',
      path: '/search',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (e) {
          reject(new Error('解析失败: ' + e.message));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// 格式化输出
function formatResults(result) {
  if (!result.results || result.results.length === 0) {
    return '未找到相关新闻';
  }

  let output = `🇨🇳 国内新闻搜索结果 (${result.results.length}条)\n`;
  output += '='.repeat(50) + '\n\n';

  result.results.forEach((item, index) => {
    output += `${index + 1}. ${item.title}\n`;
    output += `   📰 ${item.url}\n`;
    if (item.content) {
      const summary = item.content.substring(0, 120).replace(/\n/g, ' ');
      output += `   📝 ${summary}...\n`;
    }
    output += '\n';
  });

  return output;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(`
🇨🇳 国内新闻搜索

用法:
  node search.mjs "关键词"
  node search.mjs "关键词" -n 10
  node search.mjs "关键词" -d 7

选项:
  -n, --number  结果数量 (默认: 5)
  -d, --days    时间范围，天数 (默认: 1)
  -h, --help    显示帮助

示例:
  node search.mjs "AI新闻"
  node search.mjs "人工智能" -n 10 -d 3
`);
    return;
  }

  const query = args[0];
  let count = 5;
  let days = 1;

  // 解析参数
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '-n' || args[i] === '--number') {
      count = parseInt(args[i + 1]) || 5;
      i++;
    } else if (args[i] === '-d' || args[i] === '--days') {
      days = parseInt(args[i + 1]) || 1;
      i++;
    }
  }

  console.log(`🔍 搜索: "${query}"`);
  console.log(`📊 数量: ${count}条, 时间: ${days}天内\n`);

  try {
    const result = await searchChinaNews(query, { count, days });
    console.log(formatResults(result));
  } catch (error) {
    console.error('❌ 搜索失败:', error.message);
    process.exit(1);
  }
}

main();
