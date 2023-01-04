#!/bin/bash

cml runner launch \
  --repo="$REPOSITORY_URL" \
  --token="$PERSONAL_ACCESS_TOKEN" \
  --labels="cml-gpu" \
  --idle-timeout="10min"