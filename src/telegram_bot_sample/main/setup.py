import asyncio
import sys


def set_event_loop_policy() -> None:
    if "win" in sys.platform:
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
