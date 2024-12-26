#!/bin/bash
set -e

# Wait for Elasticsearch to be ready
until curl -s -u elastic:${ELASTIC_PASSWORD} http://localhost:9200 >/dev/null; do
    echo 'Waiting for Elasticsearch...'
    sleep 3
done

# Create shopinvader role
curl -X PUT -u elastic:${ELASTIC_PASSWORD} "http://localhost:9200/_security/role/shopinvader" -H 'Content-Type: application/json' -d'{
  "indices": [
    {
      "names": ["se_backend_shopinvader_demo*"],
      "privileges": ["read", "view_index_metadata"]
    }
  ]
}'

echo "Shopinvader role created successfully"