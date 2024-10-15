import unittest
from unittest.mock import MagicMock, patch
from src.error_handling.exceptions import NLPProcessingError
from src.nlp_processing.preprocess import preprocess_chat_data
from src.nlp_processing.inference import detect_intent, extract_urls, generate_response

class TestNLPProcessing(unittest.TestCase):

    @patch('src.nlp_processing.preprocess.AutoTokenizer.from_pretrained')
    def test_preprocessing(self):
        # Test tokenization and preprocessing logic
        input_text = "This is a test message."
        result = preprocess_chat_data(input_text)
        self.assertIsNotNone(result)  # Check if tokenization returns a result
        self.assertIsInstance(result, dict)  # Assuming it returns a dictionary of tokens

    @patch('src.nlp_processing.inference.AutoModelForCausalLM.from_pretrained')
    @patch('src.nlp_processing.inference.AutoTokenizer.from_pretrained')
    def test_generate_response(self, mock_load_model):
        # Mocking model loading and testing inference
        mock_model = MagicMock()
        mock_model.generate.return_value = "Test response"
        mock_load_model.return_value = mock_model

        input_text = "Test input"
        response = generate_response(input_text)
        self.assertEqual(response, "Test response")  # Check if inference generates the correct response

    def test_extract_urls(self):
        # Test that URLs are properly extracted from the response
        response_text = "Visit https://example.com for more info."
        urls = extract_urls(response_text)
        self.assertIn("https://example.com", urls)  # Check if the URL is correctly extracted

    def test_detect_intent(self):
        # Test the intent recognition from model output
        response_text = "Here is the build status."
        intent = detect_intent(response_text)
        self.assertEqual(intent, "build_status")  # Assuming "build_status" is a defined intent

    @patch('src.nlp_processing.inference.AutoModelForCausalLM.from_pretrained')
    @patch('src.nlp_processing.inference.AutoTokenizer.from_pretrained')
    def test_error_handling(self, mock_tokenizer, mock_model):
        # Mock tokenizer and model
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()
        
        # Simulate an empty input raising an error
        with self.assertRaises(NLPProcessingError):
            generate_response("")  # Empty input should raise an error


if __name__ == '__main__':
    unittest.main()
