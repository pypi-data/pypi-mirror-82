# coding=utf-8

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from django.test import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse

from monitoring.overview import constants
from monitoring.overview import views
from monitoring.test import helpers


INDEX_URL = reverse(
    constants.URL_PREFIX + 'index')


class OverviewTest(helpers.TestCase):

    @override_settings(DASHBOARDS=[],
                       KIBANA_POLICY_SCOPE='monitoring',
                       KIBANA_POLICY_RULE='monitoring:kibana_access',
                       ENABLE_LOG_MANAGEMENT_BUTTON=False,
                       ENABLE_EVENT_MANAGEMENT_BUTTON=False,
                       SHOW_GRAFANA_HOME=True)
    def test_index_get(self):
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(
            res, 'monitoring/overview/index.html')
        self.assertTemplateUsed(res, 'monitoring/overview/monitor.html')


class KibanaProxyViewTest(helpers.TestCase):

    def setUp(self):
        super(KibanaProxyViewTest, self).setUp()
        self.view = views.KibanaProxyView()
        self.request_factory = RequestFactory()

    def test_get_relative_url_with_unicode(self):
        """Tests if it properly converts multibyte characters."""
        from six.moves.urllib import parse as urlparse

        self.view.request = self.request_factory.get(
            '/', data={'a': 1, 'b': 2}
        )
        expected_path = ('/elasticsearch/.kibana/search'
                         '/New-Saved-Search%E3%81%82')
        expected_qs = {'a': ['1'], 'b': ['2']}

        url = self.view.get_relative_url(
            u'/elasticsearch/.kibana/search/New-Saved-Searchあ'
        )
        # order of query params may change
        parsed_url = urlparse.urlparse(url)
        actual_path = parsed_url.path
        actual_qs = urlparse.parse_qs(parsed_url.query)

        self.assertEqual(actual_path, expected_path)
        self.assertEqual(actual_qs, expected_qs)
