import os
import sys
import pos
import unittest
import tempfile
import logging


class POSTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, pos.app.config['DATABASE'] = tempfile.mkstemp()
        pos.app.config['TESTING'] = True
        self.app = pos.app.test_client()
        # pos.init_db()
        # print 'aaa'

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(pos.app.config['DATABASE'])

    def test_webapp_route(self):
        rv = self.app.get('/')
        # print rv
        assert '/cache/Cache.rdf' in rv.data
    def test_cache_route(self):
        rv = self.app.get('/cache/Cache.rdf')
        print rv
        rv = self.app.get('/cache/Cache.png')
        print rv




if __name__ == '__main__':
    unittest.main()
