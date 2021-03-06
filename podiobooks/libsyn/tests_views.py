"""Automated Tests of the Podiobooks LibSyn RSS Feed Parser"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.contrib.auth.models import User
from podiobooks.core.models import License


class LibsynImportViewsTestCase(TestCase):
    # fixtures = []

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@admin.com', 'pass')
        License.objects.create(slug='by-nc-nd', text='by-nc-nd', url='by-nc-nd')

    def test_slug_entry_view_redirect(self):
        response = self.client.get('/libsyn/import/')
        self.assertRedirects(response, '/admin/?next=/libsyn/import/', fetch_redirect_response=False)
        response = self.client.get('/admin/?next=/libsyn/import/')
        self.assertRedirects(response, '/admin/login/?next=/admin/%3Fnext%3D/libsyn/import/')

    def test_slug_entry_view(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get('/libsyn/import/')
        self.assertEquals(200, response.status_code)

    def test_libsyn_results_view(self):
        self.client.login(username='admin', password='pass')
        response = self.client.post('/libsyn/import/', data={'libsyn_slug': 'shadowmagic'})
        self.assertRedirects(response, '/libsyn/import/slug/shadowmagic/')
