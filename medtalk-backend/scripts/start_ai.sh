export NEO_PROFILE="http://10.203.228.251:7474/"
export NEO_PASSWORD="Citrus130649"

cd src && uvicorn aiapp.main:app --host '0.0.0.0' --port 8010 --reload --reload-dir ./aiapp