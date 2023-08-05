import html
import json
import time

import requests


class API(object):
    ROOT_URL = 'https://api.litmos.com/v1.svc'
    PAGINATION_OFFSET = 200
    api_key = None
    app_name = None

    @classmethod
    def _base_url(cls, resource, **kwargs):
        return cls.ROOT_URL + "/" + \
            resource + \
            ("/" + kwargs['resource_id'] if kwargs.get('resource_id', None) else "") + \
            ("/" + kwargs['sub_resource'] if kwargs.get('sub_resource', None) else "") + \
            ("/" + kwargs['sub_resource_id'] if kwargs.get('sub_resource_id', None) else "") + \
            '?source=' + cls.app_name + \
            '&format=json' + \
            ("&search=" + str(kwargs['search_param']) if kwargs.get('search_param', None) else "") + \
            ("&limit=" + str(kwargs['limit']) if kwargs.get('limit', None) else "") + \
            ("&start=" + str(kwargs['start']) if kwargs.get('start', None) else "")

    @classmethod
    def _perform_request(cls, method, url, **kwargs):
        kwargs['headers'] = {'apikey': cls.api_key}
        response = requests.request(method, url, **kwargs)

        if response.status_code == 503:  # request rate limit exceeded
            time.sleep(60)
            response = requests.request(method, url, **kwargs)

        response.raise_for_status()

        return response

    @staticmethod
    def _parse_response(response):
        return json.loads(html.unescape(response.text))

    @classmethod
    def find(cls, resource, resource_id):
        response = cls._perform_request(
            'GET',
            cls._base_url(resource, resource_id=resource_id)
        )

        return cls._parse_response(response)

    @classmethod
    def delete(cls, resource, resource_id):
        cls._perform_request(
            'DELETE',
            cls._base_url(resource,
                          resource_id=resource_id
                          )
        )

        return True

    @classmethod
    def create(cls, resource, attributes):
        response = cls._perform_request(
            'POST',
            cls._base_url(resource),
            json=attributes
        )

        return cls._parse_response(response)

    @classmethod
    def update(cls, resource, resource_id, attributes):
        response = cls._perform_request(
            'PUT',
            cls._base_url(resource, resource_id=resource_id),
            json=attributes
        )

        if response.text:
            return cls._parse_response(response)

        return {}


    @classmethod
    def search(cls, resource, search_param):
        response = cls._perform_request(
            'GET',
            cls._base_url(resource, search_param=search_param)
        )

        return cls._parse_response(response)

    @classmethod
    def _get_all(cls, resource, results, start_pos):
        response = cls._perform_request(
            'GET',
            cls._base_url(resource, limit=cls.PAGINATION_OFFSET, start=start_pos)
        )

        response_list = cls._parse_response(response)
        results += response_list

        if not response_list:
            return results
        else:
            return cls._get_all(resource, results, start_pos + cls.PAGINATION_OFFSET)

    @classmethod
    def all(cls, resource):
        return cls._get_all(resource, [], 0)

    @classmethod
    def get_children(cls, resource, resource_id):
        response = cls._perform_request(
            'GET',
            cls._base_url(resource, resource_id=resource_id, sub_resource=resource)
        )

        return cls._parse_response(response)

    @classmethod
    def get_sub_resource(cls, resource, resource_id, sub_resource):
        return cls._get_sub_resource(resource, resource_id, sub_resource, [], 0)

    @classmethod
    def _get_sub_resource(cls, resource, resource_id, sub_resource, results, start_pos):
        response = cls._perform_request(
            'GET',
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource,
                limit=cls.PAGINATION_OFFSET, start=start_pos
            )
        )

        response_list = cls._parse_response(response)
        results += response_list

        if not response_list:
            return results
        else:
            return cls._get_sub_resource(resource, resource_id, sub_resource, results, start_pos + cls.PAGINATION_OFFSET)

    @classmethod
    def add_sub_resource(cls, resource, resource_id, sub_resource, attributes):
        response = cls._perform_request(
            'POST',
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource
            ),
            json=attributes
        )

        if response.text:
            return cls._parse_response(response)

        return True

    @classmethod
    def update_sub_resource(cls, resource, resource_id, sub_resource, sub_resource_id, attributes=None):
        response = cls._perform_request(
            'PUT',
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource,
                sub_resource_id=sub_resource_id
            ),
            json=attributes
        )

        if response.text:
            return cls._parse_response(response)

        return True

    @classmethod
    def remove_sub_resource(cls, resource, resource_id, sub_resource, sub_resource_id):
        cls._perform_request(
            'DELETE',
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource,
                sub_resource_id=sub_resource_id)
        )

        return True

    @classmethod
    def remove_sub_resources(cls, resource, resource_id, sub_resource, attributes):
        response = cls._perform_request(
            'DELETE',
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource
            ),
            json=attributes
        )

        if response.text:
            return cls._parse_response(response)

        return True
