<?php
include('db.inc.php');

$company=strtolower($_GET['company']);

$result=mysql_query("SELECT * FROM `placement2016-17` WHERE company='$company'");

while($row=mysql_fetch_assoc($result))
		{
			$number=$row['number'];
		
		
		}
		if($number){ echo $number." students placed in ".$company;}
		else{ echo "0";}


?>