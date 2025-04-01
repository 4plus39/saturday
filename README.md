# 專案名稱

## 📌 介紹
這是一個部署在 **Azure** 的專案，使用 **自訂域名**，並且串接 **中央氣象局 API** 來獲取即時天氣資訊。

## 🔧 技術架構
- **雲端平台**：Azure Web App
- **後端框架**：Django
- **前端框架**：Tailwind CSS
- **資料來源**：中央氣象局 API
- **安全性**：API Key 隱藏處理
- **CD/CI**：GitHub Actions

## 🚀 部署方式
1. **設定 Azure Web App**
   ```sh
   az webapp create --resource-group my-resource-group --plan my-app-plan --name my-app-name
   ```
   
📜 API 使用
請參考官方中央氣象局 API 文件：[連結](https://opendata.cwa.gov.tw/)

📌 環境變數設定
在 .env 或 Azure App Settings 設定：
```sh
CWA_API_KEY=your_api_key
```

# 啟動開發環境
```sh
python manage.py runserver
```

🎯 其他
