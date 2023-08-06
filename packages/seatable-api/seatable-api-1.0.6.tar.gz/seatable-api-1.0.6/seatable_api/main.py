import json
import requests

from .constants import ROW_FILTER_KEYS, ColumnTypes
from .constants import RENAME_COLUMN, RESIZE_COLUMN, FREEZE_COLUMN, MOVE_COLUMN, MODIFY_COLUMN_TYPE, DELETE_COLUMN
from .socket_io import connect_socket_io


def parse_headers(token):
    return {
        'Authorization': 'Token ' + token,
        'Content-Type': 'application/json',
    }


def parse_server_url(server_url):
    return server_url.rstrip('/')


def parse_response(response):
    if response.status_code >= 400:
        raise ConnectionError(response.status_code, response.text)
    else:
        try:
            data = json.loads(response.text)
            return data
        except:
            pass

class SeaTableAPI(object):
    """SeaTable API
    """

    def __init__(self, token, server_url):
        """
        :param token: str
        :param server_url: str
        """
        self.token = token
        self.server_url = parse_server_url(server_url)
        self.dtable_server_url = None
        self.dtable_uuid = None
        self.headers = None
        self.socketIO = None

    def __str__(self):
        return 'SeaTableAPI Object [ %s ]' % self.dtable_uuid

    def auth(self, with_socket_io=False):
        """Auth to SeaTable
        """
        url = self.server_url + '/api/v2.1/dtable/app-access-token/'
        headers = parse_headers(self.token)
        response = requests.get(url, headers=headers)
        data = parse_response(response)

        self.dtable_uuid = data.get('dtable_uuid')
        jwt_token = data.get('access_token')
        self.headers = parse_headers(jwt_token)
        self.dtable_server_url = parse_server_url(data.get('dtable_server'))

        if with_socket_io is True:
            self.socketIO = connect_socket_io(
                self.dtable_server_url, self.dtable_uuid, jwt_token)

    def _metadata_server_url(self):
        return self.dtable_server_url + '/api/v1/dtables/' + self.dtable_uuid + '/metadata/'

    def _row_server_url(self):
        return self.dtable_server_url + '/api/v1/dtables/' + self.dtable_uuid + '/rows/'

    def _batch_row_server_url(self):
        return self.dtable_server_url + '/api/v1/dtables/' + self.dtable_uuid + '/batch-append-rows/'

    def _filtered_rows_server_url(self):
        return self.dtable_server_url + '/api/v1/dtables/' + self.dtable_uuid + '/filtered-rows/'

    def _row_link_server_url(self):
        return self.dtable_server_url + '/api/v1/dtables/' + self.dtable_uuid + '/links/'

    def _app_download_link_url(self):
        return self.server_url + '/api/v2.1/dtable/app-download-link/'

    def _app_upload_link_url(self):
        return self.server_url + '/api/v2.1/dtable/app-upload-link/'

    def _column_server_url(self):
        return self.dtable_server_url + '/api/v1/dtables/' + self.dtable_uuid + '/columns/'

    def get_metadata(self):
        """
        :return: dict
        """
        url = self._metadata_server_url()
        response = requests.get(url, headers=self.headers)
        data = parse_response(response)
        return data.get('metadata')

    def list_rows(self, table_name, view_name=None):
        """
        :param table_name: str
        :param view_name: str
        :return: list
        """
        url = self._row_server_url()
        params = {
            'table_name': table_name,
        }
        if view_name:
            params['view_name'] = view_name
        response = requests.get(url, params=params, headers=self.headers)
        data = parse_response(response)
        return data.get('rows')

    def append_row(self, table_name, row_data):
        """
        :param table_name: str
        :param row_data: dict
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row': row_data,
        }
        response = requests.post(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def batch_append_rows(self, table_name, rows_data):
        """
        :param table_name: str
        :param rows_data: dict
        """
        url = self._batch_row_server_url()
        json_data = {
            'table_name': table_name,
            'rows': rows_data,
        }
        response = requests.post(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def insert_row(self, table_name, row_data, anchor_row_id):
        """
        :param table_name: str
        :param row_data: dict
        :param anchor_row_id: str
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row': row_data,
            'anchor_row_id': anchor_row_id,
        }
        response = requests.post(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def update_row(self, table_name, row_id, row_data):
        """
        :param table_name: str
        :param row_id: str
        :param row_data: dict
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row_id': row_id,
            'row': row_data,
        }
        response = requests.put(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def delete_row(self, table_name, row_id):
        """
        :param table_name: str
        :param row_id: str
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row_id': row_id,
        }
        response = requests.delete(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def filter_rows(self, table_name, filters, view_name=None, filter_conjunction='And'):
        """
        :param table_name: str
        :param view_name: str
        :param filters: list
        :param filter_conjunction: str, 'And' or 'Or'
        :return: list
        """
        # params check
        if not filters:
            raise ValueError('filters can not be empty.')
        if not isinstance(filters, list):
            raise ValueError('filters invalid.')
        if len(filters) != len([f for f in filters if isinstance(f, dict)]):
            raise ValueError('filters invalid.')

        for filter in filters:
            for key in filter.keys():
                if key not in ROW_FILTER_KEYS:
                    raise ValueError('filters invalid.')

        if filter_conjunction not in ['And', 'Or']:
            raise ValueError('filter_conjunction invalud, filter_conjunction must be '
                             '"And" or "Or"')

        params = {
            'table_name': table_name,
        }
        if view_name:
            params['view_name'] = view_name

        json_data = {
            'filters': filters,
            'filter_conjunction': filter_conjunction,
        }

        url = self._filtered_rows_server_url()
        response = requests.get(
            url, json=json_data, params=params, headers=self.headers)
        data = parse_response(response)
        return data.get('rows')

    def get_file_download_link(self, path):
        """
        :param path: str
        :return: str
        """
        url = self._app_download_link_url()
        params = {'path': path}
        headers = parse_headers(self.token)
        response = requests.get(url, params=params, headers=headers)
        data = parse_response(response)
        return data.get('download_link')

    def get_file_upload_link(self):
        """
        :return: dict
        """
        url = self._app_upload_link_url()
        headers = parse_headers(self.token)
        response = requests.get(url, headers=headers)
        data = parse_response(response)
        return data

    def add_link(self, link_id, table_name, other_table_name, row_id, other_row_id):
        """
        :param link_id: str
        :param table_name: str
        :param other_table_name: str
        :param row_id: str
        :param other_row_id: str
        """
        url = self._row_link_server_url()
        json_data = {
            'link_id': link_id,
            'table_name': table_name,
            'other_table_name': other_table_name,
            'table_row_id': row_id,
            'other_table_row_id': other_row_id,
        }
        response = requests.post(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def remove_link(self, link_id, table_name, other_table_name, row_id, other_row_id):
        """
        :param link_id: str
        :param table_name: str
        :param other_table_name: str
        :param row_id: str
        :param other_row_id: str
        """
        url = self._row_link_server_url()
        json_data = {
            'link_id': link_id,
            'table_name': table_name,
            'other_table_name': other_table_name,
            'table_row_id': row_id,
            'other_table_row_id': other_row_id,
        }
        response = requests.delete(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def list_columns(self, table_name, view_name=None):
        """
        :param table_name: str
        :param view_name: str
        :return: list
        """
        url = self._column_server_url()
        params = {
            'table_name': table_name,
        }
        if view_name:
            params['view_name'] = view_name
        response = requests.get(url, params=params, headers=self.headers)
        data = parse_response(response)
        return data.get('columns')

    def insert_column(self, table_name, column_name, column_type, column_key=None):
        """
        :param table_name: str
        :param column_name: str
        :param column_type: ColumnType enum
        :param column_key: str, which you want to insert after
        :return: dict
        """
        if column_type not in ColumnTypes:
            raise ValueError("type %s invalid!" % (column_type,))
        url = self._column_server_url()
        json_data = {
            'table_name': table_name,
            'column_name': column_name,
            'column_type': column_type.value
        }
        if column_key:
            json_data['column_key'] = column_key
        response = requests.post(url, json=json_data, headers=self.headers)
        data = parse_response(response)
        return data

    def rename_column(self, table_name, column_key, new_column_name):
        """
        :param table_name: str
        :param column_key: str
        :param new_column_name: str
        :return: dict
        """
        url = self._column_server_url()
        json_data = {
            'op_type': RENAME_COLUMN,
            'table_name': table_name,
            'column_key': column_key,
            'new_column_name': new_column_name
        }
        response = requests.put(url, json=json_data, headers=self.headers)
        data = parse_response(response)
        return data

    def resize_column(self, table_name, column_key, new_column_width):
        """
        :param table_name: str
        :param column_key: str
        :param old_column_width: int
        :param new_column_width: int
        :return: dict
        """
        url = self._column_server_url()
        json_data = {
            'op_type': RESIZE_COLUMN,
            'table_name': table_name,
            'column_key': column_key,
            'new_column_width': new_column_width
        }
        response = requests.put(url, json=json_data, headers=self.headers)
        data = parse_response(response)
        return data

    def freeze_column(self, table_name, column_key, frozen):
        """
        :param table_name: str
        :param column_key: str
        :param frozen: bool
        :return: dict
        """
        url = self._column_server_url()
        json_data = {
            'op_type': FREEZE_COLUMN,
            'table_name': table_name,
            'column_key': column_key,
            'frozen': frozen
        }
        response = requests.put(url, json=json_data, headers=self.headers)
        data = parse_response(response)
        return data

    def move_column(self, table_name, column_key, target_column_key):
        """
        :param table_name: str
        :param column_key: str
        :param target_column_key: bool
        :return: dict
        """
        url = self._column_server_url()
        json_data = {
            'op_type': MOVE_COLUMN,
            'table_name': table_name,
            'column_key': column_key,
            'target_column_key': target_column_key
        }
        response = requests.put(url, json=json_data, headers=self.headers)
        data = parse_response(response)
        return data

    def modify_column_type(self, table_name, column_key, new_column_type):
        """
        :param table_name: str
        :param column_key: str
        :param new_column_type: str
        :return: dict
        """
        if new_column_type not in ColumnTypes:
            raise ValueError("type %s invalid!" % (new_column_type,))
        url = self._column_server_url()
        json_data = {
            'op_type': MODIFY_COLUMN_TYPE,
            'table_name': table_name,
            'column_key': column_key,
            'new_column_type': new_column_type.value
        }
        response = requests.put(url, json=json_data, headers=self.headers)
        data = parse_response(response)
        return data

    def delete_column(self, table_name, column_key):
        """
        :param table_name: str
        :param column_key: str
        :return: None
        """
        url = self._column_server_url()
        json_data = {
            'table_name': table_name,
            'column_key': column_key
        }
        response = requests.delete(url, json=json_data, headers=self.headers)
        data = parse_response(response)
        return data
