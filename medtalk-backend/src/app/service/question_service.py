from typing import Type

from sqlmodel.ext.asyncio.session import AsyncSession

from aiapp import crud
from aiapp.models import BaseCount, EntityCount, IntentCount, WordCount


async def make_dict(db: AsyncSession, model: Type[BaseCount], trans: dict[str, str] | None = None):
    if trans is None:
        trans = {}
    res = await crud.counter.get_tops(db, model, 100)
    return {trans.get(c.key, c.key): c.value for c in res}


intent_trans = {
    "disease_check": "检查项目",
    "disease_prevent": "预防措施",
    "disease_lasttime": "治疗时间",
    "disease_cureprob": "治愈概率",
    "disease_cureway": "治疗方式",
    "disease_easyget": "易感人群",
    "disease_desc": "疾病描述",
    "disease_symptom": "疾病的症状",
    "symptom_disease": "症状导致的疾病",
    "disease_acompany": "并发症",
    "disease_not_food": "忌口",
    "disease_do_food": "宜食食物",
    "disease_drug": "治疗药物",
    "disease_cause": "疾病病因",
}


async def get_counters(db: AsyncSession):
    return {
        "word": await make_dict(db, WordCount),
        "intent": await make_dict(db, IntentCount, intent_trans),
        "entity": await make_dict(db, EntityCount),
    }
