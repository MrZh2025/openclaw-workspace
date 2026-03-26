// Direct script to create Feishu doc and upload file using Lark SDK
const fs = require('fs');
const path = require('path');
const Lark = require('@larksuiteoapi/node-sdk');

async function main() {
  console.log('Starting Feishu document creation...');
  
  // Read the feishu config to get credentials
  const configPath = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'openclaw.json');
  const configContent = fs.readFileSync(configPath, 'utf-8');
  const config = JSON.parse(configContent);
  
  const feishuConfig = config.channels?.feishu;
  if (!feishuConfig?.accounts?.main) {
    console.error('No Feishu account config found');
    return;
  }
  
  const { appId, appSecret } = feishuConfig.accounts.main;
  console.log('Using app:', appId);
  
  // Create Lark client
  const client = new Lark.Client({
    appId,
    appSecret,
  });
  
  // Step 1: Create document
  console.log('\n1. Creating document "分析要求"...');
  const owner_open_id = "ou_18b66a584c9dbbdf8e5b9cf8d371f3e4";
  
  const createRes = await client.docx.document.create({
    data: { 
      title: "分析要求",
      folder_token: undefined 
    },
  });
  
  if (createRes.code !== 0) {
    console.error('Document creation failed:', createRes.msg);
    return;
  }
  
  const docToken = createRes.data?.document?.document_id;
  const docUrl = `https://feishu.cn/docx/${docToken}`;
  console.log('Document created successfully!');
  console.log('Doc Token:', docToken);
  console.log('Doc URL:', docUrl);
  
  // Step 2: Grant permission to owner
  console.log('\n2. Granting permission to owner...');
  try {
    const permRes = await client.drive.permissionMember.create({
      path: { token: docToken },
      params: { type: "docx", need_notification: false },
      data: {
        member_type: "openid",
        member_id: owner_open_id,
        perm: "edit",
      },
    });
    
    if (permRes.code === 0) {
      console.log('Permission granted successfully!');
    } else {
      console.log('Permission grant result:', permRes.msg);
    }
  } catch (err) {
    console.log('Permission grant error (non-fatal):', err.message);
  }
  
  // Step 3: Upload file attachment
  console.log('\n3. Uploading file attachment...');
  const filePath = "C:\\Users\\Mr Zhou\\Desktop\\分析要求.TXT";
  
  if (!fs.existsSync(filePath)) {
    console.error('File not found:', filePath);
    console.log('\n=== RESULT ===');
    console.log('Document URL:', docUrl);
    console.log('File upload: SKIPPED (file not found)');
    return;
  }
  
  const fileBuffer = fs.readFileSync(filePath);
  const fileName = path.basename(filePath);
  console.log('File:', fileName, `(${fileBuffer.length} bytes)`);
  
  // Upload file to Feishu drive
  const uploadRes = await client.drive.media.uploadAll({
    data: {
      file_name: fileName,
      parent_type: "docx_file",
      parent_node: docToken,
      size: fileBuffer.length,
      file: fileBuffer,
    },
  });
  
  if (uploadRes.code !== 0) {
    console.error('File upload failed:', uploadRes.msg);
    console.log('\n=== RESULT ===');
    console.log('Document URL:', docUrl);
    console.log('File upload: FAILED -', uploadRes.msg);
    return;
  }
  
  const fileToken = uploadRes?.file_token;
  console.log('File uploaded successfully!');
  console.log('File Token:', fileToken);
  
  // Note: Feishu API doesn't support direct file block creation
  // The file is uploaded to drive and associated with the doc
  console.log('\n=== RESULT ===');
  console.log('Document URL:', docUrl);
  console.log('File Upload: SUCCESS');
  console.log('File Name:', fileName);
  console.log('File Token:', fileToken);
  console.log('\nNote: File uploaded to drive. To add it as an attachment in the doc,');
  console.log('you may need to manually insert it or use a markdown link.');
}

main().catch(console.error);
