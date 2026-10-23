\# Enterprise Policy \& SOP Intelligence Assistant



An AI-powered application that helps users query enterprise policy and Standard Operating Procedure (SOP) documents using Retrieval-Augmented Generation (RAG).



\## Project Overview



Enterprise organizations maintain policies and procedures across multiple PDF documents. Finding the right information manually can be time-consuming.



This project explores how RAG can retrieve relevant policy passages and use them to generate answers grounded in approved documents, with document and page references.



\## Key Features



\- PDF-based knowledge ingestion

\- Text extraction and chunking

\- Semantic retrieval of relevant document passages

\- Gemini-powered answer generation

\- Comparison of policy versions

\- Abstention when the available context does not support an answer

\- Source and page references derived from retrieved metadata

\- Streamlit web interface

\- Initial retrieval and answer evaluation



\## Technology Stack



\- Python

\- Streamlit

\- Google Gemini API

\- PyMuPDF

\- Retrieval-Augmented Generation (RAG)

\- Semantic search



\## Architecture



PDF Policy Documents  

↓  

Text Extraction  

↓  

Text Chunking and Metadata  

↓  

Semantic Retrieval  

↓  

Relevant Context  

↓  

Gemini Answer Generation  

↓  

Answer and Source References  

↓  

Streamlit Interface



\## Evaluation Results



Initial evaluation using eight question-based test cases:



\- Retrieval: 6 of 6 answerable cases passed expected-source checks.

\- Automated answer checks: 5 passed.

\- Policy comparison test T04: automated evaluation pending following a Gemini 503 service-availability error.

\- Abstention: 2 manually tested cases passed.

\- Streamlit functional testing: 3 questions generated expected answers.

\- Citation metadata validation: passed.



These are preliminary results on a small test set. Keyword checks and metadata validation do not independently establish factual accuracy or claim-level groundedness.



\## Project Structure



```text

AI\_Enterprise\_Policy\_Assistant/

├── app.py

├── rag.py

├── semantic\_search.py

├── evaluate.py

├── evaluate\_answers.py

├── validate\_citations.py

├── evaluation\_dataset.json

├── EVALUATION\_REPORT.md

├── Documents/

├── Knowledge/

├── .env

├── .gitignore

└── README.md

```



The file list above describes the principal project files. Update it if your actual directory structure differs.



\## Setup



1\. Install Python and create a virtual environment.

2\. Install the required Python packages:



&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



3\. Create a `.env` file in the project root and add your Gemini API key:



&#x20;  ```text

&#x20;  GEMINI\_API\_KEY=your\_gemini\_api\_key

&#x20;  ```



4\. Place permitted test policy PDFs in the `Documents/` folder.

5\. Generate knowledge chunks and metadata:



&#x20;  ```bash

&#x20;  python document\_processor.py

&#x20;  ```



&#x20;  This creates `Knowledge/chunks.json` from the PDFs.



6\. Build the ChromaDB vector store:



&#x20;  ```bash

&#x20;  python embedding\_store.py

&#x20;  ```



&#x20;  This generates embeddings for the chunks and stores them in `Knowledge/chroma\_db/`. A valid Gemini API key and internet access are required.



7\. Start the application:



&#x20;  ```bash

&#x20;  streamlit run app.py

&#x20;  ```



Keep API keys and confidential documents out of public repositories. Use only policy documents you are permitted to process and share.



\## Known Limitations



\- Evaluation uses a small, manually prepared dataset.

\- Keyword matching is only a preliminary answer check.

\- Citation metadata validation does not prove that every answer claim is supported.

\- Model availability and API quotas may affect answer generation.

\- Further testing is required before production use.



\## Future Improvements



\- Claim-level grounding evaluation

\- Better retrieval relevance metrics

\- Automated regression testing

\- Policy version comparison evaluation

\- Improved handling of model service errors

\- Enterprise access controls and audit logging



\## Responsible AI



This is a learning and portfolio project. Generated answers should be checked against authoritative policies before being used to make operational or compliance decisions.



