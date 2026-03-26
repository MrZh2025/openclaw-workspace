// Direct script to create Feishu doc and upload file
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Starting Feishu document creation...');
  
  // Read the feishu config to get credentials
  const configPath = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'openclaw.json');
  let config;
  try {
    const configContent = fs.readFileSync(configPath, 'utf-8');
    config = JSON.parse(configContent);
    console.log('Config loaded from:', configPath);
  } catch (err) {
    console.error('Failed to load config:', err.message);
    return;
  }
  
  console.log('Config keys:', Object.keys(config.channels?.feishu || {}));
  
  // Get Feishu app credentials
  const feishuConfig = config.channels?.feishu;
  if (!feishuConfig) {
    console.error('No Feishu config found');
    return;
  }
  
  console.log('Feishu config:', JSON.stringify(feishuConfig, null, 2));
}

main().catch(console.error);
