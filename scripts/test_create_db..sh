#!/bin/bash
edgedb database create dialaxy_test_db
edgedb migration create -d dialaxy_test_db --non-interactive
edgedb migrate -d dialaxy_test_db
echo database create and migration successful
