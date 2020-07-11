# moneyTransfer

## Overview
Money Transaction is a system based on the recent famous FastAPI.

### techniques selection

System's technique selection is as follows:
- Service Framework：`python/fastapi`
- ORM: `sqlalchemy` + `encode/databases` (as FastAPI recommends)
- python async web service: `asgi/uvicorn`
- authentication: `JWT`
- python type hints: `pydantic`


### why fastapi?

`fastapi` is a python web framework gathering features of flask, django. It supports both asynchronous checkpoints and normal blog ways. Using `uvicorn` to support eventloop make fastapi faster. More excellent feature is the pydantic and data scheme, encouraging to follow the OpenAPI rules, the `swagger-docs` will be generated automatically.



#### build images

```
git clone https://github.com/williamsyb/moneyTransfer.git
cd moneyTransfer
sh build.sh
docker-compose up
```
