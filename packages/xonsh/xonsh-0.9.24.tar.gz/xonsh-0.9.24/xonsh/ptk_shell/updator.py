"""Has classes that help updating Prompt sections using Threads."""

import builtins
import concurrent.futures
import threading
import typing as tp

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import PygmentsTokens

from xonsh.prompt.base import _format_value
from xonsh.style_tools import partial_color_tokenize, style_as_faded


class Executor:
    """Caches thread results across prompts."""

    def __init__(self):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=builtins.__xonsh__.env["ASYNC_PROMPT_THREAD_WORKERS"]
        )

        # the attribute, .cache is cleared between calls.
        # This caches results from callback alone by field name.
        self.thread_results = {}

    def submit(self, func: tp.Callable, field: str):
        future = self.thread_pool.submit(self._run_func, func, field)
        place_holder = "{" + field + "}"

        return (
            future,
            (
                self.thread_results[field]
                if field in self.thread_results
                else place_holder
            ),
            place_holder,
        )

    def _run_func(self, func, field):
        """Run the callback and store the result."""
        result = func()
        self.thread_results[field] = (
            result if result is None else style_as_faded(result)
        )
        return result


class AsyncPrompt:
    """Represent an asynchronous prompt."""

    def __init__(self, name: str, session: PromptSession, executor: Executor):
        """

        Parameters
        ----------
        name: str
            what prompt to update. One of ['message', 'rprompt', 'bottom_toolbar']
        session: PromptSession
            current ptk session
        """

        self.name = name

        # list of tokens in that prompt. It could either be resolved or not resolved.
        self.tokens: tp.List[str] = []
        self.timer = None
        self.session = session
        self.executor = executor

        # (Key: the future object) that is created for the (value: index/field_name) in the tokens list
        self.futures: tp.Dict[
            concurrent.futures.Future,
            tp.Tuple[str, tp.Optional[int], tp.Optional[str], tp.Optional[str]],
        ] = {}

    def start_update(self, on_complete):
        """Listen on futures and update the prompt as each one completed.

        Timer is used to avoid clogging multiple calls at the same time.

        Parameters
        -----------
        on_complete:
            callback to notify after all the futures are completed
        """
        for fut in concurrent.futures.as_completed(self.futures):
            val = fut.result()

            if fut not in self.futures:
                # rare case where the future is completed but the container is already cleared
                # because new prompt is called
                continue

            placeholder, idx, spec, conv = self.futures[fut]
            # example: placeholder="{field}", idx=10, spec="env: {}"

            if isinstance(idx, int):
                self.update_token(idx, val, spec, conv)
            else:  # when the function is called outside shell.
                for idx, sect in enumerate(self.tokens):
                    if placeholder in sect:
                        val = sect.replace(placeholder, val)
                        self.update_token(idx, val, spec, conv)

            # calling invalidate in less period is inefficient
            self.invalidate()

        on_complete(self.name)

    def update_token(
        self,
        idx: int,
        val: tp.Optional[str],
        spec: tp.Optional[str],
        conv: tp.Optional[str],
    ) -> None:
        """Update tokens list in-place"""
        if idx < len(self.tokens):
            self.tokens[idx] = _format_value(val, spec, conv)

    def invalidate(self):
        """Create a timer to update the prompt. The timing can be configured through env variables.
        threading.Timer is used to stop calling invalidate frequently.
        """
        from xonsh.ptk_shell.shell import tokenize_ansi

        if self.timer:
            self.timer.cancel()

        def _invalidate():
            new_prompt = "".join(self.tokens)
            formatted_tokens = tokenize_ansi(
                PygmentsTokens(partial_color_tokenize(new_prompt))
            )
            setattr(self.session, self.name, formatted_tokens)
            self.session.app.invalidate()

        self.timer = threading.Timer(
            builtins.__xonsh__.env["ASYNC_INVALIDATE_INTERVAL"], _invalidate
        )
        self.timer.start()

    def stop(self):
        """Stop any running threads"""
        for fut in self.futures:
            fut.cancel()
        self.futures.clear()

    def submit_section(
        self,
        func: tp.Callable,
        field: str,
        idx: tp.Optional[int] = None,
        spec: tp.Optional[str] = None,
        conv=None,
    ):
        future, intermediate_value, placeholder = self.executor.submit(func, field)
        self.futures[future] = (placeholder, idx, spec, conv)
        return intermediate_value


class PromptUpdator:
    """Handle updating multiple AsyncPrompt instances prompt/rprompt/bottom_toolbar"""

    def __init__(self, session: PromptSession):
        self.prompts: tp.Dict[str, AsyncPrompt] = {}
        self.prompter = session
        self.executor = Executor()

    def add(self, prompt_name: tp.Optional[str]):
        # clear out old futures from the same prompt
        if prompt_name is None:
            return

        if prompt_name in self.prompts:
            self.stop(prompt_name)

        self.prompts[prompt_name] = AsyncPrompt(
            prompt_name, self.prompter, self.executor
        )
        return self.prompts[prompt_name]

    def start(self):
        """after ptk prompt is created, update it in background."""
        threads = [
            threading.Thread(target=prompt.start_update, args=[self.on_complete])
            for pt_name, prompt in self.prompts.items()
        ]

        for th in threads:
            th.start()

    def stop(self, prompt_name: str):
        if prompt_name in self.prompts:
            self.prompts[prompt_name].stop()

    def on_complete(self, prompt_name):
        self.prompts.pop(prompt_name, None)

    def set_tokens(self, prompt_name, tokens: tp.List[str]):
        if prompt_name in self.prompts:
            self.prompts[prompt_name].tokens = tokens
