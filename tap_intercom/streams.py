# streams: API URL endpoints to be called
# properties:
#   <root node>: Plural stream name for the endpoint
#   path: API endpoint relative path, when added to the base URL, creates the full path,
#       default = stream_name
#   key_properties: Primary key fields for identifying an endpoint record.
#   replication_method: INCREMENTAL or FULL_TABLE
#   replication_keys: bookmark_field(s), typically a date-time, used for filtering the results
#        and setting the state
#   params: Query, sort, and other endpoint specific parameters; default = {}
#   data_key: JSON element containing the results list for the endpoint; default = 'results'
#   bookmark_query_field: From date-time field used for filtering the query
#   bookmark_type: Data type for bookmark, integer or datetime
#   scroll_ind: True/False if endpoint may use scroll API for historical sync

STREAMS = {
    'admins': {
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE'
    },
    'companies': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['updated_at'],
        'bookmark_type': 'datetime',
        'scroll_ind': True
    },
    'company_attributes': {
        'path': 'data_attributes/company',
        'data_key': 'data_attributes',
        'key_properties': ['name'],
        'replication_method': 'FULL_TABLE'
    },
    'company_segments': {
        'path': 'segments',
        'data_key': 'segments',
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['updated_at'],
        'bookmark_type': 'datetime',
        'params': {
            'type': 'company',
            'include_count': 'true'
        }
    },
    # 'conversations': {
    #     'key_properties': ['id'],
    #     'replication_method': 'INCREMENTAL',
    #     'replication_keys': ['updated_at'],
    #     'bookmark_type': 'datetime',
    #     'children': {
    #         'conversation_parts': {
    #             'path': 'conversations/{}',
    #             'key_properties': ['id'],
    #             'replication_method': 'INCREMENTAL',
    #             'replication_keys': ['updated_at'],
    #             'bookmark_type': 'datetime'
    #         }
    #     }
    # },
    'customer_attributes': {
        'path': 'data_attributes/customer',
        'data_key': 'data_attributes',
        'key_properties': ['name'],
        'replication_method': 'FULL_TABLE'
    },
    'leads': {
        'path': 'contacts',
        'data_key': 'contacts',
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['updated_at'],
        'bookmark_type': 'datetime',
        'params': {
            'sort': 'updated_at',
            'order': 'asc'
        },
        'scroll_ind': True
    },
    'segments': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['updated_at'],
        'bookmark_type': 'datetime',
        'params': {
            'include_count': 'true'
        }
    },
    'tags': {
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE'
    },
    'teams': {
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE'
    },
    'users': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['updated_at'],
        'bookmark_query_field': 'updated_since',
        'bookmark_type': 'datetime',
        'params': {
            'sort': 'updated_at',
            'order': 'asc'
        },
        'scroll_ind': True
    }
}


def flatten_streams():
    flat_streams = {}
    # Loop through parents
    for stream_name, endpoint_config in STREAMS.items():
        flat_streams[stream_name] = {
            'key_properties': endpoint_config.get('key_properties'),
            'replication_method': endpoint_config.get('replication_method'),
            'replication_keys': endpoint_config.get('replication_keys')
        }
        # Loop through children
        children = endpoint_config.get('children')
        if children:
            for child_stream_name, child_enpoint_config in children.items():
                flat_streams[child_stream_name] = {
                    'key_properties': child_enpoint_config.get('key_properties'),
                    'replication_method': child_enpoint_config.get('replication_method'),
                    'replication_keys': child_enpoint_config.get('replication_keys')
                }
    return flat_streams
