import markovify
from random import choice

from model.songelement import SongElement
from utils import clean_commas

from typing import List, Dict, Optional


class WriteSong:
    """
    Song object
    """

    def __init__(self, opts, structure: str, data):
        self.opts = opts
        self.verse_model = self._build_model(data["verse_text"])
        self.chorus_model = self._build_model(data["chorus_text"])

        self.verse_dict = data["verse_dict"]
        self.chorus_dict = data["chorus_dict"]

        self.structure = structure
        self.song: List[str] = []
        self._write_song()

    def __repr__(self) -> str:
        """Return string representation of song"""
        return "\n".join(clean_commas(self.song))

    def _write_song(self):
        """Iterate through the song structure and build
        corresponding song elements"""
        chorus = self._build_song_element(
            "C", self.chorus_model, self.chorus_dict)
        for name in self.structure:
            if name == "C":
                self.song.extend(chorus)
            else:
                self.song.extend(
                    self._build_song_element(
                        name, self.verse_model, self.verse_dict)
                )
            self.song.append("\n")

    def _build_song_element(self, name: str, model, rhyme_dict) -> List[str]:
        """Takes an element name, returns a song element"""
        num_syllables = choice(self.opts[name]["num_syllables"])
        pattern = choice(self.opts[name]["pattern"])
        song_elem = SongElement(self.opts, name, model, rhyme_dict,
                                num_syllables, pattern)
        return song_elem.get_elem()

    @staticmethod
    def _build_model(text: str):
        """Takes text and returns a Markovify model"""
        return markovify.NewlineText(text, state_size=2)
