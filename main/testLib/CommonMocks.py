
from django.http import QueryDict
from unittest.mock import Mock


def createMockUserProfile(fields={}):
    valid_profile = {
        'user': Mock(),
        'nr_stories': 1,
        'nr_vocabs': 1,
        'profile_pic': Mock()
    }
    valid_profile.update(fields)

    profile = Mock()
    for key, value in valid_profile.items():
        profile.__setattr__(key, value)

    valid_profile['user'].__setattr__('__iter__', Mock())
    return profile


def createMockQuery(base_content, override_fields={}):
    query_content = base_content.copy()
    query_content.update(override_fields)

    query_dict = QueryDict('', mutable=True)
    query_dict.update(query_content)

    return query_dict
