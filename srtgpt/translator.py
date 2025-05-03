import srt
from typing import Iterator
from anthropic import Anthropic


PROMPT_TEMPLATE = """
Translate these subtitles into {language}. Do not change the timestamps too much, and make sure the lines match them.
Keep the segment indexes and any other tags intact. Respond only with the translated subtitles in SRT format and nothing else.

Here's the subtitles:
```srt
{srt_content}
```
"""


def parse_ai_response(text: str) -> str:
    srt_start = text.find("```srt")
    srt_end = text.rfind("```")

    raw_srt = text
    if srt_start >= 0 and srt_end >= 0:
        raw_srt = text[srt_start + 6:srt_end]

    # ensure the response can be parsed as valid SRT
    srt.parse(raw_srt)

    return raw_srt.strip()


def translate(
    filename: str,
    language: str,
    chunk_size: int,
    max_tokens: int,
    model: str,
    anthropic: Anthropic,
) -> Iterator[str]:
    with open(filename) as f:
        subtitles = list(srt.parse(f.read()))

    for i in range(0, len(subtitles), chunk_size):
        chunk = subtitles[i:i + chunk_size]

        srt_content = srt.compose(chunk, start_index=i + 1).strip()

        prompt = PROMPT_TEMPLATE.format(srt_content=srt_content, language=language).strip()

        message = anthropic.messages.create(
            max_tokens=max_tokens,
            model=model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        if i > 0:
            print()

        for content in message.content:
            yield parse_ai_response(content.text)

