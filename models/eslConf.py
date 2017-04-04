import ESL


def getConfUUID(room):
    
function getConfUUID($room)
{
    $ip = getLowConferenceCount($confroom);
    $esl = new eslConnection($ip, '8021', 'ClueCon');
    $e = $esl->api("conference conf_{$confroom} xml_list");
    $xml = simplexml_load_string($e->getBody());
    $xmlattr = $xml->conference[0]->attributes();
    return $xmlattr->uuid;
}
