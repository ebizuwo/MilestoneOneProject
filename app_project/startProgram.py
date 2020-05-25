import ipywidgets as widgets
import pgeocode
from IPython import display


def program():
    lat_long = ()
    def get_lat_long(zip_):
        # using a library called pgeocode
        nomi = pgeocode.Nominatim('US')
        geoinfo = nomi.query_postal_code(zip_)
        lat = geoinfo.loc['latitude']
        long = geoinfo.loc['longitude']
        lat_long = lat, long

    def callback(wdgt):
        display(wdgt.value)
        get_lat_long(wdgt.value)

    text=widgets.Text(
        value='',
        placeholder='30082',
        description='Zip:',
        disabled=False
    )

    display(text)
    text.on_submit(callback)
    return lat_long