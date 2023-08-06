# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
# Copyright (C) 2019 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

import json

import pytest
from invenio_records.models import RecordMetadata
from invenio_search import current_search

from invenio_rdm_records.cli import create_fake_record


@pytest.mark.skip()
def test_create_fake_record_saves_to_db(app, es_clear, location):
    """Test if fake records are saved to db."""
    # app needed for config overwrite of pidstore
    assert RecordMetadata.query.first() is None

    created_record = create_fake_record()

    retrieved_record = RecordMetadata.query.first()
    assert created_record.record.model == retrieved_record


def _assert_single_hit(response, expected_record):
    assert response.status_code == 200

    search_hits = response.json['hits']['hits']

    # Kept for debugging
    for hit in search_hits:
        print("Search hit:", json.dumps(hit, indent=4, sort_keys=True))

    assert len(search_hits) == 1
    search_hit = search_hits[0]
    # only a record that has been published has an id, so we don't check for it
    for key in ['created', 'updated', 'metadata', 'links']:
        assert key in search_hit

    required_fields = [
        '_access',
        '_owners',
        'access_right',
        'contact',
        'titles',
        'descriptions',
        'recid',
        'resource_type',
        'creators',
        'contributors',
        'licenses'
    ]
    for key in required_fields:
        expected_value = expected_record[key]
        if key == 'publication_date':
            expected_value = expected_value[:10]
        assert search_hit['metadata'][key] == expected_value


@pytest.mark.skip()
def test_create_fake_record_saves_to_index(client, es_clear, location):
    """Test the creation of fake records and searching for them."""
    created_record = create_fake_record()
    # ES does not flush fast enough some times
    current_search.flush_and_refresh(index='records')

    response = client.get("/rdm-records")

    _assert_single_hit(response, created_record.record)
