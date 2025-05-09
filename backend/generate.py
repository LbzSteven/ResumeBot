import requests


def explain_output_format(fmt: str) -> str:
    if fmt == "json_bullet":
        return """Output must be in JSON format:
                ```json
                {
                  "title": "string",
                  "skills": ["skill1", "skill2", ...],
                  "impact": "string",
                  "bullet_point": "string"
                }
                ```"""
    elif fmt == "markdown":
        return """Output should be in Markdown format, e.g.:
            - **Role**: LLM Engineer
            - **Skills**: BERT, Prompt Engineering
            - **Impact**: Improved response accuracy by 30%
            """
    elif fmt == "typst":
        return "Output should be a typst format"
    elif fmt == "plain":
        return "Output should be casual, professional and plain text."
    else:
        return "Output should be readable resume content."


def explain_output_type(type: str) -> str:
    if type == "cover_letter":
        return """cover_letter"""
    elif type == "linkedin_summary":
        return """Output should be in linkedin_summary
            """
    elif type == "resume":
        return "Output should be a resume"

    else:
        return "Output should be readable resume content."


def build_prompt(template_path, output_format, output_type, tone, job_description, skills, experience, user_info,
                 user_requirements):
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    fmt_description = explain_output_format(output_format)
    type_description = explain_output_type(output_type)
    return (
        template.replace("{{output_type}}", output_type)
                .replace("{{output_type_description}} ", type_description)
                .replace("{{output_format}}", output_format)
                .replace("{{output_format_description}}", fmt_description)
                .replace("{{tone}}", tone)
                .replace("{{job_description}}", job_description or "")
                .replace("{{skills}}", skills or "")
                .replace("{{experience}}", experience or "")
                .replace("{{user_info}}", user_info or "")
                .replace("{{user_requirements}}", user_requirements or "")
    )


def call_ollama(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception(f"❗️Error: {response.text}")
