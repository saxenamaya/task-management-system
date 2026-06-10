# Architecture

```
                 ┌───────────────┐
                 │    Swagger    │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    FastAPI    │
                 └───────┬───────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   Auth Router      Task Router    Assignment Router
        │                │                │
        └────────┬───────┴───────┬────────┘
                 ▼               ▼
             Services       Rule Engine
                 │
                 ▼
            Repositories
                 │
                 ▼
              SQLite
```
