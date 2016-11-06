<?php
$mysqli = new mysqli("myapp", "user", "password", "database");
if (!$mysqli) {
    /* Of course, your error handling is nicer... */
    die(sprintf("[%d] %s\n", mysqli_connect_errno(), mysqli_connect_error()));
}

/* Create a global table - a table available on all shards */
mysqlnd_ms_fabric_select_global($mysqli, "test.fabrictest");
if (!$mysqli->query("CREATE TABLE test.fabrictest(id INT NOT NULL PRIMARY KEY)")) {
    die(sprintf("[%d] %s\n", $mysqli->errno, $mysqli->error));
}

/* Switch connection to appropriate shard and insert record */
mysqlnd_ms_fabric_select_shard($mysqli, "test.fabrictest", 10);
if (!($res = $mysqli->query("INSERT INTO fabrictest(id) VALUES (10)"))) {
    die(sprintf("[%d] %s\n", $mysqli->errno, $mysqli->error));
}

/* Try to read newly inserted record */
mysqlnd_ms_fabric_select_shard($mysqli, "test.fabrictest", 10);
if (!($res = $mysqli->query("SELECT id FROM test WHERE id = 10"))) {
    die(sprintf("[%d] %s\n", $mysqli->errno, $mysqli->error));
}
?>