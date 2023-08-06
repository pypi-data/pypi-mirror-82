# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Nested data structure diffing support (dict of dicts). 
  Exposed through the function object_diff.diff_iter.

## [0.1.0] - 2020-10-18

### Added

- Single level of dict diffing in `object_diff.diff_dict_iter`.
- Diffing of scalar values in `object_diff.value_diff`.
- Setup `pre-commit` and `black` formatting.
