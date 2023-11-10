import os
from typing import List, Literal, Optional

import langchain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel, Field

# langchain.verbose = True


# Define a new Pydantic model with field descriptions and tailored for Physician's Primary Statements.
class PrimaryStatements(BaseModel):
    diagnosis_primary: str = Field(
        description="Primary Diagnosis Provided, Refer to Assessment and plan, Extract ICD-11 Diagnosis Code and Assessment from MD Notes",
        default=None,
    )
    diagnosis_secondary: Optional[str] = Field(
        description="If there is secondary Diagnosis provided, otherwise leave it blank",
        default=None,
    )
    if_childbirth_d: Optional[int] = Field(
        description="If patient is pregnant and provided expected date of delivery, give provided date, only extract date i.e. 1-31.",
        default=None,
        ge=1,
        le=31,
    )
    if_childbirth_m: Optional[int] = Field(
        description="If patient is pregnant and provided expected date of delivery, give provided month, only extract month i.e. 1-12.",
        default=None,
        ge=1,
        le=31,
    )
    if_childbirth_y: Optional[int] = Field(
        description="If patient is pregnant and provided expected date of delivery, give provided year, only extract year e.g. 2023.",
        default=None,
        ge=2021,
        le=2023,
    )
    if_childbirth_method: Literal["Vaginal", "C-Section", None] = Field(
        description="If patient is pregnant and provided expected mode of delivery provide it ",
        default=None,
    )
    whether_occupational_illness: Optional[bool] = Field(
        description="Whether mentioned the illness was triggered due to employer or occupation.",
        default=False,
    )
    start_period_d: int = Field(
        description="Date of first constultation, only extract date i.e. 1-31.",
        default=None,
        ge=1,
        le=31,
    )
    start_period_m: int = Field(
        description="Month of the first consultation, only extract month i.e. 1-12.",
        default=None,
        ge=1,
        le=12,
    )
    start_period_y: int = Field(
        description="Month of the first consultation, only extract month e.g. 2023.",
        default=2023,
        ge=2021,
        le=2023,
    )
    # Skipping First date of abscence due to condition, because filled with last_day_worked + 1.
    has_hospitalized: bool = Field(
        description="Whether patient was hospitalized for given illness", default=False
    )
    date_admitted_d: Optional[int] = Field(
        description="If the patient was hospitalized and provided with date of hospital admission, extract date only i.e. 1-31",
        ge=1,
        le=31,
        default=None,
    )
    date_admitted_m: Optional[int] = Field(
        description="If the patient was hospitalized and provided with date of hospital admission, extract month only i.e. 1-12",
        ge=1,
        le=12,
        default=None,
    )
    date_admitted_y: Optional[int] = Field(
        description="If the patient was hospitalized and provided with date of hospital admission, extract year only e.g. 2023",
        ge=2021,
        le=2023,
        default=None,
    )
    date_discharge_d: Optional[int] = Field(
        description="If the patient was hospitalized and provided with date of hospital discharge, extract date only i.e. 1-31",
        ge=1,
        le=31,
        default=None,
    )
    date_discharge_m: Optional[int] = Field(
        description="If the patient was hospitalized and provided with date of hospital discharge, extract month only i.e. 1-12",
        ge=1,
        le=12,
        default=None,
    )
    date_discharge_y: Optional[int] = Field(
        description="If the patient was hospitalized and provided with date of hospital discharge, extract year only e.g. 2023",
        ge=2021,
        le=2023,
        default=None,
    )
    hospital_name: Optional[str] = Field(
        description="If the patient was hospitalized and provided the name of the institution/hospital that they were admitted in, provide the name of the hospital.",
        default=None,
    )
    had_surgery: bool = Field(description="Whether patient had surgery", default=False)
    surgery_d: Optional[int] = Field(
        description="If the patient had surgery and provided with date of surgery, extract date only i.e. 1-31",
        ge=1,
        le=31,
        default=None,
    )
    surgery_m: Optional[int] = Field(
        description="If the patient had surgery and provided with date of surgery, extract month only i.e. 1-12",
        ge=1,
        le=12,
        default=None,
    )
    surgery_y: Optional[int] = Field(
        description="If the patient had surgery and provided with date of surgery, extract year only e.g. 2023",
        ge=2021,
        le=2023,
        default=None,
    )
    surgery_description: Optional[str] = Field(
        description="If the patient had surgery and provide the short description about surgery in 15 words or less.",
        default=None,
    )
    surgery_anaesthetic: Optional[str] = Field(
        description="If the patient had surgery and provide the type of anaesthics used during the surgery.",
        default="",
    )
    treatment: str = Field(
        description="Summarize the treatment from the MD Notes, mention drugs, dosage, physiotherapy if required and other details.",
        default=None,
    )
    prognosis: str = Field(
        description="Infer from the notes how is the prognosis, use 'Good' by default.",
        default="Good",
    )


def infer_llm(context):
    # print(context)
    # Instantiate the parser with the new model.
    # langchain.debug=True
    parser = PydanticOutputParser(pydantic_object=PrimaryStatements)

    # Update the prompt to match the new query and desired format.
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "Fill up following LOA form from given context. \n Context: \n {context} \n{format_instructions}\n{question}"
            )
        ],
        input_variables=["question", "context"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )
    chat_model = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3,
    )
    # Generate the input using the updated prompt.
    user_query = (
        "Be specific, only use context to find the answers for fields. Do not make information up."
        "Follow the schema provided."
    )
    _input = prompt.format_prompt(question=user_query, context=context)

    output = chat_model(_input.to_messages())
    parsed = parser.parse(output.content)
    # print(output.content)
    # print(parsed)
    return parsed
