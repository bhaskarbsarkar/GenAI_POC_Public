from langchain.schema import HumanMessage

class ResponseSynthesisAgent:
    def __init__(self, pc_index, embedding, llm):
        """
        Initialize the ResponseSynthesisAgent with a language model, embeddings, and Pinecone index.
        
        Args:
            llm (ChatOpenAI): The language model to use for synthesizing responses.
            embedding (OpenAIEmbeddings): The embeddings to use for vector representation.
            pc_index (Index): The Pinecone index for storing and retrieving vectors.
        """
        self.pc_index = pc_index
        self.embedding = embedding
        self.llm = llm

    def synthesize_response(self, state):
        """
        Synthesize a response based on the hypothetical answer in the state.
        
        Args:
            state (dict): The current state containing the hypothetical answer.
        
        Returns:
            dict: Updated state with the synthesized answer.
        """
        context_dict = []
        query_vector = self.embedding.embed_query(state["hypothetical_answer"])
        results = self.pc_index.query(vector=query_vector, top_k=5, include_metadata=True, include_values=True)
        
        for res in results.matches:
            per_context = "Book and Page Info:\n" + res.id + "\n\n" + res.metadata["bullet_points"]
            context_dict.append(per_context)

        context = "\n\n".join(context_dict)
        prompt = ("The below is the conversation history happened between you and user."
                  "If it's empty, treat it as a fresh conversation else take the history into account for answering the user query."
                  f"\n\n###Chat History in Json format:\n\n{state["chat_history"]}\n\nNow,"
            f"Given the query\n\n'{state["query"]}'\n\nand the context\n\n'{context}',"
            "provide the a detailed answer to the query in less than 300 tokens with NO PREAMBLE."
            "Stick to the context only. If the query doesnot align with the context, strictly reply that you cannot answer"
            "STRICTLY PROVIDE REFERENCE NUMBER NOTATION at the end of a line and REFERENCE LIST at the end of response by referring the book title and page number."
        )
        response = self.llm([HumanMessage(content=prompt)])
        return {"synthesized_answer": response.content}
