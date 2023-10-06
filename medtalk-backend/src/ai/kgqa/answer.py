import random
from dataclasses import dataclass
from operator import itemgetter
from typing import Any

from more_itertools import first

from .search import Search


@dataclass
class AnswerResult:
    entity: str
    items: list[str]
    text: str
    marked_text: str


def mark_answer(text: str):
    return text.replace("\n", "<br>")


class Answer:
    def __init__(self) -> None:
        self.searcher = Search()
        self.answer_formats = {
            "Symptom_accompany": ["{0}的并发症有：{1}等", "{0}可能会并发这些不适应症状：{1}", "{1}是{0}的并发症"],
            "Symptom_cause": ["{0}可能的成因有以下几种：{1}", "{0}的可能原因大致为：{1}", "{0}有以下几种原因{1}"],
            "Symptom_lasttime":["症状持续时间{0}"],
            "Symptom_check": ["出现{0}应该检查{1}等项目", "出现{0}应该做这些检查：{1}", "{0}需要的检查有：{1}等项目"],
            "Symptom_solprob": [
                "{0}问题解决的概率约为：{1}",
                "解决好{0}的概率约为：{1}",
            ],
            "Symptom_solway": ["{0}的解决方式有：{1}", "{0}可以采取的解决方式有：{1}"],
            
            "Device_usage_desc": ["{0}的简介：{1}", "{0}的相关信息如下：{1}", "{0}的主要特征为：{1}"],
            "soft_error_desc": ["{0}的简介：{1}", "{0}的相关信息如下：{1}", "{0}的主要特征为：{1}"],
            "soft_support_desc": ["{0}的简介：{1}", "{0}的相关信息如下：{1}", "{0}的主要特征为：{1}"],
            "Device_support_desc": ["{0}的简介：{1}", "{0}的相关信息如下：{1}", "{0}的主要特征为：{1}"],
           
            "Device_support_prevent": ["{0}的预防措施有：{1}", "预防{0}可以做这些措施：{1}", "可以采用以下方法：{1}来预防{0}"],
            "soft_error_prevent": ["{0}的预防措施有：{1}", "预防{0}可以做这些措施：{1}", "可以采用以下方法：{1}来预防{0}"],
            "device_Symptom": ["设备的{0}情况会导致的不适应症状有：{1}", "{0}症状可能预示着这些设备出现{1}"],
        }
        self.answer_fallback = ["暂时没有{0}相关信息"]
        self.answer_none = ["您的问题并不明确，请换个问法再说一遍，谢谢。"]
        self.answer_unk = [
            "您的问题好像超出了我的回答范围，请问一个合适的问题",
            "我是耳动设备问答机器人，没有其他领域的知识哦",
        ]

    def search_answer(self, question_type: str, entity: str) -> list[dict[str, Any]]:
        """根据问题类型调用Search类查询neo4j数据库，并将直接查询结果返回"""
        match question_type:
            case "Symptom_cause":  # 查询不适应症状的原因
                return self.searcher.entity(entity, "cause")
            case "Device_support_prevent":  # 查询设备保护性预防措施
                return self.searcher.entity(entity, "Device_support")
            case "soft_error_prevent":  # 查询软件保护性预防措施
                return self.searcher.entity(entity, "soft_error")
            case "Device_usage_desc":  # 查询介绍
                return self.searcher.entity(entity, "dec")
            case "soft_error_desc":    # 查询介绍
                return self.searcher.entity(entity, "dec")
            case "soft_support_desc":  # 查询介绍
                return self.searcher.entity(entity, "dec")
            case "Device_support_desc":# 查询介绍
                return self.searcher.entity(entity, "dec")         
            case "Symptom_lasttime":  # 查询不适应症状的持续时间
                return self.searcher.entity(entity, "sym_lasttime")
            case "Symptom_solprob":  # 查询不适应症状的解决概率
                return self.searcher.entity(entity, "sol_prob")
            case "Symptom_solway":  # 查询不适应症状的治疗方式
                return self.searcher.entity(entity, "sol_way")
            case "Symptom_symptom":  # 查询不适应症状归类
                return self.searcher.entity_relation(entity, "has_symptom")
            case "Symptom_accompany":  # 查询不适应症状的并发症
                return self.searcher.entity_relation(entity, "accompany_with")
            case "Symptom_check":  # 查询不适应症状应该进行的检查
                return self.searcher.entity_relation(entity, "need_check")
        print("Unknown", question_type)
        assert False

    def extract_search_results(self, answers: list[dict[str, Any]]) -> list[str]:
        if not answers:
            return []
        if "y.name" in answers[0]:
            # 一堆{x.name, y.name}
            return list(map(itemgetter("y.name"), answers))
        else:
            key = first((k for k in answers[0].keys() if k != "x.name"))
            val = answers[0][key]
            return val if isinstance(val, list) else [val]

    def create_answer(self, question_type: str, entity: str) -> AnswerResult:
        """调用serach_answer函数，获得查询结果，依据结果生成对应的自然语言回答的字符串"""
        results = self.search_answer(question_type, entity)
        extracted = self.extract_search_results(results)
        txt = (
            random.choice(self.answer_formats[question_type]).format(entity, "、".join(extracted))
            if extracted
            else random.choice(self.answer_fallback).format(entity)
        )
        return AnswerResult(entity=entity, items=extracted, text=txt, marked_text=mark_answer(txt))

    def create_answer_multi(self, question_type: str, entitys: list[str]) -> list[AnswerResult]:
        return [self.create_answer(question_type, entity) for entity in entitys]

    def get_answer_none(self):
        return random.choice(self.answer_none)
    
    def get_answer_unk(self):
        return random.choice(self.answer_unk)


if __name__ == "__main__":
    a = Answer()
