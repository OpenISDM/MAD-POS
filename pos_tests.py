import os
import pos
import unittest
import tempfile
import logging


class POSTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, pos.app.config['DATABASE'] = tempfile.mkstemp()
        pos.app.config['TESTING'] = True
        self.app = pos.app.test_client()
        self.topic_url = 'http://isserver.iis.sinica.edu.tw/topic?id=12312RW'

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(pos.app.config['DATABASE'])

    def test_1nit(self):
        """
        Step 1!!!!
        Testing uploaded route '/callback' using HTTP POST
        """
        with open('./testing/pos.pyc', 'rb') as f:
            rv = self.app.post('/callback', data=dict(file=f))
        assert 'PUSH file is not correct' in rv.data

        with open('./testing/testing.rdf', 'rb') as f:
            rv = self.app.post('/callback', data=dict(file=f))
        assert 'PUSH Success' in rv.data

        with open('./testing/testing.png', 'rb') as f:
            rv = self.app.post('/callback', data=dict(file=f))
        assert 'PUSH Success' in rv.data

    def test_webapp_route(self):
        rv = self.app.get('/')
        assert '/cache/Cache.rdf' in rv.data

    def test_cache_route(self):
        rv = self.app.get('/cache/rdf')
        assert '<ns1:hasDistrict>' in rv.data
        rv = self.app.get('/cache/png')
        assert '200' in str(rv.status_code)

    def test_setTopicUrl_route(self):
        rv = self.app.get('/settopicurl?url=' + self.topic_url)
        assert 'Store Topic URL Success!' in rv.data
        rv = self.app.get('/settopicurl')
        assert 'Store Topic URL Failed!' in rv.data

    def test_callback_route_GET(self):
        rv = self.app.get('/callback?hub.mode=' + 'subscribe' +
                          '&hub.challenge=' + 'secretkey' + 
                          '&hub.topic=' + self.topic_url)
        assert "Sorry! I don't know what do you want for me!!" in rv.data
        rv = self.app.get('/callback?hub.mode=' + 'unsubscribe' +
                          '&hub.challenge=' + 'secretkey' + 
                          '&hub.topic=' + self.topic_url)
        assert "Sorry! I don't know what do you want for me!!" in rv.data
        rv = self.app.get('/callback?hub.mode=' + 'denied' +
                          '&hub.challenge=' + 'secretkey' + 
                          '&hub.topic=' + self.topic_url)
        assert "Accepted!!" in rv.data


if __name__ == '__main__':
    unittest.main()
