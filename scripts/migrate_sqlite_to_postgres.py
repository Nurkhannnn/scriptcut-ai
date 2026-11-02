#!/usr/bin/env python
"""One-off data copy: SQLite -> PostgreSQL.

Usage (after `alembic upgrade head` on the target):
    python scripts/migrate_sqlite_to_postgres.py sqlite:///./old.db postgresql+psycopg2://user:pw@host/db

Reflects both databases and copies the columns they share, converts SQLite 0/1
booleans, then resets Postgres serial sequences.
"""
import sys

from sqlalchemy import MetaData, create_engine, text

COPY_ORDER = ["projects", "segments", "exports"]  # parents first; extend with your own tables


def main(src_url: str, dst_url: str) -> None:
    src, dst = create_engine(src_url), create_engine(dst_url)
    src_meta, dst_meta = MetaData(), MetaData()
    src_meta.reflect(src)
    dst_meta.reflect(dst)

    with src.connect() as s, dst.begin() as d:
        for name in COPY_ORDER:
            if name not in src_meta.tables or name not in dst_meta.tables:
                print(f"skip {name}: missing on one side")
                continue
            s_tbl, d_tbl = src_meta.tables[name], dst_meta.tables[name]
            cols = [c.name for c in d_tbl.columns if c.name in s_tbl.columns]
            payload = [{c: r._mapping[c] for c in cols} for r in s.execute(s_tbl.select())]
            bool_cols = [c.name for c in d_tbl.columns if str(c.type) == "BOOLEAN"]
            for row in payload:
                for col in bool_cols:
                    if row.get(col) is not None:
                        row[col] = bool(row[col])
            if payload:
                d.execute(d_tbl.insert(), payload)
            print(f"{name}: copied {len(payload)} rows")

        for name in COPY_ORDER:
            tbl = dst_meta.tables.get(name)
            if tbl is not None and "id" in tbl.columns and str(tbl.c.id.type) == "INTEGER":
                d.execute(text(
                    f"SELECT setval(pg_get_serial_sequence('{name}', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM {name}"
                ))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
