<?php
    $pass = $_GET["pass"];
    $name = $_GET["name"];
    if ($pass == "password123_but_more_secure!") {
        if ($name == "") {
            echo '<br>Correct password, but the submitted first or last name is empty... please go back and try again.';
        } else {
            // Check if the name is already in the file
            $file = fopen("leaderboard.txt", "r");
            while (!feof($file)) {
                $line = fgets($file);
                if (strpos($line, $name) !== false) {
                    echo '<br>Error: The name "' . $name . '" is already in the leaderboard';
                    fclose($file);
                    exit;
                }
            }

            echo '<br>Congratulations, ' . $name . '! You have successfully completed the RELLIS Engineering Week Challenge!';
            $file = fopen("leaderboard.txt", "a");
            fwrite($file, $name . "\n");
            echo '<br>Your name has been added to the leaderboard';
            fclose($file);
        }
    } else {
        echo '<br>Incorrect password';
    }
?>
