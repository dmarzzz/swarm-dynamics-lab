CREATE TABLE IF NOT EXISTS r41_stage_authority(grant_id TEXT, stage TEXT, authority TEXT, source TEXT, manifest TEXT, maximum_calls INTEGER, maximum_model REAL, enabled INTEGER, PRIMARY KEY(grant_id,stage));
CREATE TRIGGER IF NOT EXISTS r41_stage_funding_guard BEFORE INSERT ON r41_work BEGIN
 SELECT CASE WHEN NOT EXISTS (
  SELECT 1 FROM r41_stage_authority a JOIN r41_scope s ON s.grant_id=a.grant_id
  WHERE a.grant_id=NEW.grant_id AND a.stage=NEW.stage AND a.enabled=1
   AND a.source=s.source AND a.manifest=s.manifest
   AND (SELECT count(*) FROM r41_work w WHERE w.grant_id=NEW.grant_id AND w.stage=NEW.stage)<a.maximum_calls
   AND ((SELECT count(*) FROM r41_work w WHERE w.grant_id=NEW.grant_id AND w.stage=NEW.stage)+1)*0.005696<=a.maximum_model+0.000000001
 ) THEN RAISE(ABORT,'stage_not_allocated_or_exhausted') END;
END;
