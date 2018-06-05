#!/bin/bash
#su - postgres -c "createdb fbpicks"
su - postgres -c "pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d fbpicks /fbpicks_db/latest.dump"
