# form-stt

This repository holds the submission for my Class Project #3. This program is an example of applying LLMs to assist in
completing web forms using natural language (audio).

### Install

The only packages used in this repository are `streamlit` for the UI and `openai` for the LLM audio/text completions.

```shell
pip install -U streamlit openai
```

### Usage

> Warning! You need to provide your OPENAI_API_KEY in `streamlit_app.py` when instantiating the form service in order to
> make this application work.

To run the application, use the following command from the project root. As always, its recommended to make a virtual
environment to hold packages.

```shell
streamlit run streamlit_app.py
```

### Writeup and Video Demo

The written portion of this assignment can be found in the file `writeup.pdf` and the video demo showcasing the
functionality of the application can be found in `demo-video.mov`.