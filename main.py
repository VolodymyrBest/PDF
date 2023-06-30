import fitz
import os
from dataclasses import dataclass, asdict
from datetime import datetime


class PDFInit:

    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    @staticmethod
    def check_if_pdf(path_to_file):
        file_name, file_extension = os.path.splitext(path_to_file)
        return file_extension == '.pdf'

    @staticmethod
    def formatting_pdf(lst: list[list[str]]):
        for index, sub_lst in enumerate(lst):
            if index == 0:
                continue
            lst[0] += lst[1]
        return lst[0]

    def open_file(self):
        if self.check_if_pdf(path_to_file=self.path_to_file):
            file = fitz.open(self.path_to_file)
            return file
        else:
            return TypeError("It is not a PDF format")

    def extract_text_from_file(self) -> list[str]:
        return self.formatting_pdf([page.get_text().split("\n") for page in self.open_file()])


class Extractor(PDFInit):
    first_rule = 'CERTIFICATE OF AUTOMOBILE INSURANCE'
    second_rule = 'Underwritten by'

    def extract_name(self):
        if self.extract_text_from_file()[0] == Extractor.first_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'Named Insured and Postal Address' in section:
                    try:
                        return super().extract_text_from_file()[index + 1].strip()
                    except Exception:
                        return "No Named Insured found"
        if self.extract_text_from_file()[0] == Extractor.second_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'Name of Insured(s)' in section:
                    try:
                        return super().extract_text_from_file()[-5].strip()
                    except Exception:
                        return "No Named Insured found"

    def extract_policy_number(self):
        if self.extract_text_from_file()[0] == Extractor.first_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'Policy Number' in section:
                    try:
                        return super().extract_text_from_file()[index + 5].strip()
                    except Exception:
                        return "No Policy Number found"
        if self.extract_text_from_file()[0] == Extractor.second_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'POLICY NUMBER' in section:
                    try:
                        policy_number = super().extract_text_from_file()[index].strip()
                        return policy_number[-9:]
                    except Exception:
                        return "No Policy Number found"

    def extract_effective_date(self):
        if self.extract_text_from_file()[0] == Extractor.first_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'Policy Effective Date' in section:
                    try:
                        effective_date = super().extract_text_from_file()[index + 5].strip()
                        return effective_date.partition(',')[0]
                    except Exception:
                        return "No Effective date found"
        if self.extract_text_from_file()[0] == Extractor.second_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'Insurance Period' in section:
                    try:
                        effective_date = super().extract_text_from_file()[index + 1].strip()
                        return datetime.strptime(effective_date[5:19], '%B %d, %Y').strftime('%Y/%m/%d')
                    except Exception:
                        return "No Effective date found"

    def extract_expiry_date(self):
        if self.extract_text_from_file()[0] == Extractor.first_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'Policy Expiry Date' in section:
                    try:
                        expiry_date = super().extract_text_from_file()[index + 4].strip()
                        return expiry_date.partition(',')[0]
                    except Exception:
                        return "No Expiry date found"
        if self.extract_text_from_file()[0] == Extractor.second_rule:
            for index, section in enumerate(super().extract_text_from_file()):
                if 'Insurance Period' in section:
                    try:
                        effective_date = super().extract_text_from_file()[index + 1].strip()
                        return datetime.strptime(effective_date[23:37], '%B %d, %Y').strftime('%Y/%m/%d')
                    except Exception:
                        return "No Expiry date found"

    def all_info(self):
        return self.extract_name(), self.extract_policy_number(), self.extract_effective_date(), \
            self.extract_expiry_date()


@dataclass
class InfoFromFile:
    name_of_insured: str
    policy_number: int
    effective_date: str
    expiry_date: str


def sample_pdf_output(file_path):
    new_instance = Extractor(file_path)
    info_from_file_instance = asdict(InfoFromFile(*new_instance.all_info()))
    sample_output = {}
    sample_output['Name of Insured'] = info_from_file_instance['name_of_insured']
    sample_output['Policy Number'] = info_from_file_instance['policy_number']
    sample_output['Effective Date'] = info_from_file_instance['effective_date']
    sample_output['Expiry Date'] = info_from_file_instance['expiry_date']
    for i in sample_output.items():
        print(i[0] + ': ' + i[1])
    return sample_output


if __name__ == '__main__':
    file_path = 'pdf_sample_format2.pdf'
    sample_pdf_output(file_path)
