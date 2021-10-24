#!/usr/bin/env bash

aws-vault --prompt=terminal exec theeye -- /usr/local/bin/terraform $@
