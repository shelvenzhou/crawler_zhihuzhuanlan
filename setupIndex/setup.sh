curl -XPOST http://localhost:9200/column -d createIndex.json
curl -XPOST http://localhost:9200/post -d createIndex.json
curl -XPUT http://localhost:9200/_river/column/_meta -d @column.json
curl -XPUT http://localhost:9200/_river/post/_meta  -d @post.json
curl -XPUT 'localhost:9200/_settings' -d '{ "index" : { "number_of_replicas" : 0 } }'

