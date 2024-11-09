# diane

The following is a small script that is intended to be run through Termux in my Android phone. It records the voice, sends the recording back to OpenAI's Whisper to get the transcript, runs the transcript in a function call to an LLM to extract the information of an expense and then later on it saves that information back in a CSV that I have in my phone locally in an Obsidian vault.

to install pandas, run:
```
pkg i tur-repo
pkg i python-pandas
```
([reference](https://stackoverflow.com/a/77446476))

For the openai client I did it through pip and I ran into problems with rust I think, so I had to install rust first.