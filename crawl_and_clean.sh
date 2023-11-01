#!/bin/bash

# This script downloads a website using wget, extracts content with readability-cli, 
# then converts and cleans up the content to markdown using pandoc and other tools.

# Usage: script_name <URL> [clean]
# Example: ./script.sh http://example.com clean

# Check for required arguments
if [ -z "$1" ]; then
  echo "Usage: $0 <URL> [clean]"
  echo "[clean] is an optional argument to delete original HTML files after processing."
  exit 1
fi

# Check for required tools
for tool in wget readable pandoc; do
  if ! command -v $tool &> /dev/null; then
    echo "Error: $tool is not installed."
    exit 1
  fi
done

# Directory definitions
URL="$1"
HTML_OUTPUT_DIR="./downloaded_files"
MARKDOWN_OUTPUT_DIR="./markdown_output"


# ...

# Check if the output directory already exists
if [ -d "$HTML_OUTPUT_DIR" ]; then
    echo "Directory $HTML_OUTPUT_DIR already exists. Skipping download."
else
    # Create necessary directories
    mkdir -p "$HTML_OUTPUT_DIR" "$MARKDOWN_OUTPUT_DIR"
    # Use wget to recursively download the website
    if wget -r --no-parent --follow-tags 'a' --reject '*googletagmanager*' -P "$HTML_OUTPUT_DIR" "$URL"; then
        echo "Website downloaded successfully."
    else
        echo "Failed to download the website."
        exit 1
    fi
fi

# Process the downloaded files
find "$HTML_OUTPUT_DIR" -type f -print0 | while IFS= read -r -d $'\0' file; do
  relative_path="${file#$HTML_OUTPUT_DIR/}"

  # Extract and clean content
  extracted_text=$(readable "$file" --properties title html-content -l force)
  if [ -n "$extracted_text" ]; then
    markdown_file="$MARKDOWN_OUTPUT_DIR/$relative_path.md"
    mkdir -p "$(dirname "$markdown_file")"

    echo "$extracted_text" | \
    pandoc -s -f html -t markdown | \
    grep -vE "^(:::|\`\`\`|<!-- -->)$" | \
    perl -p0e 's/{[^}]*}//gs' | \
    sed 's|\(https://static\.wixstatic\.com/media/[^/]*~mv2\.jpg\)[^)]*|\1|g' | \
    sed '/^<div>$/,/^<\/div>$/d' | \
    awk 'NF {print $0; blank=0} !NF {if (!blank) print $0; blank=1}' | \
    sed 's/^[ \t]*//;s/[ \t]*$//' > "$markdown_file"

    echo "Processed: $file -> $markdown_file"
  else
    echo "Failed to extract content from $file"
  fi
done

# Option to delete original HTML files
if [ "$2" == "clean" ]; then
  echo "Deleting original HTML files..."
  find "$HTML_OUTPUT_DIR" -type f -exec rm {} \;
fi

echo "Processing completed."
