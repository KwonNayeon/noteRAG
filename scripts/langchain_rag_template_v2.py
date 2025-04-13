!pip install reportlab langchain langchain_openai openai

import json
import re
import datetime
import os
import getpass
from google.colab import files
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Import LangChain and OpenAI components
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# Upload text file
def upload_text_file():
    """
    Handles the upload of a text file and returns its content.
    """
    print("Please upload a text file...")
    uploaded = files.upload()

    if not uploaded:
        raise ValueError("No file was uploaded")

    filename = list(uploaded.keys())[0]
    print(f"Uploaded file: {filename}")

    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"File loaded: {len(content)} characters")
    return content, filename

# Set OpenAI API key
def set_openai_api_key():
    """
    Sets the OpenAI API key from user input without exposing it.
    """
    api_key = getpass.getpass("Enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = api_key
    print("API key set successfully!")

set_openai_api_key()

# Prepare text for processing with LangChain
def prepare_text_for_langchain(text):
    """
    Splits the text into chunks suitable for processing with LangChain.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text)

    # Convert chunks to LangChain documents
    docs = [Document(page_content=chunk) for chunk in chunks]

    return docs

# Generate summary using LangChain and OpenAI
def generate_langchain_summary(docs, api_key):
    """
    Generates a structured summary using LangChain and OpenAI.
    Returns a dictionary with high_level summary and expanded details.
    """
    # Initialize OpenAI model
    llm = ChatOpenAI(
        temperature=0.3,
        model="gpt-3.5-turbo-16k",
        openai_api_key=api_key,
        max_tokens=300
    )

    high_level_prompt = PromptTemplate(
        template="""Summarize the following text into three simple and clear main ideas.
    Use easy vocabulary and short sentences. Each point should help someone who struggles with focus or reading.

    {text}

    MAIN IDEAS:
    1.
    2.
    3.
    """,
        input_variables=["text"]
    )

    expand_prompt = PromptTemplate(
    template="""Here are three main ideas. For each one, write three short and easy explanations.
    Use simple words. Explain clearly so someone with reading difficulties can understand.

    MAIN IDEAS:
    {text}

    EXPLANATIONS:
    Point 1:
    1.1
    1.2
    1.3

    Point 2:
    2.1
    2.2
    2.3

    Point 3:
    3.1
    3.2
    3.3
    """,
        input_variables=["text"]
    )

    # Title, topic, and keywords prompt
    meta_prompt = PromptTemplate(
        template="""
        From the following text, extract:
        1. A simple and short summary title (under 10 words)
        2. The main topic of the text (1–3 words)
        3. 3 relevant keywords

        TEXT:
        {text}

        OUTPUT:
        Title:
        Topic:
        Keywords:
        """,
        input_variables=["text"]
    )

    # Generate high-level summary
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="stuff",
        prompt=high_level_prompt
    )
    high_level_output = summary_chain.run(docs)

    # Extract the three main points
    main_points = []
    for line in high_level_output.strip().split('\n'):
        if re.match(r'^\d+\.', line.strip()):
            main_points.append(line.strip())

    # Ensure we have exactly 3 points
    while len(main_points) < 3:
        main_points.append(f"Additional important point {len(main_points)+1}.")

    # Use the main points to generate expanded summaries
    expand_chain = load_summarize_chain(
        llm=llm,
        chain_type="stuff",
        prompt=expand_prompt
    )
    expand_output = expand_chain.run([Document(page_content='\n'.join(main_points))])

    # Process expanded output
    expanded_sections = []
    current_section = None

    for line in expand_output.strip().split('\n'):
        if line.startswith('Point'):
            if current_section is not None:
                expanded_sections.append(current_section)
            current_section = []
        elif re.match(r'^\d+\.\d+', line.strip()) and current_section is not None:
            current_section.append(line.strip())

    if current_section is not None:
        expanded_sections.append(current_section)

    # Ensure we have 3 sections with 3 points each
    while len(expanded_sections) < 3:
        expanded_sections.append([
            f"{len(expanded_sections)+1}.1 Additional detail.",
            f"{len(expanded_sections)+1}.2 Additional detail.",
            f"{len(expanded_sections)+1}.3 Additional detail."
        ])

    for i, section in enumerate(expanded_sections):
        while len(section) < 3:
            section.append(f"{i+1}.{len(section)+1} Additional detail.")

    # Generate meta information (title, topic, keywords)
    meta_chain = load_summarize_chain(
        llm=llm,
        chain_type="stuff",
        prompt=meta_prompt
    )
    meta_output = meta_chain.run(docs)

    # Post-process meta_output
    meta_data = {}
    for line in meta_output.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            meta_data[key.strip().lower()] = value.strip()


    # Format the final summary structure
    summary = {
        "title": meta_data.get("title", ""),
        "topic": meta_data.get("topic", ""),
        "keywords": meta_data.get("keywords", "").split(','),
        "high_level": main_points,
        "expanded": expanded_sections
    }

    return summary

# Create PDF summary
def create_pdf_summary(summary, filename="document"):
    """
    Creates a PDF file containing the summary with metadata.
    """
    output_file = f"{filename.replace('.txt', '')}_summary.pdf"

    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle',
                                 parent=styles['Title'],
                                 fontSize=16,
                                 alignment=1,
                                 spaceAfter=12)
    heading_style = ParagraphStyle('CustomHeading',
                                  parent=styles['Heading1'],
                                  fontSize=14,
                                  spaceAfter=6)
    subheading_style = ParagraphStyle('CustomSubHeading',
                                     parent=styles['Heading2'],
                                     fontSize=12,
                                     spaceAfter=4)
    body_style = ParagraphStyle('CustomBody',
                               parent=styles['Normal'],
                               fontSize=11,
                               leading=14)
    meta_style = ParagraphStyle('CustomMeta',
                               parent=styles['Normal'],
                               fontSize=10,
                               leading=12,
                               textColor='#666666')

    # Custom document title from summary if available
    doc_title = summary.get("title", "Document Summary")
    story.append(Paragraph(doc_title, title_style))
    story.append(Spacer(1, 0.15*inch))

    # Add metadata (topic and keywords) if available
    if "topic" in summary and summary["topic"]:
        story.append(Paragraph(f"Topic: {summary['topic']}", meta_style))

    if "keywords" in summary and summary["keywords"]:
        # Join keywords with commas if it's a list, otherwise use as is
        keywords_text = ", ".join(summary["keywords"]) if isinstance(summary["keywords"], list) else summary["keywords"]
        story.append(Paragraph(f"Keywords: {keywords_text}", meta_style))

    story.append(Spacer(1, 0.25*inch))

    # High-level summary
    story.append(Paragraph("Main Ideas", heading_style))
    for i, point in enumerate(summary["high_level"], 1):
        # Remove numbers if they exist at the beginning of the line
        point_text = re.sub(r'^\d+\.\s*', '', point)
        story.append(Paragraph(f"{i}. {point_text}", body_style))
    story.append(Spacer(1, 0.25*inch))

    # Expanded summary
    story.append(Paragraph("Detailed Explanations", heading_style))
    for i, section in enumerate(summary["expanded"], 1):
        story.append(Paragraph(f"Point {i}", subheading_style))
        for detail in section:
            # Extract the detail text without the numbering
            match = re.search(r'^\d+\.\d+\s+(.*)', detail)
            if match:
                detail_text = match.group(1)
            else:
                detail_text = detail

            # Create proper numbering
            story.append(Paragraph(f"{i}.{section.index(detail)+1} {detail_text}", body_style))
        story.append(Spacer(1, 0.15*inch))

    # Save PDF
    doc.build(story)

    print(f"PDF summary created: {output_file}")
    files.download(output_file)

    return output_file

# Create JSON files
def create_json_files(summary, filename="document"):
    """
    Creates both standard and iOS-formatted JSON files containing the summary with metadata.
    """
    # Standard JSON
    json_file = f"{filename.replace('.txt', '')}_summary.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"JSON summary created: {json_file}")
    files.download(json_file)

    # iOS JSON format
    ios_file = f"{filename.replace('.txt', '')}_ios_summary.json"

    # Clean up text for iOS format by removing numbering
    high_level_clean = []
    for point in summary["high_level"]:
        clean_point = re.sub(r'^\d+\.\s*', '', point)
        high_level_clean.append(clean_point)

    # Get title from summary or use filename
    doc_title = summary.get("title", filename.replace('.txt', ''))

    ios_json = {
        "document": {
            "title": doc_title,
            "topic": summary.get("topic", ""),
            "keywords": summary.get("keywords", []),
            "summary": {
                "highlevel": [
                    {"id": 1, "text": high_level_clean[0]},
                    {"id": 2, "text": high_level_clean[1]},
                    {"id": 3, "text": high_level_clean[2]}
                ],
                "expanded": []
            }
        },
        "metadata": {
            "version": "1.0",
            "generatedAt": datetime.datetime.now().isoformat(),
            "format": "ios-summary"
        }
    }

# Main pipeline
def run_langchain_summary():
    """
    Executes the complete summary generation pipeline using LangChain and OpenAI.
    """
    try:
        # 1. Set OpenAI API key
        print("STEP 1: Setting up OpenAI API")
        api_key = set_openai_api_key()

        # 2. Upload text file
        print("\nSTEP 2: Uploading text file")
        content, filename = upload_text_file()

        # 3. Prepare documents for LangChain
        print("\nSTEP 3: Processing text with LangChain")
        docs = prepare_text_for_langchain(content)

        # 4. Generate summary
        print("\nSTEP 4: Generating summary with OpenAI")
        summary = generate_langchain_summary(docs, api_key)

        # 5. Create PDF
        print("\nSTEP 5: Creating PDF summary")
        pdf_file = create_pdf_summary(summary, filename)

        # 6. Create JSON files
        print("\nSTEP 6: Creating JSON files")
        json_file, ios_file, ios_json = create_json_files(summary, filename)

        # 7. Display results
        print("\n✅ Summary completed! The following files have been downloaded:")
        print(f"- PDF: {pdf_file}")
        print(f"- JSON: {json_file}")
        print(f"- iOS JSON: {ios_file}")

        # Summary preview
        print("\n=== Summary Preview ===")
        print("High-level summary:")
        for i, item in enumerate(summary["high_level"], 1):
            clean_item = re.sub(r'^\d+\.\s*', '', item)
            print(f"{i}. {clean_item}")

        print("\nExpanded summary (first point):")
        for i, item in enumerate(summary["expanded"][0], 1):
            match = re.search(r'^\d+\.\d+\s+(.*)', item)
            if match:
                detail_text = match.group(1)
            else:
                detail_text = item
            print(f"1.{i} {detail_text}")

        return summary, ios_json

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

# Execute the code
if __name__ == "__main__":
    run_langchain_summary()