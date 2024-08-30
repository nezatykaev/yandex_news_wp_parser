<?php

$servername = "p729516.mysql.ihc.ru";
$username = "p729516_1";
$password = "C92wP3";
$database = "p729516_1";

$post_title = $_POST["post_title"];
$post_content = $_POST["post_content"];
$url = $_POST["post_url"];
$post_source = $_POST["post_source"];

$conn = new mysqli("$servername", "$username", "$password", "$database");
    if($conn->connect_error){
        die("Ошибка: " . $conn->connect_error);
    }
    $name = $conn->real_escape_string($_POST["username"]);
    $age = $conn->real_escape_string($_POST["userage"]);
    $sql = "INSERT INTO wp_posts (post_author, post_date, post_content, post_title, post_status, comment_status, ping_status, post_name, post_parent, guid, menu_order, post_type, post_mime_type, comment_count, post_source ) VALUES ('1', '2024-08-30 13:00:09', '$post_content', '$post_title', 'publish', 'open', 'closed', '$url', '0', 'http://p729516.ihc.xyz/wordpress/wp-content/uploads/2024/08/13735448-1.jpg', '0', 'news', '', '0', '$post_source')";

    if($conn->query($sql)){
	echo "yes";
    } else{
	echo "no";
    }
    $conn->close();

?>
