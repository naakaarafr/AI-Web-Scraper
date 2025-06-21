import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def parse_with_gemini(content_chunks, parse_description):
    """
    Parse content using Gemini 2.0 Flash
    
    Args:
        content_chunks (list): List of content chunks to parse
        parse_description (str): Description of what to parse/extract
    
    Returns:
        str: Parsed result from Gemini
    """
    try:
        # Initialize Gemini 2.0 Flash model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Combine all chunks into one text (Gemini can handle large contexts)
        combined_content = "\n\n".join(str(chunk) for chunk in content_chunks)
        
        # Create the prompt
        prompt = f"""
You are an expert content parser and data extractor. Your task is to analyze the provided web content and extract specific information based on the user's request.

USER REQUEST: {parse_description}

WEB CONTENT TO ANALYZE:
{combined_content}

INSTRUCTIONS:
1. Carefully analyze the provided web content
2. Extract the information requested by the user
3. Present the results in a clear, organized format
4. If the requested information is not found, clearly state that
5. Be precise and accurate in your extraction
6. If extracting structured data (like lists, tables, etc.), format it clearly
7. Provide context when necessary to make the extracted information meaningful

Please provide your analysis and extracted information below:
"""

        # Generate response
        print("Sending request to Gemini 2.0 Flash...")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=8192,
                temperature=0.2,  # Lower temperature for more precise extraction
            )
        )
        
        if response.text:
            print("Successfully parsed content with Gemini!")
            return response.text.strip()
        else:
            return "No response generated. Please try again with a different request."
            
    except Exception as e:
        print(f"Error parsing with Gemini: {str(e)}")
        return f"Error occurred while parsing: {str(e)}"

def parse_with_gemini_structured(content_chunks, parse_description, output_format="text"):
    """
    Parse content using Gemini 2.0 Flash with structured output options
    
    Args:
        content_chunks (list): List of content chunks to parse
        parse_description (str): Description of what to parse/extract
        output_format (str): "text", "json", "markdown", or "list"
    
    Returns:
        str: Parsed result in specified format
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        combined_content = "\n\n".join(str(chunk) for chunk in content_chunks)
        
        # Format-specific instructions
        format_instructions = {
            "json": "Format your response as valid JSON with appropriate keys and values.",
            "markdown": "Format your response using proper Markdown syntax with headers, lists, and emphasis.",
            "list": "Format your response as a clean, numbered or bulleted list.",
            "text": "Format your response as clear, readable text with proper paragraphs."
        }
        
        prompt = f"""
You are an expert content parser and data extractor. Your task is to analyze the provided web content and extract specific information based on the user's request.

USER REQUEST: {parse_description}

OUTPUT FORMAT: {output_format.upper()}
FORMAT INSTRUCTIONS: {format_instructions.get(output_format, format_instructions["text"])}

WEB CONTENT TO ANALYZE:
{combined_content}

INSTRUCTIONS:
1. Carefully analyze the provided web content
2. Extract the information requested by the user
3. {format_instructions.get(output_format, format_instructions["text"])}
4. If the requested information is not found, clearly state that in the specified format
5. Be precise and accurate in your extraction
6. Provide context when necessary to make the extracted information meaningful
7. Ensure your response follows the requested output format exactly

Please provide your analysis and extracted information below:
"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=8192,
                temperature=0.2,
            )
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "No response generated. Please try again with a different request."
            
    except Exception as e:
        return f"Error occurred while parsing: {str(e)}"

def parse_with_gemini_examples(content_chunks, parse_description, examples=None):
    """
    Parse content using Gemini 2.0 Flash with example-based prompting
    
    Args:
        content_chunks (list): List of content chunks to parse
        parse_description (str): Description of what to parse/extract
        examples (list): Optional list of example extractions to guide the model
    
    Returns:
        str: Parsed result with example-guided extraction
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        combined_content = "\n\n".join(str(chunk) for chunk in content_chunks)
        
        example_text = ""
        if examples:
            example_text = "\n\nEXAMPLES OF DESIRED OUTPUT:\n"
            for i, example in enumerate(examples, 1):
                example_text += f"Example {i}: {example}\n"
        
        prompt = f"""
You are an expert content parser and data extractor. Your task is to analyze the provided web content and extract specific information based on the user's request.

USER REQUEST: {parse_description}
{example_text}

WEB CONTENT TO ANALYZE:
{combined_content}

INSTRUCTIONS:
1. Carefully analyze the provided web content
2. Extract the information requested by the user
3. Follow the pattern shown in the examples (if provided)
4. Present the results in a clear, organized format similar to the examples
5. If the requested information is not found, clearly state that
6. Be precise and accurate in your extraction
7. Maintain consistency with the example format and style

Please provide your analysis and extracted information below:
"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=8192,
                temperature=0.2,
            )
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "No response generated. Please try again with a different request."
            
    except Exception as e:
        return f"Error occurred while parsing: {str(e)}"

# Alias for backward compatibility with existing code
parse_with_ollama = parse_with_gemini

# Test function
def test_gemini_connection():
    """
    Test if Gemini API is properly configured
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say 'Hello, Gemini is working!'")
        return response.text.strip() if response.text else "Connection test failed"
    except Exception as e:
        return f"Connection test failed: {str(e)}"

if __name__ == "__main__":
    # Test the connection
    print("Testing Gemini connection...")
    result = test_gemini_connection()
    print(f"Test result: {result}")
    
    # Example usage
    test_content = ["This is a sample webpage with contact information. Email: john@example.com, Phone: (555) 123-4567"]
    test_description = "Extract all contact information including emails and phone numbers"
    
    print("\nTesting content parsing...")
    parsed = parse_with_gemini(test_content, test_description)
    print(f"Parsed result: {parsed}")