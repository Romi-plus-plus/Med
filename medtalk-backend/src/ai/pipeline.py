from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pprint import pprint
from typing import TYPE_CHECKING, overload

from ai.slu.nlp import SimpleNLP

from .config import settings
from .logging import logger

logger.info("Start pipeline")

from .kgqa.answer import Answer, AnswerResult

if TYPE_CHECKING:
    from .slu.detector import DetectResult


@dataclass
class PipelineResult:
    detection: DetectResult
    tags: list[str]
    marked_input: str
    answers: list[AnswerResult]
    fallback_answer: str | None = None


def mark_question(det: DetectResult) -> str:
    marked = det.text
    for s in reversed(det.slots):
        p = det.token_pos[s.pos[0]]
        q = p + len(s.text)
        marked = f"{marked[:p]}<a>{marked[p:q]}</a>{marked[q:]}"
    return marked


class MedQAPipeline:
    def __init__(self) -> None:
        logger.info("Init MedQAPipeline")
        logger.info("Loading model async.")
        self.load_model_task = asyncio.ensure_future(self._load_model())
        self.nlp = SimpleNLP()
        self.answerer = Answer()
        logger.info("OK.")

    async def _load_model(self):
        from .slu.detector import JointIntentSlotDetector

        self.detector = JointIntentSlotDetector.from_pretrained(
            model_path=settings.MODEL_PATH,
            tokenizer_path=settings.TOKENIZER_PATH,
            intent_label_path=settings.INTENT_LABEL_PATH,
            slot_label_path=settings.SLOT_LABEL_PATH,
        )
        logger.info("Model loading done")

    async def pipeline(self, question: str) -> PipelineResult:
        """Put the question through the pipeline. Detect intent and slots, search for answers."""
        await self.load_model_task
        res = self.detector.detect(question)
        logger.info(res)
        answers = (
            [self.answerer.create_answer(res.intent, r.text) for r in res.slots]
            if res.intent != "[UNK]"
            else []
        )
        logger.info(answers)  # 如果为空，考虑加一个

        fallback_answer = None
        if res.intent == "[UNK]":
            fallback_answer = self.answerer.get_answer_unk()
        elif not answers:
            fallback_answer = self.answerer.get_answer_none()

        return PipelineResult(
            detection=res,
            tags=self.nlp(question),
            marked_input=mark_question(res),
            answers=answers,
            fallback_answer=fallback_answer,
        )

    @overload
    async def __call__(self, question: str) -> PipelineResult:
        ...

    @overload
    async def __call__(self, question: list[str]) -> list[PipelineResult]:
        ...

    async def __call__(self, question: str | list[str]):
        if isinstance(question, list):
            return await asyncio.gather(*list(map(self.pipeline, question)))
        return await self.pipeline(question)


async def main():
    pipeline = MedQAPipeline()
    while True:
        text = input("input: ")
        pprint(await pipeline(text), width=120)


if __name__ == "__main__":
    asyncio.run(main())
