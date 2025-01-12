import streamlit as st
import re
import pyperclip

def escape_regex(string):
    """Escape special regex characters"""
    return re.escape(string)

def convert_to_regex(input_data, match_type, case_transform, word_boundary):
    """Convert input data to regex pattern"""
    if not input_data.strip():
        return ''
    
    # Split input into lines and clean
    data_list = [line.strip() for line in input_data.split('\n') if line.strip()]
    
    # Apply case transformation
    if case_transform == 'upper':
        data_list = [text.upper() for text in data_list]
    elif case_transform == 'lower':
        data_list = [text.lower() for text in data_list]
    
    # Escape special characters
    escaped_data = [escape_regex(text) for text in data_list]
    
    # Add word boundaries if requested
    if word_boundary:
        processed_data = [rf'\b{text}\b' for text in escaped_data]
    else:
        processed_data = escaped_data
    
    # Join patterns with OR operator
    pattern = '|'.join(processed_data)
    
    # Apply match type modifications
    if match_type == 'exact':
        pattern = f'^(?:{pattern})$'
    elif match_type == 'startsWith':
        pattern = f'^(?:{pattern})'
    elif match_type == 'endsWith':
        pattern = f'(?:{pattern})$'
    
    return pattern

# Set page config
st.set_page_config(page_title="Looker Studio Regex Pattern Generator", layout="wide")

# Title
st.title("Looker Studio Regex Pattern Generator")

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    # Input text area
    input_data = st.text_area(
        "Enter data values (one per line):",
        height=200,
        placeholder="Enter your data values here..."
    )

with col2:
    # Match type selector
    match_type = st.selectbox(
        "Match Type:",
        options=['contains', 'exact', 'startsWith', 'endsWith'],
        format_func=lambda x: {
            'contains': 'Contains',
            'exact': 'Exact Match',
            'startsWith': 'Starts With',
            'endsWith': 'Ends With'
        }[x]
    )
    
    # Case transform selector
    case_transform = st.selectbox(
        "Case Transform:",
        options=['none', 'upper', 'lower'],
        format_func=lambda x: {
            'none': 'No Transform',
            'upper': 'Convert to Uppercase',
            'lower': 'Convert to Lowercase'
        }[x]
    )
    
    # Word boundary checkbox
    word_boundary = st.checkbox("Match Whole Words Only")

# Generate the pattern
pattern = convert_to_regex(input_data, match_type, case_transform, word_boundary)

# Display the pattern
st.subheader("Generated Pattern:")
if pattern:
    pattern_placeholder = st.code(pattern, language=None)
    
    # Copy button
    if st.button("Copy Pattern"):
        try:
            pyperclip.copy(pattern)
            st.success("Pattern copied to clipboard!")
        except:
            st.error("Could not copy to clipboard. Please copy the pattern manually.")
else:
    st.text("Enter data values above to generate pattern")

# Add some helpful instructions at the bottom
with st.expander("How to use"):
    st.markdown("""
    1. Enter your data values in the text area, one value per line
    2. Choose your match type:
        - Contains: Matches if the pattern appears anywhere in the text
        - Exact Match: Matches only if the entire text matches the pattern
        - Starts With: Matches if the text begins with the pattern
        - Ends With: Matches if the text ends with the pattern
    3. Select case transformation if needed:
        - No Transform: Keep original case
        - Convert to Uppercase: Transform all text to uppercase
        - Convert to Lowercase: Transform all text to lowercase
    4. Check 'Match Whole Words Only' if you want to match complete words only
    5. Click 'Copy Pattern' to copy the generated regex to your clipboard
    """)
