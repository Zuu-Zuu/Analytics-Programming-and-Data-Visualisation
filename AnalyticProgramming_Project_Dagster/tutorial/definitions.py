from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    load_assets_from_modules,
)

from . import assets

all_assets = load_assets_from_modules([assets])

# Addition: a ScheduleDefinition targeting all assets and a cron schedule of how frequently to run it
all_schedule = ScheduleDefinition(
    name="all_schedule",
    #target=AssetSelection.keys("test_in_batches", "store_in_mongo"),
    target=AssetSelection.all(),
    cron_schedule="0 0 * * *",  # every two minutes
)

defs = Definitions(
    assets=all_assets,
    schedules=[all_schedule],
)
