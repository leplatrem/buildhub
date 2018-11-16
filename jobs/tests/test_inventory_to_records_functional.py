# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.


import os
import io
import json
import sys
from unittest import mock

import asynctest
import pytest

from buildhub import inventory_to_records
from buildhub.utils import ARCHIVE_URL

here = os.path.dirname(__file__)


class CsvToRecordsTest(asynctest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        self.stdin = sys.stdin
        self.argv = sys.argv

        filename = os.path.join(here, 'data', 'inventory-simple.csv')
        sys.stdin = open(filename, 'r')
        sys.stdout = io.StringIO()
        sys.argv = ['inventory-to-records']

        async def fake_stream(loop, stream):
            # Workaround for "Pipe transport is for pipes/sockets only".
            # Here stream is just a file descriptor.
            for line in stream.readlines():
                yield bytes(line, 'utf-8')

        p = mock.patch('buildhub.inventory_to_records.stream_as_generator',
                       wraps=fake_stream)
        self.addCleanup(p.stop)
        p.start()

    def tearDown(self):
        sys.stdin.close()
        sys.argv = self.argv
        sys.stdout = self.stdout
        sys.stdin = self.stdin

    @pytest.fixture(autouse=True)
    def init_cache_folder(self, tmpdir):
        # Use str() on these LocalPath instances to turn them into plain
        # strings since to_kinto.fetch_existing() expects it to be a string.
        self.cache_folder = str(tmpdir)

    async def test_load_simple_file(self):
        await inventory_to_records.main(
            self.loop,
            cache_folder=self.cache_folder
        )

        output = sys.stdout.getvalue()
        records = [json.loads(o) for o in output.split('\n') if o]
        expected = [{
            'data': {
                'source': {
                    'product': 'firefox',
                    'revision': 'f6df375b86987b2772067a61873ebfe3a98c353a',
                    'repository': 'https://hg.mozilla.org/mozilla-central',
                    'tree': 'mozilla-central',
                },
                'target': {
                    'platform': 'win32',
                    'os': 'win',
                    'locale': 'en-US',
                    'version': '65.0a1',
                    'channel': 'nightly',
                },
                'download': {
                    'url': (
                        f'{ARCHIVE_URL}pub/firefox/nightly'
                        '/2018/11/2018-11-13-10-00-51-mozilla-central/'
                        'firefox-65.0a1.en-US.win32.installer.exe'
                    ),
                    'mimetype': 'application/msdos-windows',
                    'size': 50000,
                    'date': '2018-11-13T13:10:00Z',
                },
                'id': 'firefox_nightly_2018-11-13-10-00-51_65-0a1_win32_en-us',
                'build': {
                    'id': '20181113100051',
                    'date': '2018-11-13T10:00:51Z',
                    'as': 'z:/build/build/src/vs2017_15.8.4/VC/bin/Hostx64/x86/ml.exe',
                    'cc': (
                        'z:/build/build/src/clang/bin/clang-cl.exe -Xclang '
                        '-std=gnu99 -fms-compatibility-version=19.15.26726 -m32'
                    ),
                    'cxx': (
                        'z:/build/build/src/clang/bin/clang-cl.exe '
                        '-fms-compatibility-version=19.15.26726 -m32'
                    ),
                    'host': 'x86_64-pc-mingw32',
                    'target': 'i686-pc-mingw32',
                },
            }
        }, {
            'data': {
                'source': {
                    'product': 'firefox',
                    'revision': 'f6df375b86987b2772067a61873ebfe3a98c353a',
                    'repository': 'https://hg.mozilla.org/mozilla-central',
                    'tree': 'mozilla-central',
                },
                'target': {
                    'platform': 'macosx',
                    'os': 'mac',
                    'locale': 'en-US',
                    'version': '65.0a1',
                    'channel': 'nightly',
                },
                'download': {
                    'url': (
                        f'{ARCHIVE_URL}pub/firefox/nightly'
                        '/2018/11/2018-11-13-10-00-51-mozilla-central/'
                        'firefox-65.0a1.en-US.mac.dmg'
                    ),
                    'mimetype': 'application/x-apple-diskimage',
                    'size': 50000,
                    'date': '2018-11-13T13:10:00Z',
                },
                'id': 'firefox_nightly_2018-11-13-10-00-51_65-0a1_macosx_en-us',
                'build': {
                    'id': '20181113100051',
                    'date': '2018-11-13T10:00:51Z',
                    'as': (
                        '/builds/worker/workspace/build/src/clang/bin/clang '
                        '-target x86_64-apple-darwin11 -B /builds/worker/workspace/'
                        'build/src/cctools/bin -isysroot /builds/worker/workspace/'
                        'build/src/MacOSX10.11.sdk -std=gnu99'
                    ),
                    'cc': (
                        '/builds/worker/workspace/build/src/clang/bin/clang '
                        '-target x86_64-apple-darwin11 -B /builds/worker/workspace/'
                        'build/src/cctools/bin -isysroot /builds/worker/workspace/'
                        'build/src/MacOSX10.11.sdk -std=gnu99'
                    ),
                    'cxx': (
                        '/builds/worker/workspace/build/src/clang/bin/clang++ '
                        '-target x86_64-apple-darwin11 -B /builds/worker/workspace/'
                        'build/src/cctools/bin -isysroot /builds/worker/workspace/'
                        'build/src/MacOSX10.11.sdk'
                    ),
                    'host': 'x86_64-pc-linux-gnu',
                    'target': 'x86_64-apple-darwin',
                },
            }
        }, {
            'data': {
                'source': {
                    'product': 'firefox',
                    'revision': 'f6df375b86987b2772067a61873ebfe3a98c353a',
                    'repository': 'https://hg.mozilla.org/mozilla-central',
                    'tree': 'mozilla-central',
                },
                'target': {
                    'platform': 'linux-x86_64',
                    'os': 'linux',
                    'locale': 'en-US',
                    'version': '65.0a1',
                    'channel': 'nightly',
                },
                'download': {
                    'url': (
                        f'{ARCHIVE_URL}pub/firefox/nightly'
                        '/2018/11/2018-11-13-10-00-51-mozilla-central/'
                        'firefox-65.0a1.en-US.linux-x86_64.tar.bz2'
                    ),
                    'mimetype': 'application/x-bzip2',
                    'size': 50000,
                    'date': '2018-11-13T13:10:00Z',
                },
                'id': 'firefox_nightly_2018-11-13-10-00-51_65-0a1_linux-x86_64_en-us',
                'build': {
                    'id': '20181113100051',
                    'date': '2018-11-13T10:00:51Z',
                    'as': '/builds/worker/workspace/build/src/clang/bin/clang -std=gnu99',
                    'cc': '/builds/worker/workspace/build/src/clang/bin/clang -std=gnu99',
                    'cxx': '/builds/worker/workspace/build/src/clang/bin/clang++',
                    'host': 'x86_64-pc-linux-gnu',
                    'target': 'x86_64-pc-linux-gnu',
                },
            }
        }]

        assert len(records) == len(expected), [r['data']['id'] for r in records]
        assert [
            r['data']['id'] for r in records
        ] == [
            r['data']['id'] for r in expected
        ], [r['data']['id'] for r in records]
        assert records == expected
