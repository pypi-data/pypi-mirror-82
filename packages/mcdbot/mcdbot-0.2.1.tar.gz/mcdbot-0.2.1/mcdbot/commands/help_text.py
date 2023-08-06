#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.mcdbot import global_config
from mcdbot.commands import usage_text
from mcdbot.discordcontext import DiscordContext
from loguru import logger


async def help_text(msg):
    usage = usage_text[msg.x_context]
    if msg.x_context == DiscordContext.GUILD_TEXT_CHANNEL:
        context = 'main text channel'
    elif msg.x_context == DiscordContext.DM_CHANNEL:
        context = 'DMs'
    elif msg.x_context == DiscordContext.GROUP_CHANNEL:
        context = 'group DMs'
    else:
        logger.warning("[PROBABLY BUG] Context text for msg.x_context in help_text(msg) is not defined.")
        context = "SOMETHING'S WRONG BRUH"

    return f"""```md
Mcdbot (v. {global_config.final.version})

Usage (in the {context}):
{usage}

Source code: {global_config.final.source}
Issue tracker: {global_config.final.issues}
```"""
