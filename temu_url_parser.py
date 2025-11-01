"""
Temu Affiliate Link Parser and Generator

This script can extract product information from Temu URLs
and generate affiliate links.
"""

import re
from urllib.parse import urlparse, parse_qs, urlunparse

def extract_product_id_from_url(url):
    """
    Extract product ID from Temu URL
    """
    # Parse the URL
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    
    # Look for product ID in path
    # Temu URLs typically have product IDs in the path like:
    # /es/product-title-1234567890.html
    for part in path_parts:
        if part.endswith('.html'):
            # Extract numeric ID from the end of the path part
            match = re.search(r'g-(\d+)\.html$', part)
            if match:
                return match.group(1)
            
            # Alternative pattern: just numbers at the end before .html
            match = re.search(r'(\d+)\.html$', part)
            if match:
                return match.group(1)
    
    # If not found in path, try to extract from URL parameters
    query_params = parse_qs(parsed_url.query)
    if 'goods_id' in query_params:
        return query_params['goods_id'][0]
    
    # Looking for the ID in the path segments in different formats
    # Common pattern: /.../product-1234567890.html
    for i, segment in enumerate(path_parts):
        if '-' in segment and segment.endswith('.html'):
            # Split by hyphens and look for numeric values
            parts = segment.split('-')
            for part in reversed(parts):  # Start from the end
                if part.endswith('.html'):
                    part = part.replace('.html', '')
                if part.isdigit() and len(part) >= 8:  # Temu IDs are typically long
                    return part
    
    return None

def generate_affiliate_link(product_url, affiliate_id):
    """
    Generate affiliate link for Temu product
    """
    # Parse the original URL
    parsed_url = urlparse(product_url)
    
    # Extract the base URL and path
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    
    # Parse the original query parameters
    query_params = parse_qs(parsed_url.query)
    
    # Update or add affiliate parameters
    query_params['_x_ads_csite'] = ['affiliate_seo']
    query_params['_x_ads_channel'] = ['affiliate']
    query_params['_x_sessn_id'] = ['auto_generated']  # This might need to be dynamic
    
    # Reconstruct the query string
    new_query = []
    for key, values in query_params.items():
        for value in values:
            new_query.append(f"{key}={value}")
    
    affiliate_link = f"{base_url}?{'&'.join(new_query)}"
    
    # If the affiliate ID should be added as a separate parameter
    if '_x_ads_sub_channel' not in query_params:
        affiliate_link += f"&_x_ads_sub_channel={affiliate_id}"
    
    return affiliate_link

def clean_affiliate_link(product_url):
    """
    Remove existing affiliate parameters from a Temu URL
    """
    parsed_url = urlparse(product_url)
    query_params = parse_qs(parsed_url.query)
    
    # Keep only non-affiliate parameters
    clean_params = {}
    affiliate_params = {
        '_x_ads_csite', '_x_ads_channel', '_x_ads_sub_channel', 
        '_x_sessn_id', 'refer_page_name', 'refer_page_id', 
        'refer_page_sn'
    }
    
    for key, values in query_params.items():
        if key not in affiliate_params:
            clean_params[key] = values
    
    # Reconstruct the query string
    new_query = []
    for key, values in clean_params.items():
        for value in values:
            new_query.append(f"{key}={value}")
    
    clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    if new_query:
        clean_url += f"?{'&'.join(new_query)}"
    
    return clean_url

# Example usage
if __name__ == "__main__":
    # Your example URL
    example_url = "https://www.temu.com/es/libro--de-animales-aprendizaje-interactivo-para-ninos-con-paginas-duraderas-en-poliester-que-incluyen---y--ideal-como-regalo-infantil--festivo--de--navidad-meja-habilidades-cognitivas--resistente-a-roturas-g-601100131913227.html?top_gallery_url=https%3A%2F%2Fimg.kwcdn.com%2Fproduct%2Ffancy%2F4bc70669-fb26-45c9-9024-0ff3a0d4b7e5.jpg&spec_gallery_id=70137&_x_ads_csite=affiliate_seo&_x_sessn_id=ioc8mac1wp&refer_page_name=afc_share_goods&refer_page_id=13788_1761959857577_nmc2ha69qb&refer_page_sn=13788"
    
    # Extract product ID
    product_id = extract_product_id_from_url(example_url)
    print(f"Product ID: {product_id}")
    
    # Clean the URL to get the base product URL
    clean_url = clean_affiliate_link(example_url)
    print(f"Clean URL: {clean_url}")
    
    # Generate new affiliate link (replace YOUR_AFFILIATE_ID with actual ID)
    # affiliate_link = generate_affiliate_link(clean_url, "YOUR_AFFILIATE_ID")
    # print(f"New Affiliate Link: {affiliate_link}")