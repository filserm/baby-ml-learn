from soco import SoCo
import time

def radio():
    meta_template = """
    <DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
        xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/"
        xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
        <item id="R:0/0/0" parentID="R:0/0" restricted="true">
            <dc:title>{title}</dc:title>
            <upnp:class>object.item.audioItem.audioBroadcast</upnp:class>
            <desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">
                {service}
            </desc>
        </item>
    </DIDL-Lite>' """

    tunein_service = "SA_RINCON65031_"

    speaker = '192.168.0.34'
    preset = 0
    limit = 12

    mySonos = SoCo(speaker)

    if mySonos:
        stations = mySonos.get_favorite_radio_stations(preset, limit)

    #print(stations)

    for station in stations["favorites"]:
        title = station["title"]
        uri = station["uri"]
        uri = uri.replace("&", "&amp;")
        
        metadata = meta_template.format(title=station["title"], service=tunein_service)

        if 'Ö3' in title:
            
            print(mySonos.play_uri(uri, metadata))
            time.sleep(5)
            break
