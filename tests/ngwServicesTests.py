import unittest
import urllib2
import json

from pyramid.paster import get_appsettings


class NgwServicesTests(unittest.TestCase):
    # def __init__(self, path_to_config):
    #     self.config = path_to_config

    def setUp(self):
        settings = get_appsettings('production.ini')
        self.ngwUrl = settings['proxy_ngw']

    def test_get_resource_available(self):
        service_url = self.ngwUrl + 'resource/0/child/'
        request = urllib2.Request(service_url)
        response = urllib2.urlopen(request)
        self.assertEqual(response.getcode(), 200)

    def test_get_resource_as_json(self):
        service_url = self.ngwUrl + 'resource/0/child/'
        request = urllib2.Request(service_url)
        response = urllib2.urlopen(request)
        try:
            json.loads(response.read())
        except ValueError, err:
            self.fail('Resources service answer is not json format')

if __name__ == '__main__':
    unittest.main()
