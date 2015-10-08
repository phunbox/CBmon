import pygerduty
pg_api_key = "SECRET_PD_API_KEY"
pager = pygerduty.PagerDuty("allegro-group","{}".format(pg_api_key))
pager.acknowledge_incident("SECRET_PD_API_KEY","1337")
