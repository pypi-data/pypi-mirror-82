# Copyright 2016, Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf import settings
from django.views import generic
import functools
import requests
from requests import exceptions as r_exceptions

from oslo_serialization import jsonutils

from horizon import exceptions
from openstack_dashboard.api import base
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils


@urls.register
class Search(generic.View):
    """Pass-through API for executing searches against searchlight.

       Horizon only adds auth and CORS proxying.
    """
    url_regex = r'searchlight/search/$'

    @rest_utils.ajax()
    def post(self, request):
        """Executes a search query against searchlight.

        Currently accepted parameters are (all optional):

        :param query: see Elasticsearch DSL or Searchlight documentation;
                      defaults to match everything
        :param index: one or more indices to search. Typically not necessary;
                      prefer using `type` instead
        :param type: one or more types to search. Uniquely identifies resource
                     types. Example: OS::Glance::Image
        :param offset: skip over this many results
        :param limit: return this many results
        :param sort: sort by one or more fields
        :param fields: restrict the fields returned for each document
        :param highlight: add an Elasticsearch highlight clause
        """
        search_parameters = dict(request.DATA) if request.DATA else {}

        # Set some defaults
        search_parameters.setdefault('limit', 20)
        search_parameters.setdefault('query', {'match_all': {}})

        # Example:
        # {"hits": ["_id": abc, "_source": {..}], "max_score": 2.0, "total": 3}
        return searchlight_post(
            '/search',
            request,
            search_parameters
        ).json()


@urls.register
class Plugins(generic.View):
    """API call to interrogate searchlight for enabled resource types.

       Use to determine the types you can query.
    """
    url_regex = r'searchlight/plugins/$'

    @rest_utils.ajax()
    def get(self, request):
        """Requests enabled searchlight plugins.

        At this time the response looks like:
           {"plugins": [{
               "index": "searchlight",
               "type": "OS::Glance::Image",
               "name": "OS::Glance::Image"
           }.. ]
        """
        return searchlight_get('/search/plugins', request).json()


@urls.register
class Facets(generic.View):
    """API call to interrogate searchlight for available search facets."""
    url_regex = r'searchlight/facets/$'

    @rest_utils.ajax()
    def get(self, request):
        """Requests available facets for the different resource types.

        :param type: optional type to limit facets returned.
                    Uniquely identifies resource types.
                    Example: OS::Glance::Image
        :param index: optional search index to limit facets returned.
                      Typically not needed, using the type will
                      automatically map to the index unless deployer
                      has changes.
        Note - the response is changing for the searchlight 1.0 release.
        In Mitaka the value for each resource type was a list (the content
        of the 'facets' key in the new format).

        At this time the response looks like:
           {
              "OS::Glance::Image": {
                "facets": [
                  {
                    "name": "status",
                    "type": "string"
                  },
                  {
                    "name": "created_at",
                    "type": "date"
                  }
                  ...
                ],
                "doc_count": 2
              },
              "OS::Nova::Server": {
                "facets": [
                  {
                    "name": "status",
                    "options": [
                      {
                        "doc_count": 1,
                        "key": "ACTIVE"
                      }
                    ],
                    "type": "string"
                  }
                  ...
                ],
                "doc_count": 1
              }
            }
        """

        # Set some defaults
        facet_res = searchlight_get('/search/facets',
                                    request,
                                    params=request.GET).json()
        if not facet_res:
            return facet_res

        # Check for old-format responses
        first_value = facet_res.values().next()
        if isinstance(first_value, list):
            # Old-style
            return {rt: {'facets': val}
                    for rt, val in facet_res.items()}
        return facet_res


def _searchlight_request(request_method, url, request, data=None, params=None):
    """Makes a request to searchlight with an optional payload.

    Should set any necessary auth headers and SSL parameters.
    """
    # Set verify if a CACERT is set and SSL_NO_VERIFY isn't True
    verify = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    if getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False):
        verify = False

    response = request_method(
        _get_searchlight_url(request) + url,
        headers={'X-Auth-Token': request.user.token.id},
        data=jsonutils.dumps(data) if data else None,
        verify=verify,
        params=params
    )

    try:
        response.raise_for_status()
    except r_exceptions.HTTPError as e:
        for error in rest_utils.http_errors:
            if (e.response.status_code == getattr(error, 'status_code', 0) and
                    exceptions.HorizonException in error.__bases__):
                raise error
        raise

    return response


# Create some convenience partial functions
searchlight_get = functools.partial(_searchlight_request, requests.get)
searchlight_post = functools.partial(_searchlight_request, requests.post)


def _get_searchlight_url(request):
    """Get searchlight's URL from keystone; allow an override in settings"""
    searchlight_url = getattr(settings, 'SEARCHLIGHT_URL', None)
    try:
        searchlight_url = base.url_for(request, 'search')
    except exceptions.ServiceCatalogException:
        pass
    # Currently the keystone endpoint is http://host:port/
    # without the version.
    return "/".join(map(lambda x: x.strip('/'), (searchlight_url, "v1")))
