<?php
include('db.inc.php');

$action=$_GET['action'];
$sender_id=$_GET['sender_id'];
if($action==='add')
{
	$flag=$_GET['flag'];
	
	$result=mysql_query("INSERT INTO `asked` (sender_id,flag) VALUES ('$sender_id','$flag')");
	if($result){ return true;}
	else{ return false;}

}

if($action==='delete')
{
	$result=mysql_query("DELETE from `asked` WHERE sender_id=$sender_id");
	if($result){ return true;}
	else{ return false;}


}

if($action==='view')
{
	$result=mysql_query("SELECT * FROM `asked` WHERE sender_id=$sender_id");
	if(mysql_num_rows($result)==0){ echo "false";}
	else{
	
		while($row=mysql_fetch_assoc($result))
		{
			$flag=$row['flag'];
		
		
		}
		echo $flag;
		mysql_query("DELETE from `asked` WHERE sender_id=$sender_id");
	
	}

}


?>