![alt text](https://github.com/codewithadelite/domains/blob/master/static/images/screenshots/domain1.png?raw=true)

# TOOL FOR DOMAINS MANAGEMENT AND INSIGHT

This tool is used to import domains data from JSON files or onboarded through a REST API Endpoint

Example of domains in JSON:

```json
{
  "fqdn": "domain.com",
  "created_at": "2022-12-27 08:26:49.219717",
  "expire_at": "2022-12-27 08:26:49.219717",
  "deleted_at": "2022-12-27 08:26:49.219717",
  "flags": [
    {
      "flag_type": "EXPIRED",
      "valid_from": "2022-12-27 08:26:49.219717",
      "valid_to": "2022-12-27 08:26:49.219717"
    }
  ]
}
```

To run this application run the following command:

```
python3 manage.py runserver
```
