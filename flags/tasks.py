from celery import shared_task
from typing import List

from .types import DomainsData


@shared_task
def process_and_save_domains(domains: List[DomainsData]):
    pass
