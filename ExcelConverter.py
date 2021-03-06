import pandas
import xlrd
import os


class ExcelConverter:

    def __init__(self, excel_file, text_file):
        self.excel_file = excel_file
        self.text_file = text_file

    def read_file(self):
        sheets = pandas.read_excel(self.excel_file, sheet_name=None)

        for sheet in sheets:
            data_frame = sheets[sheet]
            rows, columns = data_frame.shape

            for x in range(0, columns):
                data = data_frame.iloc[:, x].tolist()
                data = " ".join(str(x) for x in data)
                self.write_to_file(data)

    def write_to_file(self, data):
        with open(self.text_file, 'a') as file:
            file.write(data)

        file.close()


if __name__ == "__main__":
    excel = ExcelConverter(os.getcwd() + "/sampleDir/plant_data.xlsx", os.getcwd() + "/temp/plant_data.txt")
    excel.read_file()
