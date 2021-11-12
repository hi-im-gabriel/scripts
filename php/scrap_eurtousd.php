<?php
//Function to download the page
function download_page($path){
   	$ch = curl_init();
    	curl_setopt($ch, CURLOPT_URL,$path);
  	curl_setopt($ch, CURLOPT_FAILONERROR,1);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION,1);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
   	curl_setopt($ch, CURLOPT_TIMEOUT, 15);
  	$retValue = curl_exec($ch);          
    	curl_close($ch);
    	return $retValue;
}

//Calling and downloading the currency page
$sXML = download_page('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml');

//Parsing XML to Json and then to Array
$xml = simplexml_load_string($sXML, "SimpleXMLElement", LIBXML_NOCDATA);
$json = json_encode($xml);
$array = json_decode($json,TRUE);

//Today's date
$date = array_values($array['Cube']['Cube'])[0]['time'];

//Setting filename with today's date
$filename = "usd_currency_rates_{$date}.csv";

//Openning .csv file
$df = fopen($filename, 'w');

$usd = array_values($array['Cube']['Cube']['Cube'][0])[0]['rate'];
//Putting info into .csv

//First line(Columns)
$columns = array(
	0 => "Currency Code",
	1 => "Rate");
fputcsv($df, array_values($columns));
//Values
foreach($array['Cube']['Cube']['Cube'] as $r){
	$line = array_values($r)[0];
	$line['rate'] = $line['rate']/$usd;
	if($line['currency'] != 'USD'){
		fputcsv($df, $line);
	}
}
?>
