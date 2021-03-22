from pathlib import Path
import json


class ResponseParser:
    def __init__(self, filename):
        """This parser reads the file with the
        responses. It's used by the chatbot
        to determine what tokens invoke what
        responses.
        """
        self.filename = Path(filename)
        if not self.filename.exists():
            raise FileNotFoundError(
                f"The responses file {repr(str(self.filename))}"
                " does not exist."
            )
        
        self.raw_responses = self._parse_file()
        self.version, self.data, self.generics = self._parse_responses()

    
    def _parse_file(self):
        with self.filename.open() as responses_file:
            return json.load(responses_file)
    
    def _parse_responses(self):
        pass
    
    def _get_raw_or_error(self, key):
        if key in self.raw_responses:
            return self.raw_responses[key]
        raise ValueError(
            "Invalid response file."
            f"Missing key {repr(key)}."
        )