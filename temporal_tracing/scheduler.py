import asyncio

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleSpec,
    ScheduleUpdate,
    ScheduleUpdateInput,
)
from temporalio.client import Client, Schedule
from temporalio.contrib.opentelemetry import TracingInterceptor

from temporal_tracing.worker import GreetingWorkflow, init_runtime_with_telemetry


async def main():
    runtime = init_runtime_with_telemetry()

    # Connect client
    client = await Client.connect(
        "localhost:7233",
        # Use OpenTelemetry interceptor
        interceptors=[TracingInterceptor()],
        runtime=runtime,
    )

    await client.create_schedule(
        "open_telemetry-workflow-scheduled",
        Schedule(
            action=ScheduleActionStartWorkflow(
                GreetingWorkflow.run,
                "scheduled!",
                id="open_telemetry-workflow-scheduled",
                task_queue="open_telemetry-task-queue",
            ),
            spec=ScheduleSpec(
                cron_expressions=["* * * * *"],
            ),
        ),
    )

    print("Scheduled workflow!")


if __name__ == "__main__":
    asyncio.run(main())
