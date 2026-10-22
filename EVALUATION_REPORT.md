\# Evaluation Report



\## Project

Enterprise Policy \& SOP Intelligence Assistant



\## Dataset

\- Seven policy and SOP PDF documents

\- Eight question-based test cases

\- Six answerable cases

\- Two abstention cases



\## Results



\### Retrieval

\- Expected-source checks passed: 6/6

\- Initial observed result: 100% on the six answerable cases



This result is limited to the prepared dataset and is not a general retrieval-accuracy guarantee.



\### Answer Evaluation

\- Automated checks passed: 5

\- T04: pending automated verification

\- T04 encountered a Gemini 503 UNAVAILABLE response.



The service error does not establish that the generated answer was incorrect. A policy comparison was also tested manually through the application.



\### Abstention

\- Two cases manually tested

\- Both behaved as expected in the observed tests



\### Application Testing

\- Three functional questions tested through Streamlit

\- All three generated expected answers



\### Citation Metadata

\- Offline document metadata validation: passed

\- Referenced PDF files and page numbers were validated against the available documents.



This check does not prove that the cited passages support every claim in an answer.



\## Limitations

\- Small evaluation dataset

\- Preliminary keyword-based answer checks

\- One automated answer case pending

\- No comprehensive claim-level grounding evaluation yet



\## Next Steps

1\. Retry T04 when the model service is available.

2\. Manually verify generated answers against source passages.

3\. Expand the evaluation dataset.

4\. Add regression tests and more robust error handling.



