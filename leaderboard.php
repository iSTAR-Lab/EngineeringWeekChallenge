<!-- Webpage that displays a list of names from a text file-->
<html>
<head>
    <title>List of Famous Hackers</title>
</head>
<!-- In-line style to change h1 font to Arial -->
<style>
    * {
        font-family: Arial;
    }

    .footer {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translate(-50%, 0);
        text-align: center;
    }
    h1 {
        font-size: 40px;
    }

    .hacker {
        font-size: 30px;
    }
</style>

<body>
    <center>
        <!-- Display the leaderboard -->
        <h1>List of Famous Hackers</h1>
    </center>

  <center>
<?php
// Open the file
$file = fopen("leaderboard.txt", "r");
// Read the file
while (!feof($file)) {
  $line = fgets($file);
  // Display the names
  echo "<div class=\"hacker\">" . $line . "</div><br>";
} // Close the file 
fclose($file); ?>

  </center>
</div>
<div class="footer">
        <img src="header.png" height="100px" />
    </div>
<div>

<script>
    let handle = setInterval( () => {
  location.reload()
  }, 15000);
</script>

</body>
</html>