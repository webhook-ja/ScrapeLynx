// TEMU SCRAPER FRONTEND - JavaScript

const API_URL = 'http://localhost:8000';

// Elements
const searchForm = document.getElementById('searchForm');
const searchButton = document.getElementById('searchButton');
const loading = document.getElementById('loading');
const stats = document.getElementById('stats');
const results = document.getElementById('results');
const noResults = document.getElementById('noResults');

// Event Listeners
searchForm.addEventListener('submit', handleSearch);

// Main Search Handler
async function handleSearch(e) {
    e.preventDefault();

    // Get form values
    const formData = {
        search_query: document.getElementById('searchQuery').value.trim(),
        max_products: parseInt(document.getElementById('maxProducts').value),
        min_rating: parseFloat(document.getElementById('minRating').value),
        min_reviews: parseInt(document.getElementById('minReviews').value),
        min_sales: parseInt(document.getElementById('minSales').value),
        price_min: parseFloat(document.getElementById('priceMin').value),
        price_max: parseFloat(document.getElementById('priceMax').value)
    };

    // Validate
    if (!formData.search_query) {
        alert('Por favor ingresa un término de búsqueda');
        return;
    }

    // Show loading
    showLoading();

    try {
        // Call API
        const response = await fetch(`${API_URL}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Hide loading
        hideLoading();

        // Display results
        if (data.success && data.results.products && data.results.products.length > 0) {
            displayResults(data.results);
        } else {
            showNoResults();
        }

    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        alert(`Error al realizar la búsqueda: ${error.message}`);
    }
}

// Display Results
function displayResults(data) {
    const products = data.products || [];

    // Show stats
    displayStats(data, products);

    // Clear previous results
    results.innerHTML = '';
    noResults.classList.add('hidden');

    // Create product cards
    products.forEach(product => {
        const card = createProductCard(product);
        results.appendChild(card);
    });

    // Smooth scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display Stats
function displayStats(data, products) {
    // Calculate stats
    const totalFound = data.total_found || 0;
    const totalFiltered = products.length;

    const avgRating = products.length > 0
        ? (products.reduce((sum, p) => sum + (p.rating || 0), 0) / products.length).toFixed(1)
        : 0;

    const avgPrice = products.length > 0
        ? (products.reduce((sum, p) => sum + (p.price || 0), 0) / products.length).toFixed(2)
        : 0;

    // Update DOM
    document.getElementById('statTotal').textContent = totalFound;
    document.getElementById('statFiltered').textContent = totalFiltered;
    document.getElementById('statAvgRating').textContent = avgRating;
    document.getElementById('statAvgPrice').textContent = `$${avgPrice}`;

    stats.classList.remove('hidden');
}

// Create Product Card
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'bg-gray-800 rounded-lg shadow-xl overflow-hidden hover:shadow-2xl transition duration-300 flex flex-col';

    // Calculate discount
    const hasDiscount = product.original_price && product.original_price > product.price;
    const discountBadge = hasDiscount
        ? `<span class="bg-red-500 text-white px-2 py-1 rounded text-xs font-bold">-${product.discount_percentage || Math.round(((product.original_price - product.price) / product.original_price) * 100)}%</span>`
        : '';

    card.innerHTML = `
        <!-- Image -->
        <div class="relative bg-gray-700 h-48 overflow-hidden">
            ${product.image_url
                ? `<img src="${product.image_url}" alt="${product.title}" class="w-full h-full object-cover hover:scale-110 transition duration-300">`
                : '<div class="w-full h-full flex items-center justify-center"><i class="fas fa-image text-6xl text-gray-600"></i></div>'
            }
            ${discountBadge ? `<div class="absolute top-2 right-2">${discountBadge}</div>` : ''}
        </div>

        <!-- Content -->
        <div class="p-4 flex-grow flex flex-col">
            <!-- Title -->
            <h3 class="font-bold text-sm mb-2 line-clamp-2 flex-grow">${product.title || 'Sin título'}</h3>

            <!-- Price -->
            <div class="mb-3">
                <div class="flex items-baseline space-x-2">
                    <span class="text-2xl font-bold text-green-400">$${(product.price || 0).toFixed(2)}</span>
                    ${hasDiscount
                        ? `<span class="text-sm text-gray-500 line-through">$${product.original_price.toFixed(2)}</span>`
                        : ''
                    }
                </div>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-2 gap-2 mb-3 text-xs">
                ${product.rating
                    ? `<div class="flex items-center space-x-1">
                        <i class="fas fa-star text-yellow-400"></i>
                        <span>${product.rating.toFixed(1)}</span>
                      </div>`
                    : '<div></div>'
                }
                ${product.reviews_count
                    ? `<div class="flex items-center space-x-1">
                        <i class="fas fa-comment text-blue-400"></i>
                        <span>${formatNumber(product.reviews_count)}</span>
                      </div>`
                    : '<div></div>'
                }
                ${product.sales_count
                    ? `<div class="flex items-center space-x-1 col-span-2">
                        <i class="fas fa-shopping-cart text-purple-400"></i>
                        <span>${formatNumber(product.sales_count)} ventas</span>
                      </div>`
                    : ''
                }
            </div>

            <!-- Buttons -->
            <div class="space-y-2">
                <!-- Affiliate Link -->
                ${product.affiliate_link
                    ? `<a href="${product.affiliate_link}" target="_blank" class="block w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white text-center py-2 px-4 rounded-lg transition duration-200 text-sm font-bold">
                        <i class="fas fa-external-link-alt mr-2"></i>Ver en Temu
                      </a>`
                    : ''
                }

                <!-- Copy Link -->
                <button
                    onclick="copyLink('${product.affiliate_link || product.product_url}')"
                    class="w-full bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-lg transition duration-200 text-sm"
                >
                    <i class="fas fa-copy mr-2"></i>Copiar Link
                </button>
            </div>
        </div>
    `;

    return card;
}

// Utility Functions
function showLoading() {
    loading.classList.remove('hidden');
    stats.classList.add('hidden');
    results.innerHTML = '';
    noResults.classList.add('hidden');
    searchButton.disabled = true;
    searchButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Scrapeando...';
}

function hideLoading() {
    loading.classList.add('hidden');
    searchButton.disabled = false;
    searchButton.innerHTML = '<i class="fas fa-search mr-2"></i>Buscar Productos';
}

function showNoResults() {
    stats.classList.add('hidden');
    results.innerHTML = '';
    noResults.classList.remove('hidden');
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function copyLink(link) {
    navigator.clipboard.writeText(link).then(() => {
        // Show toast notification
        showToast('Link copiado al portapapeles! 📋');
    }).catch(err => {
        console.error('Error copying:', err);
        alert('Error al copiar el link');
    });
}

function showToast(message) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-bounce';
    toast.innerHTML = `<i class="fas fa-check-circle mr-2"></i>${message}`;

    document.body.appendChild(toast);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Temu Scraper Frontend initialized');
});
