#!/bin/bash
docker run --name fb-postgres -p 5432:5432 -v `pwd`:/dump -d rotschopf/rpi-postgres
