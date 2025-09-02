import re
import spacy

class DroneNLP:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def _extract_number(self, doc):
        for token in doc:
            if token.like_num:
                try:
                    return int(token.text)
                except ValueError:
                    pass
        return None

    def parse(self, text: str):
        """Return (intent, value) from a natural language command."""
        t = text.lower().strip()
        doc = self.nlp(t)

        if "take off" in t or "takeoff" in t or "launch" in t:
            alt = self._extract_number(doc) or 10
            return ("TAKEOFF", alt)
        if "land" in t or "touch down" in t:
            return ("LAND", None)
        if "rtl" in t or "return to launch" in t or "return home" in t or "go home" in t:
            return ("RTL", None)

        if "forward" in t:
            dist = self._extract_number(doc) or 5
            return ("MOVE_FORWARD", dist)
        if "backward" in t or re.search(r"\bback\b", t):
            dist = self._extract_number(doc) or 5
            return ("MOVE_BACKWARD", dist)
        if re.search(r"\bleft\b", t):
            dist = self._extract_number(doc) or 3
            return ("MOVE_LEFT", dist)
        if re.search(r"\bright\b", t):
            dist = self._extract_number(doc) or 3
            return ("MOVE_RIGHT", dist)
        if "up" in t or "ascend" in t or "climb" in t:
            dz = self._extract_number(doc) or 2
            return ("MOVE_UP", dz)
        if "down" in t or "descend" in t:
            dz = self._extract_number(doc) or 2
            return ("MOVE_DOWN", dz)

        if "rotate" in t or "yaw" in t or "turn" in t:
            deg = self._extract_number(doc) or 30
            if "left" in t or "anticlockwise" in t or "counter" in t:
                return ("ROTATE_CCW", deg)
            if "right" in t or "clockwise" in t:
                return ("ROTATE_CW", deg)
            return ("ROTATE_CW", deg)

        if "arm" in t and "disarm" not in t:
            return ("ARM", None)
        if "disarm" in t:
            return ("DISARM", None)
        if "hold" in t or "loiter" in t or "hover" in t:
            return ("HOLD", None)

        return ("UNKNOWN", None)