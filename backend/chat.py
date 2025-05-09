from generate import call_ollama, build_prompt

class ChatSession:
    def __init__(self, output_format="json", output_type='resume', tone="concise"):
        self.dialogue_history = []
        self.format = output_format
        self.type = output_type
        self.tone = tone


        self.name = None
        self.education = None
        self.skills = None
        self.experience = None
        self.job_description = None
        self.requirement = None
    def set_format(self, fmt):
        self.format = fmt

    def set_tone(self, style):
        self.tone = style

    def set_name(self, name):
        self.name = name

    def set_education(self, edu):
        self.education = edu

    def set_skills(self, skills):
        self.skills = skills

    def set_exp(self, experience):
        self.experience = experience

    def set_jd(self, jd):
        self.job_description = jd

    def set_requirement(self, requirement):
        self.requirement = requirement
    def add_user_input(self, data: dict):
        # support mapping

        for key in ["name", "education", "skills", "experience", "jd", "requirement"]:
            if key in data and data[key] is not None:
                setattr(self, key, data[key])


        self.dialogue_history.append({
            "role": "user",
            "content": data  # 原始字典形式
        })

    def get_bot_response(self):
        # full_dialogue = self._format_dialogue()
        prompt = build_prompt(
            "prompts/dialog_template.txt",
            self.format,
            self.type,
            self.tone,
            self.job_description,
            self.skills,
            self.experience,
            user_info= "".join(["User name", str(self.name), "User Education:", str(self.education)]),
            user_requirements=self.requirement,
        )
        response = call_ollama(prompt)
        self.dialogue_history.append({"role": "bot", "content": response})
        return response

    def _format_dialogue(self):
        formatted_turns = []
        for turn in self.dialogue_history:
            role = turn["role"].capitalize()
            content = turn["content"]
            if isinstance(content, dict):
                content_str = "\n".join(
                    f"{k.replace('_', ' ').title()}: {v}"
                    for k, v in content.items() if v is not None
                )
            else:
                content_str = content
            formatted_turns.append(f"{role}: {content_str}")
        return "\n".join(formatted_turns)

    def undo_last(self):
        if len(self.dialogue_history) >= 2:
            self.dialogue_history.pop()  # bot
            self.dialogue_history.pop()  # user

    def edit_user_turn(self, turn_index, new_text):
        if 0 <= turn_index < len(self.dialogue_history):
            if self.dialogue_history[turn_index]["role"] == "user":
                self.dialogue_history[turn_index]["content"] = new_text

    def regenerate(self):
        if self.dialogue_history and self.dialogue_history[-1]["role"] == "bot":
            self.dialogue_history.pop()
        return self.get_bot_response()

    def reset(self):
        self.dialogue_history = []
        self.format = "bullet point"
        self.tone = "concise"

if __name__ == "__main__":
    # TODO too old don't use
    chat = ChatSession()
    chat.set_format("paragraph")
    chat.set_tone("persuasive")
    chat.format = "json_resume_bullet"  # 让模型以 JSON 返回！

    chat.add_user_input("I'm applying for a machine learning engineer role focused on LLMs.")
    chat.add_user_input("I created a prompt-engineered Q&A bot using LLaMA2.")
    chat.add_user_input("I'm applying for a position as a machine learning researcher.")
    print(chat.get_bot_response())

    chat.add_user_input("I led a project that used BERT to extract insights from customer feedback.")
    print(chat.get_bot_response())

    # 撤销
    chat.undo_last()

    # 替换第一句
    chat.edit_user_turn(0, "I'm applying for a data scientist job in the healthcare industry.")
    print(chat.regenerate())