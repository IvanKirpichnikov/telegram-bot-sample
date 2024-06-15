import asyncio
import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from adaptix import load

from telegram_bot_sample.config import build_config
from telegram_bot_sample.infrastructure.localization.storage import build_localization_storage
from telegram_bot_sample.main.setup import set_event_loop_policy


class RunType(Enum):
    TELEGRAM_BOT = "telegram_bot"


@dataclass(frozen=True, slots=True)
class Arguments:
    config: Path | None = None
    run: RunType | None = None


def run_application(
    arguments: Arguments,
    run_type: RunType,
) -> None:
    if run_type == RunType.TELEGRAM_BOT:
        if arguments.config is None:
            raise ValueError(arguments)
        
        from telegram_bot_sample.main.run import run_telegram_bot
        
        logging.basicConfig(level=logging.DEBUG)
        config = build_config(path=arguments.config)
        localization_storage = build_localization_storage(config.localization)
        return asyncio.run(
            run_telegram_bot(
                config=config,
                localization_storage=localization_storage,
            ),
        )


def create_argument_parser() -> ArgumentParser:
    argparse = ArgumentParser(description="bijouterie application")
    
    argparse.add_argument(
        "--run",
        dest="run",
        required=False,
        type=str,
    )
    argparse.add_argument(
        "--config",
        dest="config",
        required=False,
        type=Path,
    )
    
    return argparse


def parse_arguments_parser(argument_parser: ArgumentParser) -> Arguments:
    return load(
        argument_parser.parse_args().__dict__,
        Arguments,
    )


def main() -> None:
    set_event_loop_policy()
    
    argument_parser = create_argument_parser()
    arguments = parse_arguments_parser(argument_parser)
    
    if arguments.run:
        run_application(arguments, arguments.run)
