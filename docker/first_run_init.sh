#!/bin/bash
# After the first docker-compose up, you need to run a few commands:
docker-compose exec db /fbpicks_db/import_db.sh
sleep 5
docker-compose restart django
