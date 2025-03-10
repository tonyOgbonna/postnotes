## Project Specification
Create a Streamlit based application that would take a YouTube video url, get the transcript, process the transcript using an LLM according to system instructions to the LLM, format the output as a structured Obsidian markdown, and store the output in a given folder within an Obsidian vault. It should be configurable, featuring a main page and a setting page. The configurable elements should include: the LLM model, system instruction, the output folder within Obsidian vault to save the output file.

Within the given Obsidian Vault it should check for a folder name same as the safe name of the YouTube video channel, if it exists save the result in that folder. If it doesn't create the folder then save the result there.

The available system instructions should be in the form of markdown files stored in a particular folder with the application folder. Each system instruction is identified within the app by their file name.