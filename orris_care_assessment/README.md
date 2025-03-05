# Medical Chatbot with Memory

This project is a medical chatbot that leverages advanced language models and vector databases to provide accurate and context-aware responses to medical queries. The chatbot is built using Streamlit for the user interface, OpenAI's GPT-4o for language processing, and Pinecone for vector storage and retrieval.

## Features

- **Hypothetical Answer Generation**: Uses a language model to generate hypothetical answers based on user queries.
- **Response Synthesis**: Synthesizes responses using embeddings and vector storage to provide accurate answers.
- **Follow-Up Questions**: Generates follow-up questions to engage users and gather more information.
- **Memory**: Maintains conversation history to provide context-aware responses.

## Technologies Used

- **Streamlit**: For building the user interface.
- **OpenAI GPT-4o**: For natural language processing and generating responses.
- **Pinecone**: For vector storage and retrieval.
- **LangChain**: For managing language models and embeddings.
- **dotenv**: For managing environment variables.

## Directory Structure
```
orris_care_assessment/
│
├── agents/
│   ├── __init__.py
│   ├── hyde_agent.py
│   ├── response_agent.py
│   └── followup_agent.py
├── app.py
├── pinecone_util.py
├── requirements.txt
└── README.md
```

### `agents/`

- **hyde_agent.py**: Contains the `HyDEAgent` class for generating hypothetical answers.
- **response_agent.py**: Contains the `ResponseSynthesisAgent` class for synthesizing responses.
- **followup_agent.py**: Contains the `FollowUpQuestionAgent` class for generating follow-up questions.

### `pinecone_util.py`

- Contains the `init_pinecone` function for initializing the Pinecone index.

### `app.py`

- Main application file that sets up the Streamlit interface and integrates all the agents and workflow.

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd orris_care_assessment
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the root directory and add your Pinecone and OpenAI API key and environment:
    ```env
    PINECONE_API_KEY=your_pinecone_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```
    OR create a `.streamlit/secrets.toml`
    ```.streamlit/secrets.toml
    OPENAI_API_KEY = "your_openai_api_key"
    PINECONE_API_KEY = "your_pinecone_api_key"
    ```


4. **Run the application**:
    ```sh
    streamlit run app.py
    ```

## Usage

- Open the Streamlit interface in your browser.
- Enter your medical question in the input field and click "Ask".
- The chatbot will generate a hypothetical answer, synthesize a response, and provide follow-up questions.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.