import os

from fastapi import Request, HTTPException, Depends

from fastapi.security import APIKeyHeader


poc_auth_key = os.getenv("POC_AUTH_KEY")


def poc_auth(request: Request):
    if request.headers.get("Authorization") != poc_auth_key or not poc_auth_key:
        raise HTTPException(status_code=401)


poc_auths = [Depends(APIKeyHeader(name="Authorization")), Depends(poc_auth)]


__all__ = ["poc_auths"]
