#!/usr/bin/env python

import argparse
import math
import srt
import os
from typing import List
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()


PROMPT_TEMPLATE = """
Translate these subtitles into {language}. Do not change the timestamps too much, and make sure the lines match them.
Keep the segment indexes and any other tags intact. Respond only with the translated subtitles in SRT format and nothing else.

Here's the subtitles:
```srt
{srt_content}
```
"""


def main():
    api_key = os.getenv("ANTHROPIC__API_KEY")
    if api_key is None:
        raise ValueError("Please specify an Anthropic API key by creating an .env file or passing it directly")

    anthropic = Anthropic(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Path to the SRT file to translate")
    parser.add_argument("language", help="The language to translate to")
    parser.add_argument("--chunk-size", "-n", help="Number of subtitle lines to translate at once", default=20)
    parser.add_argument("--model", "-m", help="The Anthropic model name to use", default="claude-3-5-haiku-20241022")
    parser.add_argument("--max-tokens", "-t", help="The maximum number of output tokens", default=4000)

    args = parser.parse_args()
    with open(args.filename) as f:
        subtitles = list(srt.parse(f.read()))

    for i in range(0, len(subtitles), args.chunk_size):
        chunk = subtitles[i:i+args.chunk_size]

        srt_content = srt.compose(chunk, start_index=i+1).strip()

        prompt = PROMPT_TEMPLATE.format(srt_content=srt_content, language=args.language).strip()

        message = anthropic.messages.create(
            max_tokens=args.max_tokens,
            model=args.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        if i > 0:
            print()

        for content in message.content:
            print(content.text, end=None, flush=True)

if __name__ == "__main__":
    main()

