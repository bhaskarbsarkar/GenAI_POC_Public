import warnings
warnings.filterwarnings('ignore')

import json
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os

load_dotenv()

class LinkedinCrew:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME')
        
        with open("agent/post_types_param.json", "r") as file:
            self.post_type_param = json.load(file)
        with open("agent/prompt_example.txt", "r") as file:
            self.example = file.read()

    def prepare_crew(self, content_type):

        self.copywriter = Agent(
                role="Senior LinkedIn Copywriter",
                goal=self.post_type_param[content_type]['copywriter']["goal"],
                backstory=self.post_type_param[content_type]['copywriter']["backstory"],
                allow_delegation=False,
                verbose=True
            )

        self.editor = Agent(
            role="Senior Editor",
            goal=self.post_type_param[content_type]['editor']["goal"],
            backstory=self.post_type_param[content_type]['editor']["backstory"],
            allow_delegation=False,
            verbose=True
        )

        self.write_task = Task(
            description=(
                self.post_type_param[content_type]['write_task']["description"]
            ),
            expected_output=self.post_type_param[content_type]['write_task']["expected_output"],
            agent=self.copywriter,
        )

        self.edit_task = Task(
            description=(
                self.post_type_param[content_type]['edit_task']["description"]
            ),
            expected_output=self.post_type_param[content_type]['edit_task']["expected_output"],
            agent=self.editor
        )

        self.crew = Crew(
            agents=[self.copywriter, self.editor],
            tasks=[self.write_task, self.edit_task],
            verbose=True
        )
    
        return self.crew 
    
    def generate_normal_post(self, content):
        inputs = {
            "content": content,
            "example": self.example
        }
        final_crew = self.prepare_crew(content_type="normal_post")
        result = final_crew.kickoff(inputs=inputs)
        return str(result)
    
    def generate_tool_demo_post(self, content):
        inputs = {
            "content": content,
            "example": self.example
        }
        final_crew = self.prepare_crew(content_type="tool_demo")
        result = final_crew.kickoff(inputs=inputs)
        return str(result)

    def generate_hooks(self, content):
        inputs = {
            "content": content
        }
        final_crew = self.prepare_crew(content_type="hook_gen")
        result = final_crew.kickoff(inputs=inputs)
        return str(result)

    def generate_comments(self, content):
        inputs = {
            "content": content
        }
        final_crew = self.prepare_crew(content_type="comment_gen")
        result = final_crew.kickoff(inputs=inputs)
        return str(result)
