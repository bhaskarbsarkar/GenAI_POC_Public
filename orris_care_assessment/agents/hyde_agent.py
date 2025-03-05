from langchain.schema import HumanMessage

class HyDEAgent:
    def __init__(self, llm):
        """
        Initialize the HyDEAgent with a language model.
        
        Args:
            llm (ChatOpenAI): The language model to use for generating hypothetical answers.
        """
        self.llm = llm

    def generate_hypothetical_answer(self, state):
        """
        Generate a hypothetical answer based on the query in the state.
        
        Args:
            state (dict): The current state containing the query.
        
        Returns:
            dict: Updated state with the hypothetical answer.
        """
        prompt = (f"The below is the conversation history happened between you and user."
                  "If it's empty, treat it as a fresh conversation else take the history into account for answering the user query.\n\n"
                  f"###Chat History in Json format:\n\n{state["chat_history"]}\n\n"
                  f"Now, generate a detailed 5 line medical document answering user query: \n\n{state["query"]}"
                )
        response = self.llm([HumanMessage(content=prompt)])
        return {"hypothetical_answer": response.content}
