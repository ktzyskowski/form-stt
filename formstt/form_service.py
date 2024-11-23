from typing import Type, IO

import openai
from pydantic import BaseModel


class FormService:
    def __init__(self, api_key: str, form_parameters: Type[BaseModel]):
        self._client = openai.OpenAI(
            api_key=api_key
        )
        self._form_tool = openai.pydantic_function_tool(
            form_parameters,
            name="form_filler",
            description="Fill out the parameters of this form with information provided by the user."
        )

    def from_audio(self, audio: IO[bytes]):
        transcript = self._client.audio.transcriptions.create(
            model="whisper-1",
            file=audio
        )
        return self.from_text(transcript.text)

    def from_text(self, transcript: str):
        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": ""
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ],
            tools=[self._form_tool],
            tool_choice="required"
        )
        return response.choices[0].message.tool_calls[0].function.arguments
