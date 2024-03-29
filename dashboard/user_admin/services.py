from contextlib import closing

from django.db import connection

from base.utils.db import dictfetchone


def cnts():
    sql = """
        SELECT  ( SELECT COUNT(*)
            FROM   dashboard_member
            where is_student is FALSE and status == 2 and permission != 3
            ) AS tcnt, ( SELECT COUNT(*)
            FROM   dashboard_member
            where is_student is TRUE and permission != 3
            ) AS scnt, (
            SELECT COUNT(*)
            FROM   dashboard_group
            where status == 2 or status == 1
            ) AS agcnt, (
            SELECT COUNT(*)
            FROM dashboard_group
            where status == 1
            ) AS sgcnt, (
            SELECT COUNT(*)
            FROM   dashboard_group
            where status == 3
            ) AS egcnt, (
            SELECT COUNT(*)
            FROM   dashboard_group
            ) AS allgcnt,
            (SELECT COUNT(*)
            FROM   dashboard_interested
            WHERE contacted is FALSE or "view" is FALSE 
            ) AS icnt,
            (SELECT COUNT(*)
            FROM   dashboard_course
            ) AS ccnt
        FROM dashboard_position
        limit 1
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        res = dictfetchone(cursor)

    return res


def gcnt():
    sql = """
            SELECT  ( SELECT COUNT(*)
                FROM dashboard_group
                where status == 1
                ) AS start, (SELECT COUNT(*)
                FROM   dashboard_group
                where status == 2
                ) AS act,(SELECT COUNT(*)
                FROM   dashboard_group
                where status == 3
                ) AS end,
                (SELECT COUNT(*)
                FROM   dashboard_interested
                WHERE contacted is FALSE or "view" is FALSE 
                ) AS icnt
            FROM dashboard_group
            limit 1
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        res = dictfetchone(cursor)

    return res
