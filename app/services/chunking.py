def chunk_content(content: str, chunk_size: int = 1000, overlap: int = 200):
    chunks = []
    start = 0
    content_length = len(content)

    while start < content_length:
        end = start + chunk_size
        if end < content_length:
            # Try to find the end of a sentence within the last 100 characters of the chunk
            sentence_end = content.rfind('.', end - 100, end)
            if sentence_end != -1:
                end = sentence_end + 1
            else:
                # If no sentence end, try to break at a word boundary
                end = content.rfind(' ', end - 50, end) + 1
                if end == 0:  # if no word boundary found
                    end = start + chunk_size
        else:
            end = content_length

        chunk = content[start:end].strip()
        chunks.append(chunk)
        start = end - overlap

    return chunks