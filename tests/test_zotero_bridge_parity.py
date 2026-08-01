"""Zotero köprü bayt-özdeşlik parity guard.

İki kopya (nicel kök + niteliksel kol) daima byte-identical olmalıdır.
CONVENTIONS k.15 — dosya kopyası, kollar arası import değil.
"""
import hashlib
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
A = ROOT / "scripts" / "util" / "zotero_env_bridge.py"
B = ROOT / "niteliksel" / "scripts" / "util" / "zotero_env_bridge.py"


def _sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


class TestZoteroBridgeParity(unittest.TestCase):
    def test_both_bridge_copies_exist(self) -> None:
        self.assertTrue(A.exists(), f"Kanonik kök köprü bulunamadı: {A}")
        self.assertTrue(B.exists(), f"Niteliksel kol köprüsü bulunamadı: {B}")

    def test_bridge_copies_are_byte_identical(self) -> None:
        sha_a = _sha(A)
        sha_b = _sha(B)
        self.assertEqual(
            sha_a,
            sha_b,
            "İki Zotero köprü kopyası ayrıştı; kanonik (nicel kök) → nitele senkronla "
            "(kollar arası import değil, dosya kopyası). CONVENTIONS k.15.",
        )


if __name__ == "__main__":
    unittest.main()
