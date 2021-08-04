#!/usr/bin/env python3
# -*- mode: python; mode: view -*-
import argparse
import os
from flask import Flask
from flask import request
import psycopg2


def environ_or_required(key):
    "Argparse environment vars helper"
    if os.environ.get(key):
        return {"default": os.environ.get(key)}
    else:
        return {"required": True}


def parse_args():
    parser = argparse.ArgumentParser(description="Test app")
    parser.add_argument(
        "--db",
        help="Required. May be in POSTGRES_DB env var",
        **environ_or_required("POSTGRES_DB")
    )
    parser.add_argument(
        "--user",
        help="Required. May be in POSTGRES_USER env var",
        **environ_or_required("POSTGRES_USER")
    )
    parser.add_argument(
        "--passwd",
        help="Required. May be in POSTGRES_PASSWORD env var",
        **environ_or_required("POSTGRES_PASSWORD")
    )
    parser.add_argument(
        "--host",
        help="Required. May be in POSTGRES_HOST env var",
        **environ_or_required("POSTGRES_HOST")
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    with psycopg2.connect(
        dbname=args.db, user=args.user, password=args.passwd, host=args.host
    ) as conn:
        with conn.cursor() as cursor:
            app = Flask(__name__)
            cursor.execute(
                "CREATE TABLE posts (id serial PRIMARY KEY, data varchar) IF NOT EXIST;"
            )

            @app.route("/post", methods=["POST"])
            def post():
                cursor.execute(
                    "INSERT INTO posts (data) VALUES (%s)", (
                        request.form["data"])
                )
                return request.form["data"]

            @app.route("/get")
            def get():
                cursor.execute("SELECT * FROM posts")
                return "\n".join(map(str, cursor.fetchall()))

            app.run("0.0.0.0:5000")
