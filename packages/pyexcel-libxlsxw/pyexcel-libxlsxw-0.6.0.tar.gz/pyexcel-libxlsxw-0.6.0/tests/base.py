import os

import pyexcel

from nose.tools import eq_


class PyexcelHatWriterBase:
    """
    Abstract functional test for hat writers
    """

    content = {
        "X": [1, 2, 3, 4, 5],
        "Y": [6, 7, 8, 9, 10],
        "Z": [11, 12, 13, 14, 15],
    }

    def test_series_table(self):
        pyexcel.save_as(
            adict=self.content,
            dest_file_name=self.testfile,
            library="pyexcel-libxlsxw",
        )
        r = pyexcel.get_sheet(file_name=self.testfile, name_columns_by_row=0)
        eq_(r.dict, self.content)


class PyexcelWriterBase:
    """
    Abstract functional test for writers

    testfile and testfile2 have to be initialized before
    it is used for testing
    """

    content = [
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
    ]

    def _create_a_file(self, file):
        pyexcel.save_as(
            dest_file_name=file, array=self.content, library="pyexcel-libxlsxw"
        )

    def test_write_array(self):
        self._create_a_file(self.testfile)
        r = pyexcel.get_sheet(file_name=self.testfile)
        actual = list(r.rows())
        assert actual == self.content


class PyexcelMultipleSheetBase:
    def _write_test_file(self, filename):
        pyexcel.save_book_as(
            bookdict=self.content,
            dest_file_name=filename,
            library="pyexcel-libxlsxw",
        )

    def _clean_up(self):
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

    def test_sheet_names(self):
        r = pyexcel.BookReader(self.testfile)
        expected = ["Sheet1", "Sheet2", "Sheet3"]
        sheet_names = r.sheet_names()
        for name in sheet_names:
            assert name in expected

    def test_reading_through_sheets(self):
        b = pyexcel.BookReader(self.testfile)
        data = list(b["Sheet1"].rows())
        expected = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
        assert data == expected
        data = list(b["Sheet2"].rows())
        expected = [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]
        assert data == expected
        data = list(b["Sheet3"].rows())
        expected = [[u"X", u"Y", u"Z"], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected
        sheet3 = b["Sheet3"]
        sheet3.name_columns_by_row(0)
        data = list(b["Sheet3"].rows())
        expected = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected
