"""This package contains test code copied from ZODB 3.9 with minor alterations.

It is especially useful for testing RelStorage + ZODB 3.8.
"""
import os
from nti.testing.time import MonotonicallyIncreasingTimeLayerMixin

from ZODB.DB import DB
from ZODB.tests.util import setUp
from ZODB.tests.util import tearDown

class TestBlobMixin(object):

    DEFAULT_BLOB_STORAGE_KWARGS = {}

    def setUp(self):
        super(TestBlobMixin, self).setUp()
        setUp(self)
        self._timer = MonotonicallyIncreasingTimeLayerMixin()
        self._timer.testSetUp()
        try:
            self.blob_storage = self.create_storage(**self.DEFAULT_BLOB_STORAGE_KWARGS)
        except: # pragma: no cover
            # If setUp() raises an exception, tearDown is never called.
            # That's bad: ZODB.tests.util.setUp() changes directories and
            # monkeys with the contents of the stdlib tempfile.
            tearDown(self)
            raise
        self.database = DB(self.blob_storage)

    def tearDown(self):
        self.database.close()
        self.blob_storage.close()
        self._timer.testTearDown()
        tearDown(self)
        super(TestBlobMixin, self).tearDown()

    def _count_and_size_blobs_in_directory(self):
        size = 0
        count = 0
        d = self.blob_storage.blobhelper.blob_dir
        for base, _, files in os.walk(d):
            for f in files:
                if f.endswith('.blob'):
                    count += 1
                    try:
                        size += os.stat(os.path.join(base, f)).st_size
                    except OSError: # pragma: no cover
                        if os.path.exists(os.path.join(base, f)):
                            raise
        return count, size

    def _size_blobs_in_directory(self):
        return self._count_and_size_blobs_in_directory()[1]

    def _count_blobs_in_directory(self):
        return self._count_and_size_blobs_in_directory()[0]
