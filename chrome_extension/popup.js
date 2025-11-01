// popup.js

// Switch between tabs in the popup
function switchTab(tabName) {
  // Hide all content divs
  document.querySelectorAll('.content').forEach(content => {
    content.classList.remove('active');
  });
  
  // Remove active class from all tabs
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.remove('active');
  });
  
  // Show selected content and mark tab as active
  document.getElementById(`${tabName}-content`).classList.add('active');
  event.target.classList.add('active');
  
  // Load content for the selected tab
  if (tabName === 'cookies') {
    loadCookies();
  } else if (tabName === 'apis') {
    loadAPIs();
  } else if (tabName === 'affiliates') {
    loadAffiliateData();
  }
}

// Load cookies from the active tab
async function loadCookies() {
  try {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    const cookies = await chrome.cookies.getAll({url: tab.url});
    
    const cookiesList = document.getElementById('cookies-list');
    cookiesList.innerHTML = '';
    
    if (cookies.length === 0) {
      cookiesList.innerHTML = '<p>No cookies found for this site</p>';
      return;
    }
    
    const cookiesContainer = document.createElement('div');
    
    cookies.forEach(cookie => {
      const cookieDiv = document.createElement('div');
      cookieDiv.className = 'cookie-item';
      
      // Check if cookie might be related to affiliate tracking
      const isAffiliateCookie = isAffiliateRelated(cookie.name);
      if (isAffiliateCookie) {
        cookieDiv.classList.add('highlight');
      }
      
      cookieDiv.innerHTML = `
        <div class="cookie-name">${cookie.name}</div>
        <div class="cookie-value">${cookie.value}</div>
        <div><strong>Domain:</strong> ${cookie.domain}</div>
        <div><strong>Path:</strong> ${cookie.path}</div>
        <div><strong>Expires:</strong> ${cookie.expirationDate ? new Date(cookie.expirationDate * 1000).toLocaleString() : 'Session'}</div>
        <div><strong>Secure:</strong> ${cookie.secure ? 'Yes' : 'No'}</div>
      `;
      
      cookiesContainer.appendChild(cookieDiv);
    });
    
    cookiesList.appendChild(cookiesContainer);
  } catch (error) {
    console.error('Error loading cookies:', error);
    document.getElementById('cookies-list').innerHTML = `<p>Error loading cookies: ${error.message}</p>`;
  }
}

// Load API calls from the active tab
async function loadAPIs() {
  try {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    
    // Get stored API calls for this tab
    const result = await chrome.storage.local.get(`api_calls_${tab.id}`);
    const apiCalls = result[`api_calls_${tab.id}`] || [];
    
    const apisList = document.getElementById('apis-list');
    apisList.innerHTML = '';
    
    if (apiCalls.length === 0) {
      apisList.innerHTML = '<p>No API calls detected yet. Navigate around the website to see API requests.</p>';
      return;
    }
    
    const apisContainer = document.createElement('div');
    
    apiCalls.forEach((apiCall, index) => {
      const apiDiv = document.createElement('div');
      apiDiv.className = 'api-item';
      
      apiDiv.innerHTML = `
        <div class="api-name">${apiCall.method} ${apiCall.url}</div>
        <div class="api-details">
          <strong>Timestamp:</strong> ${new Date(apiCall.timestamp).toLocaleString()}<br>
          <strong>Response Status:</strong> ${apiCall.responseStatus || 'N/A'}<br>
          <strong>Headers:</strong> ${JSON.stringify(apiCall.headers || {})}<br>
          <strong>Payload:</strong> ${JSON.stringify(apiCall.payload || {})}
        </div>
      `;
      
      apisContainer.appendChild(apiDiv);
    });
    
    apisList.appendChild(apisContainer);
  } catch (error) {
    console.error('Error loading API calls:', error);
    document.getElementById('apis-list').innerHTML = `<p>Error loading API calls: ${error.message}</p>`;
  }
}

// Load affiliate-related data
async function loadAffiliateData() {
  try {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    
    // Get stored affiliate data for this tab
    const result = await chrome.storage.local.get(`affiliate_data_${tab.id}`);
    const affiliateData = result[`affiliate_data_${tab.id}`] || { ids: [], params: [], urls: [] };
    
    const affiliatesList = document.getElementById('affiliates-list');
    affiliatesList.innerHTML = '';
    
    const affiliatesContainer = document.createElement('div');
    
    // Add affiliate IDs
    if (affiliateData.ids.length > 0) {
      const idsDiv = document.createElement('div');
      idsDiv.innerHTML = `<strong>Affiliate IDs found:</strong>`;
      affiliateData.ids.forEach(id => {
        const idDiv = document.createElement('div');
        idDiv.innerHTML = `<span class="highlight">${id}</span>`;
        idsDiv.appendChild(idDiv);
      });
      affiliatesContainer.appendChild(idsDiv);
      affiliatesContainer.appendChild(document.createElement('br'));
    }
    
    // Add affiliate parameters
    if (affiliateData.params.length > 0) {
      const paramsDiv = document.createElement('div');
      paramsDiv.innerHTML = `<strong>Affiliate Parameters found:</strong>`;
      affiliateData.params.forEach(param => {
        const paramDiv = document.createElement('div');
        paramDiv.innerHTML = `<span class="highlight">${param.key}=${param.value}</span>`;
        paramsDiv.appendChild(paramDiv);
      });
      affiliatesContainer.appendChild(paramsDiv);
      affiliatesContainer.appendChild(document.createElement('br'));
    }
    
    // Add affiliate-related URLs
    if (affiliateData.urls.length > 0) {
      const urlsDiv = document.createElement('div');
      urlsDiv.innerHTML = `<strong>Affiliate-related URLs found:</strong>`;
      affiliateData.urls.forEach(url => {
        const urlDiv = document.createElement('div');
        urlDiv.innerHTML = `<span class="highlight">${url}</span>`;
        urlsDiv.appendChild(urlDiv);
      });
      affiliatesContainer.appendChild(urlsDiv);
    }
    
    if (affiliateData.ids.length === 0 && affiliateData.params.length === 0 && affiliateData.urls.length === 0) {
      affiliatesList.innerHTML = '<p>No affiliate data detected. Browse to affiliate pages to see data.</p>';
      return;
    }
    
    affiliatesList.appendChild(affiliatesContainer);
  } catch (error) {
    console.error('Error loading affiliate data:', error);
    document.getElementById('affiliates-list').innerHTML = `<p>Error loading affiliate data: ${error.message}</p>`;
  }
}

// Check if a cookie name is related to affiliate tracking
function isAffiliateRelated(cookieName) {
  const affiliateKeywords = [
    'affiliate', 'referral', 'campaign', 'source', 'medium', 'term', 'content',
    'sessn', 'ads', 'tracking', 'utm', 'gclid', 'session', 'visit'
  ];
  
  return affiliateKeywords.some(keyword => 
    cookieName.toLowerCase().includes(keyword)
  );
}

// Initialize popup when loaded
document.addEventListener('DOMContentLoaded', async () => {
  // Load initial cookies tab
  await loadCookies();
  
  // Add event listener to refresh button
  document.addEventListener('click', async (e) => {
    if (e.target.id === 'refresh-btn') {
      const activeTab = document.querySelector('.tab.active').textContent.toLowerCase();
      switch (activeTab) {
        case 'cookies':
          await loadCookies();
          break;
        case 'apis':
          await loadAPIs();
          break;
        case 'affiliates':
          await loadAffiliateData();
          break;
      }
    }
  });
});