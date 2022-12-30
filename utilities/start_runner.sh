#!/bin/bash

cml runner launch \
  --repo="$REPOSITORY_URL" \
  --token="$PERSONAL_ACCESS_TOKEN" \
  --labels="cml-docker-work" \
  --idle-timeout="60min"
