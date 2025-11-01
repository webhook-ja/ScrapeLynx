// background.js

// Store API calls and affiliate data for each tab
const tabData = new Map();

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'AFFILIATE_DATA') {
    // Update tab ID with actual tab ID
    const tabId = sender.tab.id;
    
    // Initialize data structure for this tab if not exists
    if (!tabData.has(tabId)) {
      tabData.set(tabId, {
        affiliate: { ids: [], params: [], urls: [], cookies: [] },
        apis: [],
        lastUpdated: Date.now()
      });
    }
    
    // Update affiliate data
    const currentData = tabData.get(tabId);
    currentData.affiliate = {
      ids: [...new Set([...currentData.affiliate.ids, ...request.data.ids])],
      params: [...new Set([...currentData.affiliate.params, ...request.data.params])],
      urls: [...new Set([...currentData.affiliate.urls, ...request.data.urls])],
      cookies: [...new Set([...currentData.affiliate.cookies, ...request.data.cookies])]
    };
    
    // Update storage
    chrome.storage.local.set({
      [`affiliate_data_${tabId}`]: currentData.affiliate
    });
    
    // Send response back to content script if needed
    sendResponse({status: 'affiliate_data_received'});
  } 
  else if (request.type === 'API_ENDPOINTS') {
    const tabId = sender.tab.id;
    
    // Initialize data structure for this tab if not exists
    if (!tabData.has(tabId)) {
      tabData.set(tabId, {
        affiliate: { ids: [], params: [], urls: [], cookies: [] },
        apis: [],
        lastUpdated: Date.now()
      });
    }
    
    // Update API data
    const currentData = tabData.get(tabId);
    
    // Add new API endpoints
    for (const endpoint of request.data) {
      if (!currentData.apis.some(api => api.url === endpoint)) {
        currentData.apis.push({
          url: endpoint,
          method: 'GET',
          timestamp: Date.now(),
          responseStatus: null
        });
      }
    }
    
    // Update storage
    chrome.storage.local.set({
      [`api_calls_${tabId}`]: currentData.apis
    });
  }
  
  return true; // Required for async sendResponse
});

// Listen for tab updates to clean up data
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'loading') {
    // Reset data for the tab when navigating to a new page
    tabData.set(tabId, {
      affiliate: { ids: [], params: [], urls: [], cookies: [] },
      apis: [],
      lastUpdated: Date.now()
    });
    
    // Clear stored data for this tab
    chrome.storage.local.remove([
      `affiliate_data_${tabId}`,
      `api_calls_${tabId}`
    ]);
  }
});

// Listen for tab removal to clean up data
chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
  tabData.delete(tabId);
  chrome.storage.local.remove([
    `affiliate_data_${tabId}`,
    `api_calls_${tabId}`
  ]);
});

// Handle extension installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('ScrapeLynx Inspector extension installed');
});

// Handle extension startup
chrome.runtime.onStartup.addListener(() => {
  console.log('ScrapeLynx Inspector extension started');
});