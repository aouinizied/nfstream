import unittest
from nfstream.streamer import Streamer
from sys import maxsize
import os


def get_files_list(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file and 'future' not in r:
                files.append(os.path.join(r, file))
    return files


def flows_from_file(file):
    f = open(file, "r")
    fl = f.readlines()
    truth = []
    for l in fl:
        truth.append(l.split("\n")[0])
    del fl
    f.close()
    return sorted(truth)


class TestMethods(unittest.TestCase):
    def test_protocols_without_timeouts(self):
        files = get_files_list("tests/csv/")
        print("test: functional on {} applications traffic capture".format(len(files)))
        for file in files:
            streamer = Streamer(source=file.replace('.csv', '').replace('/csv/', '/pcap/'),
                                capacity=128000,
                                inactive_timeout=maxsize,
                                active_timeout=maxsize)
            print(file.replace('.csv', '').replace('/csv/', '/pcap/'))
            exports = []
            for export in streamer:
                exports.append(str(export))
            exports = sorted(exports)
            exports_ground_truth = flows_from_file(file)
            del streamer
            self.assertEqual(exports, exports_ground_truth)


if __name__ == '__main__':
    unittest.main()