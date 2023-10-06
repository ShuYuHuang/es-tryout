
- (20230926) Space warning, connection timeout:
    - {"@timestamp":"2023-09-26T13:05:30.192Z", "log.level": "WARN", "message":"flood stage disk watermark [95%] exceeded on [I6rPVGlWTzqPrbJvFboLXQ][48043dde07e1][/usr/share/elasticsearch/data] free: 10gb[2.2%], all indices on this node will be marked read-only", "ecs.version": "1.2.0","service.name":"ES_ECS","event.dataset":"elasticsearch.server","process.thread.name":"elasticsearch[48043dde07e1][generic][T#20]","log.logger":"org.elasticsearch.cluster.routing.allocation.DiskThresholdMonitor","elasticsearch.cluster.uuid":"FpNTpx1ORue3Ey1ImPq2Mw","elasticsearch.node.id":"I6rPVGlWTzqPrbJvFboLXQ","elasticsearch.node.name":"48043dde07e1","elasticsearch.cluster.name":"docker-cluster"}
    > not enough spaces that all the spaces in this docker will be marked as read-only, which caused the connection time-out
    - setup watermark threshold (examples are in 2_start_esearch.sh)

- (20230925) TlsError: TLS error caused by: TlsError(TLS error caused by: SSLError([SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1123)))
    > Not running elastic search properly
    - run elastic search using docker in advance

- (20230923) ERROR: cannot import name 'deprecated' from 'typing_extensions'
    > In my case I'm using pydantic and was able to walk-around the issue with pydantic<2.3.0, which includes the deprecated import
    - update pydantic

- (20230922) ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
    > pylint 2.12.2 requires mccabe<0.7,>=0.6, but you have mccabe 0.7.0 which is incompatible.
    - use mccabe 0.6









