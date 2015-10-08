import pygerduty
pg_api_key = "SECRET_PD_API_KEY"
pager = pygerduty.PagerDuty("your_org","{}".format(pg_api_key))
pager.trigger_incident("{}".format(pg_api_key), "Bardzo deskryptywny opis zdarzenia", "", "przykladowa reakcja")
