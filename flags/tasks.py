from domain.celery import app
from typing import List
import json

from .types import DomainsData

from .models import Domain, Flag

BATCH_SIZE = 100


@app.task
def process_and_save_domains(domains: List[DomainsData]) -> None:
    """
    Background task to process domains and their assigned flags data
    and saves in the database.
        - Domains without assigned flags are filtered and saved at the same time with bulk.
        - Domains with assigned flags are filtered and saved one by one.
          It means Domain is created first and then its associated flags created.
    ----------------------------------------------------------------
    Args:
        domains (List[DomainsData]): Collection of domains to be saved in the database.
    ----------------------------------------------------------------

    Returns:
        (None): It processes data and returns None after the completion.
    """
    if len(domains) == 0:  # When domains is empty, we stops the execution
        return

    print(domains)
    # Prepare domains without flags for bulk create.
    domains_data = [
        Domain(
            fqdn=domain.get("fqdn", ""),
            created_at=domain.get("created_at", ""),
            expire_at=domain.get("expire_at", ""),
            deleted_at=domain.get("deleted_at", ""),
        )
        for domain in list(
            filter(lambda domain: len(domain.get("flags", [])) == 0, domains)
        )
    ]
    # Bulk create domains
    Domain.objects.bulk_create(domains_data, batch_size=BATCH_SIZE)

    flags_to_create = list()

    for domain in list(
        filter(lambda domain: len(domain.get("flags", [])) >= 1, domains)
    ):
        # Create domain
        domain_obj = Domain.objects.create(
            fqdn=domain.get("fqdn", ""),
            created_at=domain.get("created_at", ""),
            expire_at=domain.get("expire_at", ""),
            deleted_at=domain.get("deleted_at", ""),
        )

        for flag in domain["flags"]:
            flags_to_create.append(
                Flag(
                    domain=domain_obj,
                    flag_type=flag["flag_type"],
                    valid_from=flag["valid_from"],
                    valid_to=flag["valid_to"],
                )
            )

    flags_to_create_not_empty = len(
        flags_to_create
    )  # Equal to 0 when empty else has flags in it

    if flags_to_create_not_empty:
        Flag.objects.bulk_create(flags_to_create, batch_size=BATCH_SIZE)
