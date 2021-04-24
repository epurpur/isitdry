import datetime

def create_unix_timestamp(date):
    """This is a helper function used to return unix timestamp for dates in historical weather forecast"""
    unix_time = date.strftime("%s")
    return unix_time