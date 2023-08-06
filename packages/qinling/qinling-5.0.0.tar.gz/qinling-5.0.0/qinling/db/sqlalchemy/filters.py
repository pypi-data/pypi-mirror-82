#    Copyright 2016 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


def apply_filters(query, model, **filters):
    filter_dict = {}

    for key, value in filters.items():
        column_attr = getattr(model, key)

        if isinstance(value, dict):
            if 'in' in value:
                query = query.filter(column_attr.in_(value['in']))
            elif 'nin' in value:
                query = query.filter(~column_attr.in_(value['nin']))
            elif 'neq' in value:
                query = query.filter(column_attr != value['neq'])
            elif 'gt' in value:
                query = query.filter(column_attr > value['gt'])
            elif 'gte' in value:
                query = query.filter(column_attr >= value['gte'])
            elif 'lt' in value:
                query = query.filter(column_attr < value['lt'])
            elif 'lte' in value:
                query = query.filter(column_attr <= value['lte'])
            elif 'eq' in value:
                query = query.filter(column_attr == value['eq'])
            elif 'has' in value:
                like_pattern = '%{0}%'.format(value['has'])

                query = query.filter(column_attr.like(like_pattern))
        else:
            filter_dict[key] = value

    if filter_dict:
        query = query.filter_by(**filter_dict)

    return query
