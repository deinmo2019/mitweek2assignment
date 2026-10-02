"""Deterministic teaching examples; no trained model or external API."""
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Question:
    text: str
    options: tuple
    correct: str
    explanation: str

QUESTIONS = [
    Question('It is raining outside. What should you take before walking out?', ('An umbrella', 'Sunglasses only', 'Nothing'), 'An umbrella', 'An umbrella helps keep you dry.'),
    Question('The traffic light is red. What should a driver do?', ('Stop', 'Speed up', 'Ignore it'), 'Stop', 'A red signal means stop.'),
    Question('The traffic light is green and the crossing is clear. What should a driver do?', ('Stop indefinitely', 'Proceed carefully', 'Reverse'), 'Proceed carefully', 'Proceed carefully when the signal and crossing allow it.'),
    Question('You see smoke coming from a building. What is the sensible response?', ('Enter to investigate', 'Move away and alert emergency services', 'Ignore it'), 'Move away and alert emergency services', 'Keep a safe distance and alert emergency services.'),
    Question('A banana is yellow. Does that mean every yellow object is a banana?', ('Yes', 'No', 'Only on Mondays'), 'No', 'Sharing a colour does not make objects the same thing.'),
    Question('You are thirsty. What should you drink?', ('Clean drinking water', 'Cooking oil', 'Sand'), 'Clean drinking water', 'Clean drinking water is an appropriate choice.'),
    Question('You are not thirsty, but you feel cold. What would help?', ('Clean drinking water', 'A warm jacket', 'Remove your clothes'), 'A warm jacket', 'The question describes cold, not thirst.'),
    Question('It is not raining and the forecast is dry. Must you carry an umbrella for rain?', ('Yes', 'No', 'Only indoors'), 'No', 'The question gives no reason to expect rain.'),
]

def chatbot_answer(text):
    """Deliberately basic keyword rules: negation and context are ignored."""
    tokens = set(re.findall(r'[a-z]+', text.lower()))
    if tokens & {'rain', 'raining'}:
        return 'An umbrella', 'Matched rain/raining → umbrella.'
    elif 'traffic' in tokens:
        return 'Stop', 'Matched traffic → stop; the light colour is ignored.'
    elif 'smoke' in tokens:
        return 'Move away and alert emergency services', 'Matched smoke → move away and alert.'
    elif 'yellow' in tokens:
        return 'Yes', 'Matched yellow → yes; this overgeneralizes.'
    elif 'thirsty' in tokens:
        return 'Clean drinking water', 'Matched thirsty → water; negation is ignored.'
    return 'I do not know', 'No keyword rule matched.'

@dataclass(frozen=True)
class Pattern:
    name: str
    terms: tuple
    answer: int
    rule: str

PATTERNS = [
    Pattern('Even steps', (2, 4, 6, 8), 10, 'Add 2 each time.'),
    Pattern('Doubling', (3, 6, 12, 24), 48, 'Multiply by 2 each time.'),
    Pattern('Growing gaps', (1, 3, 6, 10), 15, 'Add 2, then 3, then 4, then 5.'),
    Pattern('Squares', (1, 4, 9, 16), 25, 'Square successive positive integers.'),
    Pattern('Fibonacci', (1, 1, 2, 3, 5), 8, 'Add the previous two terms.'),
    Pattern('Alternating steps', (2, 5, 4, 7, 6), 9, 'Alternate +3 and −1.'),
]

def predict_pattern(terms):
    """Try only constant addition and constant multiplication, in that order."""
    if len(terms) < 3:
        return None, 'At least three terms are required.'
    gaps = [b - a for a, b in zip(terms, terms[1:])]
    if len(set(gaps)) == 1:
        return terms[-1] + gaps[0], f'Constant difference: add {gaps[0]}.'
    # Cross multiplication avoids floating-point ratio comparisons.
    if terms[0] != 0 and all(a != 0 for a in terms[:-1]):
        if all(b * terms[0] == a * terms[1] for a, b in zip(terms, terms[1:])):
            prediction = terms[-1] * terms[1] / terms[0]
            return prediction, f'Constant ratio: multiply by {terms[1] / terms[0]:g}.'
    return None, 'Neither constant addition nor constant multiplication fits. The script abstains.'
