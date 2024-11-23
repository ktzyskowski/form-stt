import json
from typing import Optional, IO

import streamlit as st
from pydantic import BaseModel, Field

import formstt.form_service


# ==================================================================================================================== #
# FORM SERVICE
# ==================================================================================================================== #


class FormParameters(BaseModel):
    first_name: Optional[str] = Field(description="The user's first name")
    last_name: Optional[str] = Field(description="The user's last name")
    email: Optional[str] = Field(description="The user's email address")
    phone: Optional[str] = Field(description="The user's phone number")
    age: Optional[int] = Field(description="The user's age")
    mailing_list: Optional[bool] = Field(description="Boolean to sign up for mailing list")


form_service = formstt.form_service.FormService(
    api_key="YOUR KEY HERE",
    form_parameters=FormParameters
)

# ==================================================================================================================== #
# SESSION STATE
# ==================================================================================================================== #


# session state holds form data
if "form_state" not in st.session_state:
    st.session_state.form_state = dict(FormParameters(
        first_name="", last_name="", email="", phone="", age=18, mailing_list=False
    ))


def update_from_audio(audio: IO[bytes]):
    """Update the session state form data from an audio file.

    :param audio: the audio file bytes.
    :return: None
    """
    with st.spinner("Processing"):
        raw_response = form_service.from_audio(audio)
    response = json.loads(raw_response)
    for key in response:
        if response[key]:
            st.session_state.form_state[key] = response[key]


# ==================================================================================================================== #
# USER INTERFACE
# ==================================================================================================================== #


# Component to record audio. On completion, update form data.
audio_file = st.audio_input("Record your form inputs here...")
if audio_file:
    update_from_audio(audio_file)

# Form component. This reads values from session state form data so it can be filled in by LLM.
with st.form("my_form"):
    form_state = st.session_state.form_state

    st.write("Example Contact Form")

    first_name = st.text_input("First Name", value=form_state["first_name"])
    last_name = st.text_input("Last Name", value=form_state["last_name"])
    email = st.text_input("Email", value=form_state["email"])
    phone_number = st.text_input("Phone Number", value=form_state["phone"])
    age = st.slider("Age", 0, 100, value=form_state["age"])
    send_emails = st.checkbox("Sign up for our mailing list!", value=form_state["mailing_list"])

    submitted = st.form_submit_button("Submit")
