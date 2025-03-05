from langchain.schema import HumanMessage

class FollowUpQuestionAgent:
    def __init__(self, llm):
        """
        Initialize the FollowUpQuestionAgent with a language model.
        
        Args:
            llm (ChatOpenAI): The language model to use for generating follow-up questions.
        """
        self.llm = llm

    def generate_follow_up_questions(self, state):
        """
        Generate follow-up questions based on the synthesized answer in the state.
        
        Args:
            state (dict): The current state containing the synthesized answer.
        
        Returns:
            dict: Updated state with the follow-up questions.
        """
        prompt = (
            f"Given the query\n\n'{state["query"]}' and the answer\n\n'{state["synthesized_answer"]}', "
            "\n\nSuggest 3 relevant follow-up questions WITHOUT PREAMBLE."
        )
        response = self.llm([HumanMessage(content=prompt)])

        return {'follow_up_questions': response.content.split("\n")}
