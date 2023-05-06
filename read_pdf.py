import fitz
import re


class ParsingPDF:
    re_tin = '\s\d{10}'

    def __init__(self, doc_pdf: str, key_name_person: str, key_tin: str, page_number: int):
        self.doc_pdf = doc_pdf
        self.key_name_person = key_name_person
        self.key_tin = key_tin
        self.page_number = page_number

    def find_name(self):
        doc = fitz.open(self.doc_pdf)
        text = doc.get_page_text(self.page_number - 1)
        name_person_list = re.findall(fr'{self.key_name_person}:\s\b[A-Я]\w*\b\s\b[A-Я]\w*\b\s\b[A-Я]\w*\b', text)
        name_of_person = re.sub(fr'{self.key_name_person}: ', r'', name_person_list[0].lower().title())
        return name_of_person

    def find_tin(self):
        doc = fitz.open(self.doc_pdf)
        text = doc.get_page_text(self.page_number - 1)
        tin_person_list = re.findall(fr'{self.key_tin}:{ParsingPDF.re_tin}', text)
        tin_person = re.sub(fr'{self.key_tin}: ', r'', tin_person_list[0])
        return tin_person


class DataPerson:
    x = ParsingPDF('Vypyska CredCard.pdf', 'Отримувач', 'ІПН', 1)
    dict_of_persons = {'first_name': '',
                       'last_name': '',
                       'tin': ''}

    @staticmethod
    def create_dict():
        name_of_person = ParsingPDF.find_name(DataPerson.x).split()
        tin = int(ParsingPDF.find_tin(DataPerson.x))
        DataPerson.dict_of_persons.update({'first_name': name_of_person[1], 'last_name': name_of_person[0], 'tin': tin})
        return DataPerson.dict_of_persons


a = DataPerson

if __name__ == '__main__':
    print(a.create_dict())
