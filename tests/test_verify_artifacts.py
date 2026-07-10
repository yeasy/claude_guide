from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import verify_artifacts as verifier


class ArtifactVerifierTests(unittest.TestCase):
    def test_html_title_inline_mermaid_and_published_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SUMMARY.md").write_text("* [A](a.md)\n* [A2](a.md)\n")
            (root / "a.md").write_text("```mermaid\ngraph TD\n```\n")
            self.assertEqual(verifier.summary_mermaid_count(root), 1)
            html = root / "book.html"
            html.write_text('<title>Claude 技术指南</title><figure class="diagram"><svg></svg></figure>')
            verifier.verify_html(html, "Claude 技术指南", 1)
            html.write_text('<title>Claude 技术指南</title><pre class="diagram-fallback">x</pre>')
            with self.assertRaises(verifier.ArtifactVerificationError):
                verifier.verify_html(html, "Claude 技术指南", 1)

    def test_pdf_signature_and_checksums_detect_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); pdf = root / "book.pdf"; html = root / "book.html"; manifest = root / "SHA256SUMS"
            pdf.write_bytes(b"%PDF-1.7\nbody"); html.write_text("html")
            with mock.patch.object(verifier.shutil, "which", return_value="tool"), mock.patch.object(verifier, "command_output", return_value="Title: Claude 技术指南\n"):
                verifier.verify_pdf(pdf, "Claude 技术指南")
            verifier.write_checksums([pdf, html], manifest); verifier.verify_checksums(manifest)
            html.write_text("changed")
            with self.assertRaises(verifier.ArtifactVerificationError): verifier.verify_checksums(manifest)


if __name__ == "__main__":
    unittest.main()
