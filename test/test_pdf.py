from main import sample_pdf_output
import pytest


@pytest.mark.parametrize('file_path, expected_result', [
    ('pdf_sample_format1.pdf', {'Name of Insured': 'John Smith',
                                'Policy Number': '3770302',
                                'Effective Date': '2021/06/15',
                                'Expiry Date': '2022/06/15'}),
    ('pdf_sample_format2.pdf', {'Name of Insured': 'James Smith',
                                'Policy Number': '501234249',
                                'Effective Date': '2022/04/14',
                                'Expiry Date': '2023/04/14'})])
def test_pdf_output(file_path, expected_result):
    assert isinstance(sample_pdf_output(file_path), dict)
    assert sample_pdf_output(file_path) == expected_result


