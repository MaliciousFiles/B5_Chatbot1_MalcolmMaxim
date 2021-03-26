# Reads responses.json

from pathlib import Path
import json
import random
from collections import namedtuple

from src.tokenizer import tokenize

LatestResponse = namedtuple("LatestResponse", ["response", "weight"])

CONTINUE_THREAD_TOKENS = ["continue", "more"]
END_THREAD_TOKENS = ["stop", "care"]
END_THREAD_MESSAGES = [
    "Very well then, we may talk of some other topic.",
    "If you wish, we may speak of something else.",
    "Ok then, what is your next question?"
]


class ResponseParser:
    def __init__(self, filename):
        """This parser reads the file with the
        responses. It's used by the chatbot
        to get all responses and the mapped tokens.
        """
        self.filename = Path(filename)
        if not self.filename.exists():
            raise FileNotFoundError(
                f"The responses file {repr(str(self.filename))}"
                " does not exist."
            )
        
        self.raw_responses = self._parse_file()
        (
            self.version,
            self.data,
            self.generics
		) = self._parse_responses()
        self.thread = []
        self.last_response = None

    def get_response(self, user_input):
        """Given `user_input`, this method tokenizes it, and
        returns a response that is most likely to respond to the
        user in an appropriate way.
        """
        tokens = tokenize(user_input)
        latest_response = LatestResponse(None, 0)

        if not self.data:
            raise ValueError("Data must have at least one item")

        response = self._run_thread(tokens)
        if response:
            return response
    
        # Normal handling
        for response in self.data:
            response_weight = self._get_weight(response, tokens)

            if response_weight == latest_response.weight:
                if random.random() > 0.5:
                    latest_response = LatestResponse(response, response_weight)
            elif response_weight > latest_response.weight:
                latest_response = LatestResponse(response, response_weight)

        self.last_response = latest_response
        if latest_response.weight == 0:
            return random.choice(self.generics)
        
        return random.choice(latest_response.response["value"])

    # TODO: implement 'thread'
    def _run_thread(self, tokens):
        # Continues a conversation thread
        if self.last_response and self.last_response.response and "thread" in self.last_response.response.keys():
            if not self.thread:
                self.thread = self.last_response.response["thread"]["steps"].copy()
                
                for token in tokens:
                    if token in self.last_response.response["thread"]["triggers"]:
                        if len(self.thread) == 1:
                            self.last_response = None

                        return random.choice(self.thread.pop(0))
            else:
                for token in tokens:
                    if token in CONTINUE_THREAD_TOKENS:
                        if len(self.thread) == 1:
                            self.last_response = None

                        return random.choice(self.thread.pop(0))
                    elif token in END_THREAD_TOKENS:
                        self.thread = []
                        self.last_response = None
                        return random.choice(END_THREAD_MESSAGES)

    # TODO: implement 'after'
    def _get_weight(self, response, tokens):
        """Gets the weight of `response`, and given the tokens in
        user input, returns a weight total of all
        """
        weight = 0
        for token in tokens:
            if token in response["tokens"].keys():
                weight += response['tokens'][token]['weight']

        return weight

    def _parse_file(self):
        with self.filename.open() as responses_file:
            return json.load(responses_file)
    
    def _parse_responses(self):
        version = self._get_raw_or_error("version")
        if version != 1:
            raise ValueError(
                "The parser only supports a"
                "version 1 schema."
            )
        data = self._get_raw_or_error("data")
        generics = self._get_raw_or_error("generics")
        return (version, data, generics)
    
    def _get_raw_or_error(self, key):
        if key in self.raw_responses:
            return self.raw_responses[key]
        raise ValueError(
            "Invalid response file."
            f"Missing key {repr(key)}."
        )
    
    def __repr__(self):
        return f"ResponseParser({repr(str(self.filename))})"
    
    def __str__(self):
        return self.__repr__()