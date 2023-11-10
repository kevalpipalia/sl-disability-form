# AI-Powered Automation for SunLife Short Term Disability Forms

## Project Overview

### Purpose
This project explores the innovative application of AI, specifically using GPT, to automate the completion of SunLife Short Term Disability (SL STD) forms. Our primary objective is to reduce operational costs, save time for healthcare practitioners, and significantly lower expenses for members. Typically, members incur a cost of approximately $80 per form when completed by a practitioner. Our solution aims to mitigate these costs effectively.


### Methodology
The system leverages context derived from Mental Health Services (MHS), Medical Doctor (MD), and Psychological (PSY) notes to accurately fill out the fields in the SUNLIFE STD FORM. To ensure reliability and minimize the risk of inaccurate information ('hallucinations'), the system is programmed to extract relevant data directly from these contextual notes.

#### Implementing Constrained AI Responses
To further refine the AI's output and ensure consistency, we employ pydantic parsing with constrained instructions. This approach guarantees that the AI's responses adhere strictly to the predefined pydantic model, thus enhancing the accuracy and reliability of the completed forms. For a detailed view of the implementation, refer to the `api/llmoperations.py` in our repository.

