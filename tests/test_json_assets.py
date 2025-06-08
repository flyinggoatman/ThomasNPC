import json
import os
import unittest

class TestJsonFiles(unittest.TestCase):
    def test_manifest_fields_and_assets(self):
        with open('manifest.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        required_keys = [
            'Name', 'Author', 'Version', 'Description',
            'UniqueID', 'MinimumApiVersion', 'ContentPackFor'
        ]
        for key in required_keys:
            self.assertIn(key, data, f"Missing key {key} in manifest.json")
        self.assertIn('UniqueID', data['ContentPackFor'],
                      "ContentPackFor must specify UniqueID")

    def test_content_fields_and_assets_exist(self):
        with open('content.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        required_keys = [
            'Format', 'MinimumApiVersion', 'Name', 'Author',
            'Version', 'Description', 'UniqueID', 'Changes'
        ]
        for key in required_keys:
            self.assertIn(key, data, f"Missing key {key} in content.json")
        # Verify that each referenced file exists
        for change in data.get('Changes', []):
            path = change.get('FromFile')
            if path:
                self.assertTrue(os.path.exists(path),
                                f"Referenced file {path} does not exist")

    def test_assets_json_valid(self):
        # Parse all json files under Assets/ to ensure valid json
        for root, _, files in os.walk('Assets'):
            for file in files:
                if file.lower().endswith('.json'):
                    path = os.path.join(root, file)
                    with self.subTest(path=path):
                        with open(path, 'r', encoding='utf-8') as f:
                            json.load(f)  # will raise if invalid

if __name__ == '__main__':
    unittest.main()
