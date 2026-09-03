import unittest
from unittest.mock import Mock, patch

import requests
from fastapi import HTTPException
from pydantic import ValidationError

from main import (
    ExplainRequest,
    FixRequest,
    GenerateRequest,
    PowerQueryRequest,
    VbaRequest,
    explain,
    fix,
    generate,
    power_query,
    vba,
    health_check,
)
from ollama_service import (
    OllamaServiceError,
    explain_formula,
    fix_formula,
    generate_formula,
    generate_vba,
    generate_power_query,
)


class HealthCheckTests(unittest.TestCase):
    def test_health_check_reports_ok(self):
        self.assertEqual(health_check(), {"status": "ok"})


class GenerateEndpointTests(unittest.TestCase):
    @patch("main.generate_formula", return_value="=SUM(C:C)")
    def test_generate_returns_formula(self, mock_generate):
        result = generate(GenerateRequest(prompt="sum sales"))

        self.assertEqual(result.formula, "=SUM(C:C)")
        mock_generate.assert_called_once_with("sum sales")

    @patch("main.generate_formula", side_effect=OllamaServiceError("Ollama is unavailable."))
    def test_generate_returns_service_unavailable_error(self, _mock_generate):
        with self.assertRaises(HTTPException) as context:
            generate(GenerateRequest(prompt="sum sales"))

        self.assertEqual(context.exception.status_code, 503)
        self.assertEqual(context.exception.detail, "Ollama is unavailable.")

    def test_generate_request_rejects_empty_prompt(self):
        with self.assertRaises(ValidationError):
            GenerateRequest(prompt="")


class ExplainEndpointTests(unittest.TestCase):
    @patch("main.explain_formula", return_value="This adds the values in column C.")
    def test_explain_returns_explanation(self, mock_explain):
        result = explain(ExplainRequest(formula="=SUM(C:C)"))

        self.assertEqual(result.explanation, "This adds the values in column C.")
        mock_explain.assert_called_once_with("=SUM(C:C)")

    def test_explain_request_rejects_empty_formula(self):
        with self.assertRaises(ValidationError):
            ExplainRequest(formula="")


class FixEndpointTests(unittest.TestCase):
    @patch("main.fix_formula", return_value="=SUM(A1:A10)")
    def test_fix_returns_corrected_formula(self, mock_fix):
        result = fix(FixRequest(formula="=SUM(A1:A10"))

        self.assertEqual(result.formula, "=SUM(A1:A10)")
        mock_fix.assert_called_once_with("=SUM(A1:A10")

    def test_fix_request_rejects_empty_formula(self):
        with self.assertRaises(ValidationError):
            FixRequest(formula="")


class VbaEndpointTests(unittest.TestCase):
    @patch("main.generate_vba", return_value="Sub Test()\nEnd Sub")
    def test_vba_returns_code(self, mock_generate_vba):
        result = vba(VbaRequest(prompt="create a test macro"))

        self.assertEqual(result.code, "Sub Test()\nEnd Sub")
        mock_generate_vba.assert_called_once_with("create a test macro")

    def test_vba_request_rejects_empty_prompt(self):
        with self.assertRaises(ValidationError):
            VbaRequest(prompt="")


class PowerQueryEndpointTests(unittest.TestCase):
    @patch("main.generate_power_query", return_value="let\n  Source = Excel.CurrentWorkbook()\nin\n  Source")
    def test_power_query_returns_code(self, mock_generate):
        result = power_query(PowerQueryRequest(prompt="load the current workbook"))

        self.assertEqual(result.code, "let\n  Source = Excel.CurrentWorkbook()\nin\n  Source")
        mock_generate.assert_called_once_with("load the current workbook")

    def test_power_query_request_rejects_empty_prompt(self):
        with self.assertRaises(ValidationError):
            PowerQueryRequest(prompt="")


class OllamaServiceTests(unittest.TestCase):
    @patch("ollama_service.requests.post")
    def test_generate_formula_sends_prompt_and_returns_response(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": "  =SUM(C:C)  "}
        mock_post.return_value = response

        result = generate_formula("sum sales")

        self.assertEqual(result, "=SUM(C:C)")
        mock_post.assert_called_once()
        request = mock_post.call_args.kwargs
        self.assertEqual(request["json"]["model"], "llama3.1:8b")
        self.assertIn("sum sales", request["json"]["prompt"])
        self.assertFalse(request["json"]["stream"])

    @patch("ollama_service.requests.post", side_effect=requests.RequestException)
    def test_generate_formula_reports_connection_failure(self, _mock_post):
        with self.assertRaisesRegex(OllamaServiceError, "Unable to connect to Ollama"):
            generate_formula("sum sales")

    @patch("ollama_service.requests.post")
    def test_generate_formula_reports_empty_response(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": " "}
        mock_post.return_value = response

        with self.assertRaisesRegex(OllamaServiceError, "empty response"):
            generate_formula("sum sales")

    @patch("ollama_service.requests.post")
    def test_explain_formula_returns_response(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": "  Adds column C.  "}
        mock_post.return_value = response

        self.assertEqual(explain_formula("=SUM(C:C)"), "Adds column C.")
        self.assertIn("=SUM(C:C)", mock_post.call_args.kwargs["json"]["prompt"])

    @patch("ollama_service.requests.post")
    def test_fix_formula_returns_corrected_formula(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": "  =SUM(A1:A10)  "}
        mock_post.return_value = response

        self.assertEqual(fix_formula("=SUM(A1:A10"), "=SUM(A1:A10)")
        self.assertIn("=SUM(A1:A10", mock_post.call_args.kwargs["json"]["prompt"])

    @patch("ollama_service.requests.post")
    def test_generate_vba_returns_code(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": "  ```vb\nSub Test()\nEnd Sub\n```  "}
        mock_post.return_value = response

        self.assertEqual(generate_vba("create a test macro"), "Sub Test()\nEnd Sub")
        self.assertIn("create a test macro", mock_post.call_args.kwargs["json"]["prompt"])

    @patch("ollama_service.requests.post")
    def test_generate_power_query_returns_code(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": "  let\n  Source = 1\nin\n  Source  "}
        mock_post.return_value = response

        self.assertEqual(
            generate_power_query("create a query"),
            "let\n  Source = 1\nin\n  Source",
        )
        self.assertIn("create a query", mock_post.call_args.kwargs["json"]["prompt"])


if __name__ == "__main__":
    unittest.main()
