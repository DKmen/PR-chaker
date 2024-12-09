from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings


class LLM_Analysis:
    def __init__(self, model):
        model = OllamaLLM(
            model=model, format="json", temperature=0.1, base_url=settings.ollama_url
        )
        prompt = ChatPromptTemplate.from_template(
            """
                your role is to code analyser of PR request

                As a code analyser your task is below
                    - Code style and formatting issues
                    - Potential bugs or errors
                    - Performance improvements
                    - Best practices
                
                file content:{file_content}
                file changes:{file_changes}

                For this we provide you file content and changes of that file base on that content you analyse code and provide more then 1 analysis in responce in below Output Template format
                
                Output Template:
                [{{
                    "type": "type of issue [bug,style,error,performance]",
                    "line": line number of code which this analyze provide,
                    "description": "description of problem",
                    "suggestion": "give suggetion to solve that issue"
                }} ,
                {{
                    "type": "type of issue [bug,style,error,performance]",
                    "line": line number of code which this analyze provide,
                    "description": "description of problem",
                    "suggestion": "give suggetion to solve that issue"
                }}
                ]
            """
        )

        self.chain = prompt | model

    def analyze(self, file_content, file_changes):
        return self.chain.invoke(
            {"file_content": file_content, "file_changes": file_changes}
        )
