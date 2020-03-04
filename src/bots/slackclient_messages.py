import logging
from ..core.app import App

logger = logging.getLogger(__name__)


class OnboardingTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    # TODO: Create a better message builder:
    # https://github.com/slackapi/python-slackclient/issues/392
    # https://github.com/slackapi/python-slackclient/pull/400
    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome to Slack! :wave: We're so glad you're here. :blush:\n\n"
                "*Get started by completing the steps below:*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "pythonboardingbot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_reaction_block(),
                self.DIVIDER_BLOCK,
                *self._get_pin_block(),
            ],
        }

    def _get_reaction_block(self):
        task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f"{task_checkmark} *Add an emoji reaction to this message* :thinking_face:\n"
            "You can quickly respond to any message on Slack with an emoji reaction."
            "Reactions can be used for any purpose: voting, checking off to-do items, showing excitement."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
            "Learn How to Use Emoji Reactions>*"
        )
        return self._get_task_block(text, information)

    def _get_pin_block(self):
        task_checkmark = self._get_checkmark(self.pin_task_completed)
        text = (
            f"{task_checkmark} *Pin this message* :round_pushpin:\n"
            "Important messages and files can be pinned to the details pane in any channel or"
            " direct message, including group messages, for easy reference."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/205239997-Pinning-messages-and-files"
            "|Learn How to Pin a Message>*"
        )
        return self._get_task_block(text, information)

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [
                {"type": "mrkdwn", "text": information}]},
        ]


class SlackBot:
    def __init__(self, channel):
        self.channel = channel
        self.username = "LightNovel Downloader"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.app = None

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                'I recognize input of these two categories:\n\n'
                '- Profile page url of a lightnovel.\n\n'
                '- A query to search your lightnovel.\n\n'
                'Enter whatever you want or send /cancel to stop.'
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def _return_message(self, blocks: list) -> dict:
        """Returns with a composed message dict.

        Parameters
        ----------
        list : blocks
            [Slack block list]

        Returns
        -------
        [dict]
            [Return with a dict, which contains the timestamp, channel, usename, emoji and the message blocks.]
        """
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": blocks,
        }

    def start(self):
        # TODO: must be implemented
        # Start processing using this bot. It should use self methods to take
        # inputs and self.app methods to process them.
        #
        self.app = App()
        self.app.initialize()
        #
        # Checkout console.py for a sample implementation
        return self._return_message([self.WELCOME_BLOCK])

    def get_novel_url(self):
        # Returns a novel page url or a query
        pass

    def get_crawlers_to_search(self):
        # Returns user choice to search the choosen sites for a novel
        pass

    def choose_a_novel(self):
        # The search_results is an array of (novel_title, novel_url).
        # This method should return a single novel_url only
        #
        # By default, returns the first search_results. Implemented it to
        # handle multiple search_results
        pass

    def get_login_info(self):
        # By default, returns None to skip login
        pass

    def get_output_path(self):
        # You should return a valid absolute path. The parameter suggested_path
        # is valid but not gurranteed to exists.
        #
        # NOTE: If you do not want to use any pre-downloaded files, remove all
        #       contents inside of your selected output directory.
        #
        # By default, returns a valid existing path from suggested_path
        pass

    def get_output_formats(self):
        # The keys should be from from `self.output_formats`. Each value
        # corresponding a key defines whether create output in that format.
        #
        # By default, it returns all True to all of the output formats.
        pass

    def should_pack_by_volume(self):
        # By default, returns False to generate a single file
        pass

    def get_range_selection(self):
        # Should return a key from `self.selections` array
        pass

    def get_range_using_urls(self):
        # Should return a list of chapters to download
        pass

    def get_range_using_index(self):
        # Should return a list of chapters to download
        pass

    def get_range_from_volumes(self):
        # Should return a list of chapters to download
        pass

    def get_range_from_chapters(self):
        # Should return a list of chapters to download
        pass
