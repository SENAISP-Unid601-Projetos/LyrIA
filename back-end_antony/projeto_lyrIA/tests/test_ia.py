import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.ia import LyrIA

class TestLyrIA(unittest.TestCase):
    def setUp(self):
        self.ia = LyrIA()

    def test_cumprimentos(self):
        for palavra in ["oi", "olá", "e aí"]:
            resposta = self.ia.responder(palavra)
            self.assertIn("LyrIA", resposta)

    def test_respostas_inadequadas(self):
        resposta = self.ia.responder("tchau")
        self.assertNotIn("gato", resposta.lower())

if __name__ == "__main__":
    unittest.main()