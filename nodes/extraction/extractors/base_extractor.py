#not used

class BaseExtractor:

    def extract(self, file_path):
        image = self._convert_if_pdf(file_path)
        raw_text = OCRService().extract_text(image)

        structured_data = self.parse(raw_text)

        return {
            "parsed_fields": structured_data,
            "raw_text": raw_text
        }

    def parse(self, text):
        raise NotImplementedError
