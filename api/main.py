# import json
# import os

# import fillpdf
# import uvicorn
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse, HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fillpdf import fillpdfs

# from key_mappings import mapping_dict
# from llmoperations import PrimaryStatements, infer_llm

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.get("/")
# def read_root():
#     with open("static/index.html", "r") as file:
#         html_content = file.read()
#     return HTMLResponse(content=html_content, status_code=200)


# @app.get("/generate_pdf")
# def generate_pdf():
#     try:
#         generated_pdf_path = annotate_forms()
#         if os.path.exists(generated_pdf_path):
#             return FileResponse(
#                 path=generated_pdf_path,
#                 filename="filled-sunlife.pdf",
#                 media_type="application/pdf",
#             )
#         else:
#             raise FileNotFoundError
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# def annotate_forms():
#     # fields = fillpdfs.get_form_fields("input-forms/blank_format.pdf")
#     # print(fields)
#     output_path = "filled-out.pdf"
#     member_details = get_user_details("member-details.json")
#     phy_statement_1 = get_primary_statement("context.txt")
#     provider_details = get_user_details("provider-details.json")
#     final_update = {**member_details, **phy_statement_1, **provider_details}
#     fillpdfs.write_fillable_pdf(
#         "input-forms/blank_format.pdf", output_path, final_update
#     )
#     return output_path


# def get_user_details(filepath):
#     f = open(filepath)
#     user_details = json.load(f)
#     f.close()
#     return user_details


# def get_primary_statement(contextpath):
#     with open("context.txt", "r") as f:
#         context = f.read()
#         f.close()
#     generated_fields = infer_llm(context)
#     aligned_generated_fields = match_generated_content_with_template_fields(
#         generated_fields
#     )
#     return aligned_generated_fields


# def match_generated_content_with_template_fields(content: PrimaryStatements):
#     serialized_content = content.model_dump(exclude_none=True)
#     swapped_dict = {
#         mapping_dict[key]: value
#         for key, value in serialized_content.items()
#         if key in mapping_dict
#     }
#     swapped_dict = {
#         key: None if value is True else "Female" if value is False else value
#         for key, value in swapped_dict.items()
#     }
#     return swapped_dict


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")


import json
import os

import fillpdf
from fillpdf import fillpdfs
from flask import Flask, abort, render_template, send_file, send_from_directory

from api.key_mappings import mapping_dict
from api.llmoperations import PrimaryStatements, infer_llm

app = Flask(__name__)


@app.route("/")
def read_root():
    try:
        return render_template("index.html")
    except Exception as e:
        abort(500, description=str(e))


@app.route("/generate_pdf")
def generate_pdf():
    try:
        generated_pdf_path = annotate_forms()
        if os.path.exists(generated_pdf_path):
            return send_file(generated_pdf_path, as_attachment=True)
        else:
            abort(404, "Generated PDF file not found")
    except Exception as e:
        abort(500, description=str(e))


def annotate_forms():
    # fields = fillpdfs.get_form_fields("input-forms/blank_format.pdf")
    # print(fields)
    output_path = "/tmp/filled-out.pdf"
    member_details = get_user_details("api/member-details.json")
    phy_statement_1 = get_primary_statement("api/context.txt")
    provider_details = get_user_details("api/provider-details.json")
    final_update = {**member_details, **phy_statement_1, **provider_details}
    fillpdfs.write_fillable_pdf(
        "api/input-forms/blank_format.pdf", output_path, final_update
    )
    return output_path


def get_user_details(filepath):
    f = open(filepath)
    user_details = json.load(f)
    f.close()
    return user_details


def get_primary_statement(contextpath):
    with open(contextpath, "r") as f:
        context = f.read()
        f.close()
    generated_fields = infer_llm(context)
    aligned_generated_fields = match_generated_content_with_template_fields(
        generated_fields
    )
    return aligned_generated_fields


def match_generated_content_with_template_fields(content: PrimaryStatements):
    serialized_content = content.model_dump(exclude_none=True)
    swapped_dict = {
        mapping_dict[key]: value
        for key, value in serialized_content.items()
        if key in mapping_dict
    }
    swapped_dict = {
        key: None if value is True else "Female" if value is False else value
        for key, value in swapped_dict.items()
    }
    return swapped_dict


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
