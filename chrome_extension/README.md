# 🦁 ScrapeLynx Cookie & API Inspector

A Chrome extension to detect cookies, affiliate IDs, API endpoints, and tracking parameters on websites.

## ✨ Features

- 🔍 **Cookie Detection**: View all cookies from the current website
- 🏷️ **Affiliate ID Detection**: Identify affiliate tracking parameters, IDs, and URLs
- 🌐 **API Endpoint Detection**: Discover API endpoints used by the website
- 📊 **Real-time Monitoring**: Continuously scans for new data as you browse
- 🚀 **Easy Access**: Simple popup interface for quick inspection

## 🛠️ How to Install

### Method 1: Chrome Developer Mode

1. Open Chrome and navigate to `chrome://extensions`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome_extension` folder from this project

### Method 2: Build Package (Future)

In the future, we can add a build script to package the extension as a .crx file.

## 📖 How to Use

1. Install the extension using the steps above
2. Navigate to any website you want to inspect
3. Click the extension icon in the Chrome toolbar
4. View cookies, affiliate data, or API endpoints in the popup

### Tabs Explained

- **Cookies**: Shows all cookies from the current domain
  - Highlights potential affiliate/tracking cookies
  - Displays cookie details (domain, path, expiration, etc.)

- **APIs**: Shows discovered API endpoints
  - Tracks API calls made by the website
  - Shows request details when possible

- **Affiliates**: Shows affiliate-related data
  - Affiliate parameters in URLs
  - Potential affiliate IDs
  - Affiliate-related links found on the page

## 🧠 Detection Patterns

The extension looks for common affiliate patterns including:

### URL Parameters
- `utm_*` parameters (utm_source, utm_medium, utm_campaign, etc.)
- `_x_ads_*` parameters (Temu's affiliate parameters)
- `affiliate`, `ref`, `referral`, `campaign` parameters
- Tracking IDs in URL parameters

### Cookie Patterns
- Cookies with names containing "affiliate", "tracking", "sessn", "ads"
- Long numeric strings that might be session IDs
- Third-party tracking cookies

### API Endpoints
- Endpoints containing "/api/" or "/graphql"
- Tracking and analytics endpoints
- Affiliate-related API calls

## ⚠️ Privacy & Security

- This extension only inspects data in the active tab
- No data is sent to external servers
- All data is stored locally in your browser
- Requires minimal permissions necessary for functionality

## 🤝 Contributing

We welcome contributions to improve the detection capabilities:

1. Add more affiliate parameter patterns
2. Improve API endpoint detection
3. Add support for additional tracking systems
4. Enhance the popup UI/UX

## 📁 Project Structure

```
chrome_extension/
├── manifest.json          # Extension configuration
├── popup.html             # Popup UI
├── popup.js               # Popup logic
├── content.js             # Content script (runs on web pages)
├── background.js          # Background script (persistent functionality)
├── icons/                 # Extension icons
└── README.md              # This file
```

## 🎯 Use Cases

- **Affiliate Marketing**: Understand how affiliate programs work
- **Web Scraping**: Identify tracking mechanisms to avoid detection
- **Privacy**: See what tracking is happening on websites
- **Development**: Debug API calls and tracking implementations

## 🚀 Next Steps

- Add more sophisticated network request interception
- Implement export functionality for inspection results
- Add support for more affiliate networks
- Create visual representations of tracking flows