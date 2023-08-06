CREATE OR REPLACE FUNCTION lock_objects_and_detect_conflicts(
  read_current_oids BIGINT[],
  read_current_tids BIGINT[]
)
  RETURNS TABLE(zoid BIGINT, tid BIGINT, prev_tid BIGINT, committed_state BYTEA)
AS
$$
BEGIN

  -- lock in share should NOWAIT

  IF read_current_oids IS NOT NULL THEN
    -- readCurrent conflicts first so we don't waste time resolving
    -- state conflicts if we are going to fail the transaction. We only need to return
    -- the first conflict; it will immediately raise an exception.
    -- Up through PG12, RETURN QUERY does *NOT* stream to the client, it buffers
    -- everything. So we must manually break and not do the locking.

    -- Doing this in a single query takes some effort to make sure
    -- that the required rows all get locked. The optimizer is smart
    -- enough to push a <> condition from an outer query into a
    -- subquery. It is *not* smart enough to do the same with a CTE...
    -- ...prior to PG12. In PG12, CTEs can be inlined, and if it was,
    -- the same optimizer error would arise.
    --
    -- Fortunately, in PG12, "CTEs are automatically inlined if they
    -- have no side-effects, are not recursive, and are referenced
    -- only once in the query." The ``FOR SHARE`` clause counts as a
    -- side-effect, and so the CTE Is not inlined.

    -- Should this ever change, we could force the issue by using
    -- 'WITH ... AS MATERIALIZED' but that's not valid syntax before
    -- 12. (It also says recursive CTEs are not inlined, and that *is*
    -- valid on older versions, but this isn't actually a recursive
    -- query, even if we use that keyword, and I don't know if the
    -- keyword alone would be enough to fool it (the plan doesn't
    -- change on 11 when we use the keyword)).
    RETURN QUERY
      WITH locked AS (
        SELECT {CURRENT_OBJECT}.zoid, {CURRENT_OBJECT}.tid, t.tid AS desired
        FROM {CURRENT_OBJECT}
        INNER JOIN unnest(read_current_oids, read_current_tids) t(zoid, tid)
          USING (zoid)
        ORDER BY zoid
        FOR SHARE NOWAIT
      )
      SELECT locked.zoid, locked.tid, NULL::BIGINT, NULL::BYTEA
      FROM locked WHERE locked.tid <> locked.desired
      LIMIT 1;
    IF FOUND THEN
      RETURN;
    END IF;
  END IF;

  -- Unlike MySQL, we can simply do the SELECT (with PERFORM) for its
  -- side effects to lock the rows.
  -- This one will block.

  -- A note on the query: PostgreSQL will typcially choose a
  -- sequential scan on the temp_store table and do a nested loop join
  -- against the object_state_pkey index culminating in a sort after
  -- the join. This is the same whether we write a WHERE IN (SELECT)
  -- or a INNER JOIN. (This is without a WHERE prev_tid <> 0 clause.)

  -- That changes substantially if we ANALYZE the temp table;
  -- depending on the data, it might do an MERGE join with an index
  -- scan on temp_store_pkey (lots of data) or it might do a
  -- sequential scan and sort in memory before doing a MERGE join
  -- (little data). (Again without the WHERE prev_tid clause.)

  -- However, ANALYZE takes time, often more time than it takes to actually
  -- do the nested loop join.

  -- If we add a WHERE prev_tid clause, even if we ANALYZE, it will
  -- choose a sequential scan on temp_store with a FILTER. Given that most
  -- transactions contain relatively few objects, and that it would do a
  -- sequential scan /anyway/, this is fine, and worth it to avoid probing
  -- the main index for new objects.

  -- TODO: Is it worth doing partitioning and putting prev_tid = 0 in their own
  -- partition? prev_tid isn't the primary key, zoid is, though, and range
  -- partitioning has to include the primary key when there is one.

  PERFORM {CURRENT_OBJECT}.zoid
  FROM {CURRENT_OBJECT}
  INNER JOIN temp_store USING (zoid)
  WHERE temp_store.prev_tid <> 0
  ORDER BY {CURRENT_OBJECT}.zoid
  FOR UPDATE OF {CURRENT_OBJECT};

  RETURN QUERY
  SELECT cur.zoid, cur.tid,
         temp_store.prev_tid, {OBJECT_STATE_NAME}.state
  FROM {CURRENT_OBJECT} cur
  INNER JOIN temp_store USING (zoid)
  {OBJECT_STATE_JOIN}
  WHERE temp_store.prev_tid <> cur.tid;

  RETURN;

END;
$$
LANGUAGE plpgsql;
