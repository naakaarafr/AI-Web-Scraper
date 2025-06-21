import streamlit as st
import json
from datetime import datetime
from scrape import (
    scrape_and_process,
    split_content,
    clean_text_content
)
from parser import parse_with_gemini, parse_with_gemini_structured

# Page configuration
st.set_page_config(
    page_title="AI Web Scraper",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: black
    }
    
    .info-box {
        background-color: #e7f3ff;
        border: 1px solid #b8daff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .step-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .download-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🕷️ AI Web Scraper</h1>
    <p>Intelligent web scraping and content parsing with AI</p>
</div>
""", unsafe_allow_html=True)

# Create main layout with columns
col1, col2 = st.columns([2, 1])

with col1:
    # Step 1: URL Input and Scraping
    st.markdown('<div class="step-header">📍 Step 1: Enter Website Details</div>', unsafe_allow_html=True)
    
    # URL input with better styling
    url = st.text_input(
        "🌐 Website URL",
        placeholder="https://example.com",
        help="Enter the complete URL including https:// or http://"
    )
    
    # Format selection with better presentation
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        scrape_format = st.selectbox(
            "📋 Output Format",
            ["json", "text"],
            help="JSON: Structured data with metadata | Text: Clean text only"
        )
    
    with col1_2:
        st.write("") # Empty space for alignment
        scrape_button = st.button("🚀 Start Scraping", type="primary")

    # Scraping logic
    if scrape_button:
        if url:
            with st.spinner("🔍 Scraping website..."):
                progress_bar = st.progress(0)
                
                try:
                    progress_bar.progress(25)
                    scraped_data = scrape_and_process(url, return_format=scrape_format)
                    progress_bar.progress(100)
                    
                    if scraped_data:
                        st.markdown("""
                        <div class="success-box">
                            ✅ <strong>Website scraped successfully!</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if scrape_format == "json":
                            st.session_state.scraped_data = scraped_data
                            st.session_state.content_format = "json"
                            
                            text_content = scraped_data.get('text', '')
                            st.session_state.text_content = clean_text_content(text_content)
                            
                            # Display summary with metrics
                            st.markdown('<div class="step-header">📊 Content Summary</div>', unsafe_allow_html=True)
                            
                            # Get title with fallback
                            title = scraped_data.get('title', '').strip()
                            if not title:
                                title = scraped_data.get('meta', {}).get('title', '').strip()
                            if not title and scraped_data.get('headings'):
                                title = scraped_data['headings'][0].strip()
                            if not title:
                                title = "No title found"
                            
                            # Metrics in columns
                            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                            
                            with metric_col1:
                                st.metric("📝 Text Length", f"{len(text_content):,}", help="Characters")
                            with metric_col2:
                                st.metric("🔗 Links", f"{len(scraped_data.get('links', [])):,}")
                            with metric_col3:
                                st.metric("🖼️ Images", f"{len(scraped_data.get('images', [])):,}")
                            with metric_col4:
                                st.metric("📋 Headings", f"{len(scraped_data.get('headings', [])):,}")
                            
                            # Title and URL info
                            st.write(f"**🏷️ Title:** {title}")
                            st.write(f"**🌐 URL:** {url}")
                            
                            # Expandable content view
                            with st.expander("🔍 View Raw Scraped Data", expanded=False):
                                st.json(scraped_data)
                                
                        elif scrape_format == "text":
                            st.session_state.text_content = scraped_data
                            st.session_state.content_format = "text"
                            
                            st.metric("📝 Text Length", f"{len(scraped_data):,} characters")
                            
                            with st.expander("📄 View Text Content", expanded=False):
                                st.text_area("Content", scraped_data, height=300, disabled=True)
                                
                    else:
                        st.markdown("""
                        <div class="warning-box">
                            ⚠️ <strong>Failed to scrape the website</strong><br>
                            • Check if the URL is accessible<br>
                            • Some websites block scraping requests<br>
                            • Verify your network connection
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    
        else:
            st.warning("⚠️ Please enter a valid URL")

    # Step 2: Content Parsing
    if "text_content" in st.session_state:
        st.markdown('<div class="step-header">🤖 Step 2: AI Content Parsing</div>', unsafe_allow_html=True)
        
        parse_description = st.text_area(
            "🎯 What do you want to extract?",
            placeholder="e.g., Extract all email addresses and phone numbers\nFind product names with prices\nGet all company names mentioned",
            height=100,
            help="Be specific about what information you want to extract"
        )
        
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            output_format = st.selectbox(
                "📤 Output Format",
                ["text", "json", "markdown", "list"],
                help="Choose how to format the extracted data"
            )
        
        with col2_2:
            st.write("")
            parse_button = st.button("🧠 Parse with AI", type="primary")

        if parse_button:
            if parse_description:
                with st.spinner("🤖 AI is analyzing the content..."):
                    try:
                        content_chunks = split_content(st.session_state.text_content)
                        
                        parsed_result = parse_with_gemini_structured(
                            content_chunks, 
                            parse_description, 
                            output_format=output_format
                        )
                        
                        st.markdown('<div class="step-header">✨ Parsing Results</div>', unsafe_allow_html=True)
                        
                        if output_format == "json":
                            try:
                                json_result = json.loads(parsed_result)
                                st.json(json_result)
                            except:
                                st.code(parsed_result, language='json')
                        elif output_format == "markdown":
                            st.markdown(parsed_result)
                        else:
                            st.write(parsed_result)
                        
                        st.session_state.parsed_result = parsed_result
                        st.session_state.parse_description = parse_description
                        
                    except Exception as e:
                        st.error(f"❌ Parsing error: {str(e)}")
            else:
                st.warning("⚠️ Please describe what you want to extract")

with col2:
    # Sidebar-like information panel
    st.markdown('<div class="step-header">📚 Quick Guide</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        **🔍 How it works:**
        1. Enter any website URL
        2. Choose output format
        3. Let AI scrape the content
        4. Describe what to extract
        5. Get AI-parsed results
        
        **💡 Parsing Examples:**
        • "Extract all email addresses"
        • "Find product prices"
        • "Get contact information"
        • "List company names"
        • "Extract article headlines"
        """)
    
    # Content statistics
    if "text_content" in st.session_state:
        st.markdown('<div class="step-header">📈 Content Stats</div>', unsafe_allow_html=True)
        
        text_len = len(st.session_state.text_content)
        word_count = len(st.session_state.text_content.split())
        
        st.metric("📝 Characters", f"{text_len:,}")
        st.metric("💬 Words", f"{word_count:,}")
        
        if st.session_state.get("content_format") == "json":
            scraped_data = st.session_state.scraped_data
            st.metric("🔗 Links", f"{len(scraped_data.get('links', [])):,}")
            st.metric("🖼️ Images", f"{len(scraped_data.get('images', [])):,}")

# Download section (full width)
if "parsed_result" in st.session_state:
    st.markdown('<div class="step-header">💾 Step 3: Download Results</div>', unsafe_allow_html=True)
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        # Download parsed results
        result_data = {
            "url": url if url else "Unknown",
            "parse_description": st.session_state.get('parse_description', ''),
            "result": st.session_state.get('parsed_result', ''),
            "content_format": st.session_state.get('content_format', 'unknown'),
            "scraped_at": str(datetime.now())
        }
        
        safe_url = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '') if url else 'unknown_url'
        filename = f"parsed_result_{safe_url}_{str(hash(st.session_state.get('parse_description', '')))[:8]}.json"
        
        st.download_button(
            label="📥 Download Parsed Results",
            data=json.dumps(result_data, indent=2, ensure_ascii=False),
            file_name=filename,
            mime="application/json",
            help="Download AI-parsed results as JSON"
        )
    
    with col_dl2:
        # Download raw scraped data (if available)
        if "scraped_data" in st.session_state:
            raw_data_json = json.dumps(st.session_state.scraped_data, indent=2, ensure_ascii=False)
            raw_filename = f"raw_data_{safe_url}.json"
            
            st.download_button(
                label="📥 Download Raw Data",
                data=raw_data_json,
                file_name=raw_filename,
                mime="application/json",
                help="Download complete scraped data"
            )

# Additional Information Section
if "scraped_data" in st.session_state and st.session_state.get("content_format") == "json":
    st.markdown('<div class="step-header">🔍 Detailed Analysis</div>', unsafe_allow_html=True)
    
    scraped_data = st.session_state.scraped_data
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["🔗 Links", "🖼️ Images", "📋 Headings", "📄 Meta Info"])
    
    with tab1:
        if scraped_data.get('links') and len(scraped_data['links']) > 0:
            st.write(f"**Found {len(scraped_data['links']):,} links:**")
            
            # Show links in a more organized way
            for i, link in enumerate(scraped_data['links'][:50], 1):  # Show first 50
                st.write(f"`{i:02d}.` {link}")
            
            if len(scraped_data['links']) > 50:
                st.info(f"... and {len(scraped_data['links']) - 50:,} more links")
        else:
            st.info("No links found in the scraped content.")
    
    with tab2:
        if scraped_data.get('images') and len(scraped_data['images']) > 0:
            st.write(f"**Found {len(scraped_data['images']):,} images:**")
            
            for i, img in enumerate(scraped_data['images'][:20], 1):  # Show first 20
                st.write(f"`{i:02d}.` {img}")
            
            if len(scraped_data['images']) > 20:
                st.info(f"... and {len(scraped_data['images']) - 20:,} more images")
        else:
            st.info("No images found in the scraped content.")
    
    with tab3:
        if scraped_data.get('headings') and len(scraped_data['headings']) > 0:
            st.write(f"**Found {len(scraped_data['headings']):,} headings:**")
            
            for i, heading in enumerate(scraped_data['headings'], 1):
                st.write(f"`{i:02d}.` {heading}")
        else:
            st.info("No headings found in the scraped content.")
    
    with tab4:
        if scraped_data.get('meta'):
            meta = scraped_data['meta']
            has_meta_info = any([meta.get('description'), meta.get('keywords'), meta.get('author')])
            
            if has_meta_info:
                if meta.get('description'):
                    st.write(f"**📝 Description:** {meta['description']}")
                if meta.get('keywords'):
                    st.write(f"**🏷️ Keywords:** {meta['keywords']}")
                if meta.get('author'):
                    st.write(f"**👤 Author:** {meta['author']}")
            else:
                st.info("No meta information available.")
        else:
            st.info("No meta information found.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🕷️ AI Web Scraper | Built with Streamlit & Gemini AI
</div>
""", unsafe_allow_html=True)