$body = @{
    app_id = "cli_a924e0ab83b85bd3"
    app_secret = "8P1m3oIQ9oEnonKB43N2ycX7cnzNgSM2"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" -Method Post -Body $body -ContentType "application/json"

$response | ConvertTo-Json
