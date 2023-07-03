from dataclasses import dataclass
from typing import final

from app.services import BaseService
from gpt.models import OpenAiProfile

from django.db.models.aggregates import Sum


@final
@dataclass
class OpenAiUsagesCounter(BaseService):
    """Returns number of all openai usages count"""

    def act(self) -> int:
        usages_sum = OpenAiProfile.objects.aggregate(Sum("usage_count"))
        return usages_sum and usages_sum["usage_count__sum"] or 0
