# 🕷️ AI Web Scraper

An intelligent web scraping and content parsing application that combines the power of web scraping with AI-driven content analysis. Built with Streamlit, Serper API, and Google's Gemini AI.

## 🌟 Features

- **Smart Web Scraping**: Extract content from any website using Serper API
- **AI-Powered Parsing**: Use Google's Gemini 2.0 Flash to intelligently parse and extract specific information
- **Multiple Output Formats**: Support for JSON, text, markdown, and list formats
- **Interactive Web Interface**: Beautiful, user-friendly Streamlit interface
- **Content Analysis**: Detailed metrics and analysis of scraped content
- **Download Options**: Export both raw scraped data and AI-parsed results
- **Flexible Extraction**: Natural language descriptions for what you want to extract

## 🚀 Demo

Visit the live application: [AI Web Scraper](https://github.com/naakaarafr/AI-Web-Scraper)

## 📸 Screenshots

*Add screenshots of your application here*

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Serper API key (for web scraping)
- Google Gemini API key (for AI parsing)

### Step 1: Clone the Repository

```bash
git clone https://github.com/naakaarafr/AI-Web-Scraper.git
cd AI-Web-Scraper
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```env
SERPER_API_KEY=your_serper_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Getting API Keys:

1. **Serper API Key**: 
   - Visit [Serper.dev](https://serper.dev/)
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Copy the key to your `.env` file

### Step 5: Run the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```txt
streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
```

## 🎯 Usage

### Basic Usage

1. **Enter Website URL**: Input any website URL you want to scrape
2. **Choose Format**: Select between JSON (structured) or text (clean text only)
3. **Start Scraping**: Click "Start Scraping" to extract content
4. **AI Parsing**: Describe what you want to extract from the content
5. **Get Results**: View and download the AI-parsed results

### Example Use Cases

#### Extract Contact Information
```
Description: "Extract all email addresses and phone numbers"
```

#### Find Product Information
```
Description: "Find all product names with their prices"
```

#### Get Company Details
```
Description: "Extract company names, addresses, and contact details"
```

#### Article Analysis
```
Description: "Summarize the main points and extract key quotes"
```

## 🏗️ Project Structure

```
AI-Web-Scraper/
├── main.py              # Main Streamlit application
├── scrape.py            # Web scraping functionality using Serper API
├── parser.py            # AI parsing using Google Gemini
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## 🔧 Configuration

### Serper API Configuration

The application uses Serper API for web scraping. Serper provides:
- Clean, structured web content extraction
- Image and link extraction
- Meta information parsing
- Reliable scraping without browser dependencies

### Gemini AI Configuration

Google's Gemini 2.0 Flash is used for content parsing:
- Natural language processing
- Structured data extraction
- Multiple output format support
- High context length for large documents

## 📊 Features Breakdown

### Web Scraping Features
- ✅ Extract text content from any website
- ✅ Parse HTML structure (headings, links, images)
- ✅ Extract meta information (title, description, keywords)
- ✅ Handle dynamic content and JavaScript-rendered pages
- ✅ Clean and format text content

### AI Parsing Features
- ✅ Natural language extraction requests
- ✅ Multiple output formats (JSON, text, markdown, list)
- ✅ Context-aware content analysis
- ✅ Structured data extraction
- ✅ Large document handling

### User Interface Features
- ✅ Modern, responsive design
- ✅ Real-time progress indicators
- ✅ Content metrics and statistics
- ✅ Expandable content viewers
- ✅ Download functionality
- ✅ Error handling and user feedback

## 🤖 AI Capabilities

The application leverages Google's Gemini 2.0 Flash for:

- **Intelligent Extraction**: Understands context and extracts relevant information
- **Multiple Formats**: Output in JSON, markdown, plain text, or structured lists
- **Natural Language Queries**: Use everyday language to describe what you want
- **Large Context**: Handle long documents and web pages
- **Accurate Parsing**: High precision in data extraction

## 🔒 Security & Privacy

- **API Key Security**: Environment variables keep your API keys secure
- **No Data Storage**: Content is processed in real-time, not stored
- **Privacy Focused**: Only processes content you explicitly provide
- **Secure Connections**: All API calls use HTTPS

## 🚨 Limitations

- **Rate Limits**: Subject to Serper and Gemini API rate limits
- **Website Restrictions**: Some websites may block scraping requests
- **Content Size**: Very large websites may take longer to process
- **API Costs**: Gemini API usage may incur costs for large volumes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Serper.dev](https://serper.dev/) for providing excellent web scraping API
- [Google AI](https://ai.google.dev/) for Gemini AI capabilities
- [Streamlit](https://streamlit.io/) for the amazing web framework
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/naakaarafr/AI-Web-Scraper/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about the issue

## 🔮 Future Enhancements

- [ ] Support for bulk URL processing
- [ ] Advanced filtering and sorting options
- [ ] Integration with more AI models
- [ ] Data export to various formats (CSV, Excel, PDF)
- [ ] Scheduled scraping capabilities
- [ ] API endpoint for programmatic access
- [ ] Enhanced error handling and retry mechanisms

## ⭐ Show Your Support

If you find this project helpful, please consider giving it a star on GitHub!
