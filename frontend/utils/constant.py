from typing import Tuple, Any



fmt_option = [
    "Markdown",
    "JSON bullets",
    "Typst",
    "Plain",
]
generate_option = [
    "Resume",
    "CV",
    "LinkedIn Summary",
]

education_option = ["Undergraduate", "Master", "Doctoral"]
tone_option = ["concise", "detailed", "persuasive"]


def normalize_generate_type(fmt: str, generate_type: str) -> tuple[str, str]:
    format_map = {
        "JSON bullets": "json_bullet",
        "Markdown": "markdown",
        "Typst": "typst",
        "Plain": "plain"
    }
    generate_option_map = {
        "Cover Letter": "cover_letter",
        "LinkedIn Summary": "linkedin_summary",
        "Resume": "resume"
    }
    return format_map[fmt], generate_option_map[generate_type]
