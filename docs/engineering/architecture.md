# Architecture

The project is split into small modules so each piece can be tested without network access.

- `models` holds endpoint and result data.
- `classifier` turns raw results into health states.
- `summary` aggregates states.
- `render` formats a readable output.
