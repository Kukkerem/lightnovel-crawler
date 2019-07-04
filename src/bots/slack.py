#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
import logging
from slackclient import SlackClient
from ..core.app import App

logger = logging.getLogger(__name__)

# TODO: It is recommended to implemented all methods. But you can skip those
#       Which return values by default.

RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


class SlackBot:
    def __init__(self):
        self.bot_id = None
        self.slack_client = None
        self.app = None

    def start(self):
        # TODO: must be implemented
        # Start processing using this bot. It should use self methods to take
        # inputs and self.app methods to process them.
        #
        proxies = {'http': os.getenv('HTTP_PROXY')} if 'HTTP_PROXY' in os.environ else None

        self.slack_client = SlackClient(token=os.environ.get('SLACK_BOT_TOKEN'), proxies=proxies)
        self.app = App()
        self.app.initialize()

        print('RTM connection')
        if self.slack_client.rtm_connect(with_team_state=False):
            print('Slack Bot connected')
            self.bot_id = self.slack_client.api_call("auth.test")["user_id"]
            while True:
                command, channel = self.parse_bot_commands(self.slack_client.rtm_read())
                if command:
                    self.handle_command(command, channel)
                time.sleep(RTM_READ_DELAY)

        else:
            print("Connection failed. Exception traceback printed above.")

        #
        # Checkout console.py for a sample implementation

    # end def

    def parse_bot_commands(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.bot_id:
                    return message, event["channel"]
        return None, None

    @staticmethod
    def parse_direct_mention(message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self, command, channel):
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

        # Finds and executes the given command, filling in response
        response = None
        # This is where you start to implement more commands!
        if command.startswith(EXAMPLE_COMMAND):
            response = "Sure...write some more code then I can do that!"
            response += f'\nThe command is: {command}'

        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

    def get_novel_url(self):
        # Returns a novel page url or a query
        pass

    # end def

    def get_crawlers_to_search(self):
        # Returns user choice to search the choosen sites for a novel
        pass

    # end def

    def choose_a_novel(self):
        # The search_results is an array of (novel_title, novel_url).
        # This method should return a single novel_url only
        #
        # By default, returns the first search_results. Implemented it to
        # handle multiple search_results
        pass

    # end def

    def get_login_info(self):
        # By default, returns None to skip login
        pass

    # end if

    def get_output_path(self):
        # You should return a valid absolute path. The parameter suggested_path
        # is valid but not gurranteed to exists.
        #
        # NOTE: If you do not want to use any pre-downloaded files, remove all
        #       contents inside of your selected output directory.
        #
        # By default, returns a valid existing path from suggested_path
        pass

    # end def

    def get_output_formats(self):
        # The keys should be from from `self.output_formats`. Each value
        # corresponding a key defines whether create output in that format.
        #
        # By default, it returns all True to all of the output formats.
        pass

    # end def

    def should_pack_by_volume(self):
        # By default, returns False to generate a single file
        pass

    # end def

    def get_range_selection(self):
        # Should return a key from `self.selections` array
        pass

    # end def

    def get_range_using_urls(self):
        # Should return a list of chapters to download
        pass

    # end def

    def get_range_using_index(self):
        # Should return a list of chapters to download
        pass

    # end def

    def get_range_from_volumes(self):
        # Should return a list of chapters to download
        pass

    # end def

    def get_range_from_chapters(self):
        # Should return a list of chapters to download
        pass
    # end def
# end class
