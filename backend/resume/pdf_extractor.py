import re
import pymupdf


# ============================================================
# SETTINGS
# ============================================================

MIN_TEXT_LENGTH = 20

# A real column normally occupies a meaningful portion
# of the page.
MIN_COLUMN_WIDTH_RATIO = 0.25

# Minimum horizontal separation.
MIN_COLUMN_GAP = 45

# Minimum number of blocks required in each column.
MIN_COLUMN_BLOCKS = 4

# A real column should contain a reasonable amount of text.
MIN_COLUMN_TEXT_RATIO = 0.20


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    if not text:
        return ""

    text = str(text)

    text = text.replace("\u00a0", " ")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    result = []

    for line in text.splitlines():

        line = re.sub(
            r"[ \t]+",
            " ",
            line
        ).strip()

        if line:
            result.append(line)

    return "\n".join(result)


# ============================================================
# GET TEXT BLOCKS
# ============================================================

def get_text_blocks(page):

    raw_blocks = page.get_text(
        "blocks",
        sort=False
    )

    blocks = []

    for block in raw_blocks:

        if len(block) < 7:
            continue

        x0, y0, x1, y1, text, block_no, block_type = block[:7]

        # Only text blocks
        if block_type != 0:
            continue

        if not text:
            continue

        text = clean_text(text)

        if not text:
            continue

        blocks.append(
            {
                "x0": float(x0),
                "y0": float(y0),
                "x1": float(x1),
                "y1": float(y1),
                "text": text,
                "block_no": block_no,
            }
        )

    return blocks


# ============================================================
# BLOCK WIDTH
# ============================================================

def block_width(block):
    return block["x1"] - block["x0"]


# ============================================================
# BLOCK HEIGHT
# ============================================================

def block_height(block):
    return block["y1"] - block["y0"]


# ============================================================
# FULL WIDTH BLOCK
# ============================================================

def is_full_width_block(block, page_width):

    width = block_width(block)

    return width >= page_width * 0.70


# ============================================================
# COLUMN CANDIDATE
# ============================================================

def get_column_candidates(
    blocks,
    page_width
):

    candidates = []

    for block in blocks:

        width = block_width(block)

        # Ignore very wide blocks.
        if width >= page_width * 0.70:
            continue

        # Ignore extremely narrow blocks.
        if width < page_width * 0.10:
            continue

        candidates.append(block)

    return candidates


# ============================================================
# DETECT REAL TWO COLUMN LAYOUT
# ============================================================

def detect_columns(
    blocks,
    page_width
):
    """
    Detect a genuine two-column layout.

    Important:
    Right-aligned dates in a normal resume should NOT
    be considered a second column.

    A second column must have:
    - several blocks
    - meaningful text
    - meaningful width
    - meaningful separation
    """

    candidates = get_column_candidates(
        blocks,
        page_width
    )

    if len(candidates) < 8:
        return None

    x_positions = sorted(
        set(
            round(block["x0"], 1)
            for block in candidates
        )
    )

    if len(x_positions) < 4:
        return None

    best_split = None
    best_score = 0

    for i in range(
        1,
        len(x_positions)
    ):

        left_x = x_positions[i - 1]
        right_x = x_positions[i]

        gap = right_x - left_x

        if gap < MIN_COLUMN_GAP:
            continue

        split_x = (
            left_x + right_x
        ) / 2

        left = [
            block
            for block in candidates
            if block["x0"] < split_x
        ]

        right = [
            block
            for block in candidates
            if block["x0"] >= split_x
        ]

        if len(left) < MIN_COLUMN_BLOCKS:
            continue

        if len(right) < MIN_COLUMN_BLOCKS:
            continue

        # ----------------------------------------------------
        # Calculate actual occupied width of each side.
        # ----------------------------------------------------

        if not left or not right:
            continue

        left_min_x = min(
            block["x0"]
            for block in left
        )

        left_max_x = max(
            block["x1"]
            for block in left
        )

        right_min_x = min(
            block["x0"]
            for block in right
        )

        right_max_x = max(
            block["x1"]
            for block in right
        )

        left_width = (
            left_max_x - left_min_x
        )

        right_width = (
            right_max_x - right_min_x
        )

        # A real column should occupy reasonable width.
        if (
            left_width
            < page_width * MIN_COLUMN_WIDTH_RATIO
        ):
            continue

        if (
            right_width
            < page_width * MIN_COLUMN_WIDTH_RATIO
        ):
            continue

        # ----------------------------------------------------
        # Text amount.
        # ----------------------------------------------------

        left_chars = sum(
            len(block["text"])
            for block in left
        )

        right_chars = sum(
            len(block["text"])
            for block in right
        )

        total_chars = (
            left_chars + right_chars
        )

        if total_chars == 0:
            continue

        left_text_ratio = (
            left_chars / total_chars
        )

        right_text_ratio = (
            right_chars / total_chars
        )

        # Prevent date-only right side from becoming
        # a column.
        if (
            left_text_ratio
            < MIN_COLUMN_TEXT_RATIO
        ):
            continue

        if (
            right_text_ratio
            < MIN_COLUMN_TEXT_RATIO
        ):
            continue

        # ----------------------------------------------------
        # Score the possible split.
        # ----------------------------------------------------

        balance = min(
            left_text_ratio,
            right_text_ratio
        )

        score = (
            balance * 100
            + min(gap, 200) * 0.1
        )

        if score > best_score:

            best_score = score

            best_split = {
                "split_x": split_x,
                "left": left,
                "right": right,
            }

    return best_split


# ============================================================
# SORT BLOCKS
# ============================================================

def sort_blocks(blocks):

    return sorted(
        blocks,
        key=lambda block: (
            round(block["y0"], 1),
            block["x0"]
        )
    )


# ============================================================
# BLOCKS TO TEXT
# ============================================================

def blocks_to_text(blocks):

    blocks = sort_blocks(
        blocks
    )

    lines = []

    for block in blocks:

        for line in block["text"].splitlines():

            line = clean_text(line)

            if line:
                lines.append(line)

    return "\n".join(lines)


# ============================================================
# NORMAL ONE-COLUMN EXTRACTION
# ============================================================

def extract_one_column_page(page):

    """
    Use PyMuPDF's natural text sorting for normal
    one-column resumes.

    This is the path Shubham and Aditya should use.
    """

    text = page.get_text(
        "text",
        sort=True
    )

    return clean_text(text)


# ============================================================
# TWO-COLUMN EXTRACTION
# ============================================================

def extract_two_column_page(
    page,
    blocks,
    column_data
):

    split_x = column_data["split_x"]

    left_blocks = []
    right_blocks = []
    full_width_blocks = []

    for block in blocks:

        if is_full_width_block(
            block,
            float(page.rect.width)
        ):

            full_width_blocks.append(
                block
            )

        elif block["x0"] < split_x:

            left_blocks.append(
                block
            )

        else:

            right_blocks.append(
                block
            )

    left_blocks = sort_blocks(
        left_blocks
    )

    right_blocks = sort_blocks(
        right_blocks
    )

    full_width_blocks = sort_blocks(
        full_width_blocks
    )

    output = []

    # --------------------------------------------------------
    # Top full-width header
    # --------------------------------------------------------

    first_column_y = min(
        [
            block["y0"]
            for block in (
                left_blocks
                + right_blocks
            )
        ],
        default=999999
    )

    top_full_width = []

    remaining_full_width = []

    for block in full_width_blocks:

        if block["y0"] <= first_column_y:

            top_full_width.append(
                block
            )

        else:

            remaining_full_width.append(
                block
            )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    for block in top_full_width:

        for line in block["text"].splitlines():

            line = clean_text(line)

            if line:
                output.append(line)

    # --------------------------------------------------------
    # Left column
    # --------------------------------------------------------

    for block in left_blocks:

        for line in block["text"].splitlines():

            line = clean_text(line)

            if line:
                output.append(line)

    # --------------------------------------------------------
    # Right column
    # --------------------------------------------------------

    for block in right_blocks:

        for line in block["text"].splitlines():

            line = clean_text(line)

            if line:
                output.append(line)

    # --------------------------------------------------------
    # Remaining full-width content
    # --------------------------------------------------------

    for block in remaining_full_width:

        for line in block["text"].splitlines():

            line = clean_text(line)

            if line:
                output.append(line)

    return "\n".join(output)


# ============================================================
# PAGE EXTRACTION
# ============================================================

def extract_page_text(page):

    page_width = float(
        page.rect.width
    )

    blocks = get_text_blocks(
        page
    )

    if not blocks:
        return ""

    # --------------------------------------------------------
    # First determine whether this REALLY looks like
    # a two-column layout.
    # --------------------------------------------------------

    columns = detect_columns(
        blocks,
        page_width
    )

    if columns is None:

        # Normal one-column resume
        return extract_one_column_page(
            page
        )

    # Genuine two-column resume
    return extract_two_column_page(
        page,
        blocks,
        columns
    )


# ============================================================
# OCR
# ============================================================

def extract_page_with_ocr(page):

    try:

        text_page = page.get_textpage_ocr(
            language="eng",
            dpi=200,
            full=True
        )

        text = page.get_text(
            "text",
            textpage=text_page,
            sort=True
        )

        return clean_text(text)

    except Exception as error:

        print(
            "OCR unavailable:",
            repr(error)
        )

        return ""


# ============================================================
# MAIN FUNCTION
# ============================================================

def extract_text_from_pdf(
    pdf_bytes
):

    if not pdf_bytes:

        raise Exception(
            "The uploaded PDF is empty."
        )

    document = None

    try:

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages_text = []

        for page_number, page in enumerate(
            document
        ):

            print(
                f"Processing PDF page "
                f"{page_number + 1}..."
            )

            page_text = extract_page_text(
                page
            )

            # ------------------------------------------------
            # OCR fallback for scanned pages
            # ------------------------------------------------

            if (
                not page_text
                or len(page_text.strip())
                < MIN_TEXT_LENGTH
            ):

                print(
                    f"Page {page_number + 1}: "
                    "little/no selectable text. "
                    "Trying OCR..."
                )

                ocr_text = (
                    extract_page_with_ocr(
                        page
                    )
                )

                if ocr_text:
                    page_text = ocr_text

            if page_text:

                pages_text.append(
                    page_text.strip()
                )

        final_text = "\n\n".join(
            pages_text
        ).strip()

        if not final_text:

            raise Exception(
                "No readable text could be "
                "extracted from the PDF."
            )

        return final_text

    except Exception as error:

        print(
            "PDF extraction error:",
            repr(error)
        )

        raise Exception(
            "Could not extract text from PDF: "
            + str(error)
        )

    finally:

        if document is not None:
            document.close()