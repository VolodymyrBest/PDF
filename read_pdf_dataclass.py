from dataclasses import dataclass, field
import fitz
import re


class ParsingPDF:
    doc_pdf = 'Vypyska CredCard.pdf'
    key_name_person = 'Отримувач'
    key_tin = 'ІПН'
    page_number = 1

    @staticmethod
    def find_name():
        doc = fitz.open(ParsingPDF.doc_pdf)
        text = doc.get_page_text(ParsingPDF.page_number - 1)
        name_person_list = re.findall(fr'{ParsingPDF.key_name_person}:\s\b[A-Я]\w*\b\s\b[A-Я]\w*\b\s\b[A-Я]\w*\b', text)
        name_of_person = re.sub(fr'{ParsingPDF.key_name_person}: ', r'', name_person_list[0].lower().title())
        return name_of_person

    @staticmethod
    def find_tin():
        doc = fitz.open(ParsingPDF.doc_pdf)
        text = doc.get_page_text(ParsingPDF.page_number - 1)
        tin_person_list = re.findall(fr'{ParsingPDF.key_tin}:\s\d\d\d\d\d\d\d\d\d\d\b', text)
        tin_person = re.sub(fr'{ParsingPDF.key_tin}: ', r'', tin_person_list[0])
        return tin_person


@dataclass
class DataPerson:
    name_of_person: str = field(default_factory=ParsingPDF.find_name, init=False, repr=False)
    tin: int = field(default_factory=ParsingPDF.find_tin, init=False, repr=False)
    info_of_person: dict = field(init=False)

    def __post_init__(self):
        self.info_of_person = {'first_name': self.name_of_person.split()[1],
                               'last_name': self.name_of_person.split()[0],
                               'tin': self.tin}


person = DataPerson()

if __name__ == '__main__':
    print(person.info_of_person)
