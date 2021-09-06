
import os
from grimoire.shell import shell as s
from grimoire.string import chomp, emptish
from search_run.exceptions import MenuException
from search_run.search_ui.interface import SearchInterface
from search_run.entities import SearchResult
from search_run.logger import logger


class FzfInTerminal(SearchInterface):
    """
    Renders the search ui using fzf + termite terminal
    """

    HEIGHT = 500
    WIDTH = 1100

    def __init__(
            self, title="RunT: "
    ):
        self.title = title

    def run(
            self, cmd: str
    ) -> (str, str):


        launch_cmd = f"""
        kitty --title=launcher -o remember_window_size=n \
        -o initial_window_width={FzfInTerminal.WIDTH}  \
        -o  initial_window_height={FzfInTerminal.HEIGHT} \
        bash -c '{cmd} | \
        fzf --reverse -i --exact --no-sort --print-query \
        > /tmp/search_run_result'
        """
        logger.info(f"{launch_cmd}")
        os.system(launch_cmd)

        with open('/tmp/search_run_result') as file:
            result = file.read()
            logger.info(f"Result: {result}")

        result = chomp(result)
        # the terminal result from fzf is the first line having the query and the second the matched result
        result_lines = result.splitlines()

        if emptish(result):
            raise MenuException.given_empty_value()
        return SearchResult(result=result_lines[1], query=result_lines[0])
