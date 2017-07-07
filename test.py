import db
data = {
  "type": "partner",
  "company_name": "StarCompanyNew",
  "domain": "Starter",
  "language": "english",
  "address": "In the nowhere",
  "country": "Mars1",
  "city": "Star1",
  "email": "post@mail.gi",
  "cphone": "456798024",
  "active": "1",
  "prtnprofile_id": "2"
}

if data:
    if data["type"] == "partner":
        sql = "INSERT INTO partner (company_name, domain, language, address, city, country, email, cphone, active, prtnprofile_id) VALUES ('{company_name}', '{domain}', '{language}', '{address}', '{city}', '{country}', '{email}', {cphone}, {active}, {prtnprofile_id})".format(**data)
    elif data["type"] == "organization":
        sql = "INSERT INTO organization (prtnid, organization_name, orgprofile_id) VALUES ({},{},{})".format(data["prtnid"], data["organization_name"], data["orgprofile_id"])
    else:
        print False
    print sql
    condb = db.ncbDB()
    res = condb.ncb_pushQuery(sql)
