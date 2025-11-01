// content.js

// Function to detect affiliate parameters in the current URL
function detectAffiliateParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const affiliateParams = [];
  
  // Common affiliate parameter names
  const affiliateParamNames = [
    'affiliate', 'ref', 'referral', 'campaign', 'utm_source', 'utm_medium', 
    'utm_campaign', 'utm_term', 'utm_content', 'source', 'medium', 'term', 
    'content', 'gclid', 'fbclid', '_x_ads_csite', '_x_ads_channel', 
    '_x_ads_sub_channel', '_x_sessn_id', 'refer_page_name', 'refer_page_id', 
    'refer_page_sn', 'aff_id', 'af_id', 'aff_sub', 'subid', 'click_id',
    'affiliate_id', 'aid', 'pid', 'tid', 'campaign_id', 'ref_id', 'tracking_id'
  ];
  
  for (const [key, value] of urlParams.entries()) {
    if (affiliateParamNames.includes(key.toLowerCase())) {
      affiliateParams.push({ key, value });
    }
  }
  
  return affiliateParams;
}

// Function to get all cookies from the current page
function getAllCookies() {
  const cookies = document.cookie.split(';');
  const cookieList = [];
  
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name) {
      cookieList.push({ name: name.trim(), value: value ? value.trim() : '' });
    }
  }
  
  return cookieList;
}

// Function to detect affiliate IDs in cookies and page data
function detectAffiliateIds(cookies) {
  const affiliateIds = [];
  
  // Check cookies for affiliate IDs
  for (const cookie of cookies) {
    // Look for common patterns in cookie names/values that might contain affiliate IDs
    if (cookie.name.toLowerCase().includes('affiliate') || 
        cookie.name.toLowerCase().includes('referral') ||
        cookie.name.toLowerCase().includes('sessn') ||
        cookie.name.toLowerCase().includes('ads')) {
      affiliateIds.push(cookie.value);
    }
    
    // Look for IDs in values that look like affiliate IDs
    if (cookie.value.length > 8 && /\d+/.test(cookie.value)) {  // Numeric ID-like strings
      affiliateIds.push(cookie.value);
    }
  }
  
  return affiliateIds;
}

// Function to detect affiliate-related URLs in the page
function detectAffiliateUrls() {
  const urls = [];
  
  // Check all links on the page
  const allLinks = document.querySelectorAll('a');
  for (const link of allLinks) {
    if (link.href.includes('_x_ads') || link.href.includes('affiliate') || 
        link.href.includes('utm_') || link.href.includes('referral')) {
      urls.push(link.href);
    }
  }
  
  // Check for any embedded URLs in data attributes
  const elementsWithDataAttrs = document.querySelectorAll('*[data-href], *[data-url], *[data-link]');
  for (const element of elementsWithDataAttrs) {
    const dataHref = element.getAttribute('data-href');
    const dataUrl = element.getAttribute('data-url');
    const dataLink = element.getAttribute('data-link');
    
    [dataHref, dataUrl, dataLink].forEach(attr => {
      if (attr && (attr.includes('_x_ads') || attr.includes('affiliate') || 
                  attr.includes('utm_') || attr.includes('referral'))) {
        urls.push(attr);
      }
    });
  }
  
  // Check for URLs in script tags (sometimes used for tracking)
  const scripts = document.querySelectorAll('script');
  for (const script of scripts) {
    if (script.textContent) {
      // Look for URLs in scripts that might be related to tracking
      const urlRegex = /(https?:\/\/[^\s'"]*(_x_ads|affiliate|utm_|referral)[^\s'"]*)/g;
      const matches = script.textContent.match(urlRegex);
      if (matches) {
        urls.push(...matches);
      }
    }
  }
  
  // Remove duplicates
  return [...new Set(urls)];
}

// Send detected affiliate data to the background script
function sendAffiliateData() {
  const cookies = getAllCookies();
  const affiliateParams = detectAffiliateParams();
  const affiliateIds = detectAffiliateIds(cookies);
  const affiliateUrls = detectAffiliateUrls();
  
  // Send message to background script to store the data
  chrome.runtime.sendMessage({
    type: 'AFFILIATE_DATA',
    data: {
      ids: affiliateIds,
      params: affiliateParams,
      urls: affiliateUrls,
      cookies: cookies,
      timestamp: Date.now()
    },
    tabId: chrome.runtime.id // Will be replaced by the actual tab ID in the background script
  });
}

// Function to intercept network requests for API detection
function interceptNetworkRequests() {
  // This is a simplified approach - in a real extension you might need a different method
  // since content scripts run in the page context and can't directly intercept network requests
  
  // For now, we'll focus on detecting existing elements in the DOM
  // More sophisticated API detection would require background scripts
  const apiEndpoints = [];
  
  // Look for common API patterns in script tags
  const scripts = document.querySelectorAll('script');
  for (const script of scripts) {
    if (script.textContent) {
      // Find API endpoint patterns
      const endpointRegex = /(https?:\/\/[^\s'"]*\/api\/[^\s'"]*)/g;
      const matches = script.textContent.match(endpointRegex);
      if (matches) {
        for (const match of matches) {
          // Filter out non-API endpoints
          if (match.includes('/api/') || match.includes('/graphql')) {
            apiEndpoints.push(match);
          }
        }
      }
    }
  }
  
  // Look for API calls in src/href attributes
  const elements = document.querySelectorAll('*[src*="/api/"], *[href*="/api/"]');
  for (const element of elements) {
    const src = element.getAttribute('src');
    const href = element.getAttribute('href');
    
    [src, href].forEach(url => {
      if (url && (url.includes('/api/') || url.includes('/graphql'))) {
        apiEndpoints.push(url);
      }
    });
  }
  
  chrome.runtime.sendMessage({
    type: 'API_ENDPOINTS',
    data: apiEndpoints,
    tabId: chrome.runtime.id // Will be replaced by the actual tab ID in the background script
  });
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'REQUEST_AFFILIATE_DATA') {
    sendAffiliateData();
  } else if (request.type === 'REQUEST_API_DATA') {
    interceptNetworkRequests();
  } else if (request.type === 'REQUEST_COOKIES') {
    sendResponse(getAllCookies());
  }
});

// Run the detection when the page loads
window.addEventListener('load', () => {
  sendAffiliateData();
  interceptNetworkRequests();
});

// Also run periodically to catch dynamically loaded content
setInterval(() => {
  sendAffiliateData();
  interceptNetworkRequests();
}, 5000); // Every 5 seconds