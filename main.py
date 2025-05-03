#!/usr/bin/env python

import argparse
import os
from dotenv import load_dotenv
from anthropic import Anthropic

from srtgpt.translator import translate

load_dotenv()


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
    for text in translate(
       args.filename,
       args.language,
       args.chunk_size,
       args.max_tokens,
       args.model,
       anthropic,
    ):
        print(text, end=None, flush=True)


if __name__ == "__main__":
    main()

